# -*- coding: utf-8 -*-
"""Classes for interacting with models."""

import re
import json
import logging
from datetime import datetime
from operator import getitem
from collections import OrderedDict
from typing import Union
from ._api_object import ApiObject
from urllib.parse import urlencode
from .error import NotFoundError, ResponseError, BadRequestError
from time import time as t
from time import sleep
from ._util import load_model, upload_input_example, run_model, deploy_model

# define constants used for model deployment method
MODEL_HARDWARE_GPU_ID = -6
MODEL_HARDWARE_ARM_ID = -99
MODEL_HARDWARE_OTHER_ID = 1
class Models:
    """The `Models` object.

    This object is used to retreive information about models from the API.

    Note:
        This class should not be instantiated directly but rather accessed through the `models`
        attribute of an `ApiClient` instance.
    """

    _base_route = '/models'

    def __init__(self, api_client):
        """Creates a `Models` instance.

        Args:
            api_client (ApiClient): An `ApiClient` instance.
        """
        self._api_client = api_client
        self.logger = logging.getLogger(__name__)
        # model deployment specific instance variables
        self.default_inputs = [
            {
                "name": "input",
                "acceptedMediaTypes": "application/json",
                "maximumSize": 1000000,
                "description": "Default input data"
            }
        ]
        self.default_outputs = [
            {
                "name": "results.json",
                "mediaType": "application/json",
                "maximumSize": 1000000,
                "description": "Default output data"
            }    
        ]

        # extract available hardware resource
        account_resources_endpoint = f"{self._base_route}/requirements/account"
        resources_list = self._api_client.http.get(account_resources_endpoint)
        self.hardware_config_options = [item for item in resources_list if item['status'] == "ACTIVE"]
        self.hardware_config_options_lookup = {}
        for item in self.hardware_config_options:
            self.hardware_config_options_lookup[item['requirementId']] = {
                "cpu": float(float(item['cpuAmount'].split('m')[0])/1000),    # converting Modzy value into unit expected by SDK
                "memory": float(item['memoryAmount'].split('G')[0])           # converting Modzy value into float value to compare with SDK value
            }
         
                

    def get_model_processing_details(self, model, version):
        """
        Checks to see if a model with a certain id and version is active, and if it is, will return the model
        details for that particular model.

        Args:
            model: model id, or `Model` instance
            version: semantic version of previously specified model

        Returns:
            model: The model details for the model with the id and version specified or None if there are no active
            models with these parameters

        """
        model_id = Model._coerce_identifier(model)

        endpoint = "/resources/processing/engines"

        result = self._api_client.http.get(endpoint)

        for model in result:
            if model["identifier"] == model_id and model["version"] == version:
                return model
        return None

    def get_minimum_engines(self) -> int:
        """Obtains the total amount of processing engines set as the minimum processing capacity across all models."""
        route = f"{self._base_route}/processing-engines"
        raw_result = self._api_client.http.get(route)
        minimum_engines_sum = int(raw_result["minimumProcessingEnginesSum"])

        self.logger.info(f"The sum of minimum processing engines is: {minimum_engines_sum}")
        return minimum_engines_sum

    def update_processing_engines(
        self, model, version: str, min_engines: int, max_engines: int, timeout: int = 0, poll_rate: int = 5
    ):
        """
        Updates the minimum and maximum processing engines for a specific model identifier and version.

        Args:
            model: model id, or `Model` instance
            version: semantic version of previously specified model
            min_engines: minimum number of processing engines allowed for this model and version
            max_engines: maximum number of processing engines allowed for this model and version
            timeout: time in seconds to wait until processing engine is spun up. 0 means return immediately, None means
            block and wait forever
            poll_rate: If timeout is nonzero, this value will determine the rate at which the state of the cluster
            is checked

        Raises:
            ForbiddenError: Occurs if the current API client does not have the appropriate entitlements in order
            to update processing engines
        """
        if not max_engines >= min_engines:
            raise ValueError("Your min_engines value may not exceed the max_engines value")

        model_id = Model._coerce_identifier(model)

        base_request_body = {
            "minimumParallelCapacity": min_engines,
            "maximumParallelCapacity": max_engines
        }
        base_endpoint = f"{self._base_route}/{model_id}/versions/{version}"

        error_message = None
        try:
            result = self._api_client.http.patch(base_endpoint, json_data={"processing": base_request_body})
            self.logger.info(
                f"Updated processing engines for Model {model_id} {version}: \n{result['processing']}"
            )
        except ResponseError as e:
            error_message = e.message
            self.logger.error(f"Direct try failed {error_message}, second try")
            try:
                result = self._api_client.http.patch(f"{base_endpoint}/processing", json_data=base_request_body)
                self.logger.info(
                    f"Updated processing engines for Model {model_id} {version}: \n{result['processing']}"
                )
            except ResponseError as e:
                error_message = e.message
                self.logger.error(error_message)
                raise ValueError(error_message)

        if timeout == 0:
            return
        else:
            assert timeout is None or timeout > 0, \
                "Timeout must either be an integer >= 0 or None if you wish to indicate no timeout"
            start_time = t()
            while True:
                current_time = t() - start_time
                if timeout is not None and current_time > timeout:
                    self.logger.warning(
                        f"Timeout of {timeout} seconds reached while waiting for processing engines to initialize."
                    )
                    return
                model_details = self.get_model_processing_details(model_id, version)
                if model_details is not None:  # This means the model with the id and version is now visible
                    engines_ready = model_details['ready']
                    if engines_ready >= min_engines:
                        self.logger.info(f"{engines_ready} engines are ready.")
                        return
                sleep(poll_rate)

    def get(self, model):
        """Gets a `Model` instance.

        Args:
            model (Union[str, Model]): The model identifier or a `Model` instance.

        Returns:
            Model: The `Model` instance.

        Raises:
            ApiError: A subclass of ApiError will be raised if the API returns an error status,
                or the client is unable to connect.
        """
        modelId = Model._coerce_identifier(model)
        self.logger.debug("getting model %s", model)
        json_obj = self._api_client.http.get('{}/{}'.format(self._base_route, modelId))
        return Model(json_obj, self._api_client)

    def get_by_name(self, name):
        """Gets a `Model` instance by name.

        Args:
            name (str): The model name.

        Returns:
            Model: The `Model` instance.

        Raises:
            ApiError: A subclass of ApiError will be raised if the API returns an error status,
                or the client is unable to connect.
        """
        params = {'name': name}
        models = self.get_models(**params)
        if models is not None and len(models) > 0:
            return self.get(models[0])
        else:
            raise NotFoundError("Model {} not found".format(name), self._base_route, None)

    def get_related(self, model):
        """Gets a list of all the models associated with the model provided, together with the model’s details.

        Returns:
            List[Model]: A list of `Model` instances.

        Raises:
            ApiError: A subclass of ApiError will be raised if the API returns an error status,
                or the client is unable to connect.
        """
        self.logger.debug("getting models related to model %s", model)
        identifier = Model._coerce_identifier(model)
        json_list = self._api_client.http.get('{}/{}/related-models'.format(self._base_route, identifier))
        return list(Model(json_obj, self._api_client) for json_obj in json_list)

    def get_versions(self, model):
        """Gets a list of all the versions associated with the model provided.

        Returns:
            List[ModelVersion]: A list of `Version` instances.

        Raises:
            ApiError: A subclass of ApiError will be raised if the API returns an error status,
                or the client is unable to connect.
        """
        self.logger.debug("getting versions related to model %s", model)
        identifier = Model._coerce_identifier(model)
        json_list = self._api_client.http.get('{}/{}/versions'.format(self._base_route, identifier))
        return list(ModelVersion(json_obj, self._api_client) for json_obj in json_list)

    def get_version(self, model, version):
        """Gets a versions associated with the model provided.

        Returns:
            ModelVersion: A instance of `ModelVersion` instances.

        Raises:
            ApiError: A subclass of ApiError will be raised if the API returns an error status,
                or the client is unable to connect.
        """
        self.logger.debug("getting version model %s version %s", model, version)
        modelId = Model._coerce_identifier(model)
        versionId = ModelVersion._coerce_identifier(version)
        json_obj = self._api_client.http.get('{}/{}/versions/{}'.format(self._base_route, modelId, versionId))
        return ModelVersion(json_obj, self._api_client)

    def get_version_input_sample(self, model, version):
        """Gets the input sample associated with the model and version provided.

        Returns:
            String: A json string with the input sample

        Raises:
            ApiError: A subclass of ApiError will be raised if the API returns an error status,
                or the client is unable to connect.
        """
        self.logger.debug("getting input sample: model %s version %s", model, version)
        modelId = Model._coerce_identifier(model)
        versionId = ModelVersion._coerce_identifier(version)
        json_obj = self._api_client.http.get('{}/{}/versions/{}/sample-input'.format(self._base_route, modelId, versionId))
        return json_obj

    def get_version_output_sample(self, model, version):
        """Gets the output sample associated with the model and version provided.

        Returns:
            String: A json string with the output sample

        Raises:
            ApiError: A subclass of ApiError will be raised if the API returns an error status,
                or the client is unable to connect.
        """
        self.logger.debug("getting output sample: model %s version %s", model, version)
        modelId = Model._coerce_identifier(model)
        versionId = ModelVersion._coerce_identifier(version)
        json_obj = self._api_client.http.get('{}/{}/versions/{}/sample-output'.format(self._base_route, modelId, versionId))
        return json_obj

    def get_all(self):
        """Gets a list of all `Model` instances.

        Returns:
            List[Model]: A list of `Model` instances.

        Raises:
            ApiError: A subclass of ApiError will be raised if the API returns an error status,
                or the client is unable to connect.
        """
        self.logger.debug("getting all models")
        return self.get_models()

    def get_models(self, model_id=None, author=None, created_by_email=None, name=None, description=None,
                   is_active=None, is_expired=None, is_recommended=None, last_active_date_time=None,
                   expiration_date_time=None, sort_by=None, direction=None, page=None, per_page=1000):
        """Gets a list of `Model` instances within a set of parameters.

        Args:
            model_id (Optional[str]): Identifier of the model
            author (Optional[str]): authoring company
            created_by_email (Optional[str]): creator email
            name (Optional[str]): name of the model
            description (Optional[str]): description of the model
            is_active (Optional[boolean, str]): availability of the model in the marketplace
            is_expired (Optional[boolean, str]): expiration status
            is_recommended (Optional[boolean, str]): recommended status
            last_active_date_time (Optional[datetime, str]): latest use date
            expiration_date_time (Optional[datetime, str]): expiration date
            sort_by (Optional[str]): attribute name to sort results
            direction (Optional[str]): Direction of the sorting algorithm (asc, desc)
            page (Optional[float]): The page number for which results are being returned
            per_page (Optional[float]): The number of models returned by page

        Returns:
            List[Model]: A list of `Model` instances.
        Raises:
            ApiError: A subclass of ApiError will be raised if the API returns an error status,
                or the client is unable to connect.
        """
        if model_id is not None and not isinstance(model_id, str):
            raise TypeError("the model_id param should be a string")
        if author is not None and not isinstance(author, str):
            raise TypeError("the author param should be a string")
        if created_by_email is not None and not isinstance(created_by_email, str):
            raise TypeError("the created_by_email param should be a string")
        if name is not None and not isinstance(name, str):
            raise TypeError("the name param should be a string")
        if description is not None and not isinstance(description, str):
            raise TypeError("the description param should be a string")
        if is_active is not None:
            if isinstance(is_active, bool):
                is_active = str(is_active)
            elif not isinstance(is_active, str):
                raise TypeError("the is_active param should be a bool or string")
        if is_expired is not None:
            if isinstance(is_expired, bool):
                is_expired = str(is_expired)
            elif not isinstance(is_expired, str):
                raise TypeError("the is_expired param should be a bool or string")
        if is_recommended is not None:
            if isinstance(is_recommended, bool):
                is_recommended = str(is_recommended)
            elif not isinstance(is_recommended, str):
                raise TypeError("the is_recommended param should be a bool or string")
        if last_active_date_time is not None:
            if isinstance(last_active_date_time, datetime):
                last_active_date_time = last_active_date_time.isoformat(timespec='milliseconds')
            elif not isinstance(last_active_date_time, str):
                raise TypeError("the last_active_date_time param should be a datetime or string")
        if expiration_date_time is not None:
            if isinstance(expiration_date_time, datetime):
                expiration_date_time = expiration_date_time.isoformat(timespec='milliseconds')
            elif not isinstance(expiration_date_time, str):
                raise TypeError("the expiration_date_time param should be a datetime or string")
        if sort_by is not None and not isinstance(sort_by, str):
            raise TypeError("the sort_by param should be a string")
        if direction is not None and not isinstance(direction, str):
            raise TypeError("the direction param should be a string")
        if page is not None:
            if isinstance(page, (int, float)):
                page = int(page)
            else:
                raise TypeError("the page param should be a number")
        if per_page is not None:
            if isinstance(per_page, (int, float)):
                per_page = int(per_page)
            else:
                raise TypeError("the per_page param should be a number")
        body = {
            "modelId":model_id,
            "author": author,
            "createdByEmail":created_by_email,
            "name":name,
            "description": description,
            "isActive": is_active,
            "isExpired": is_expired,
            "isRecommended": is_recommended,
            "lastActiveDateTime": last_active_date_time,
            "expirationDateTime": expiration_date_time,
            "sort-by": sort_by,
            "direction": direction,
            "page": page,
            "per-page": per_page
        }
        body = {k: v for (k, v) in body.items() if v is not None}
        self.logger.debug("body 2? %s", body)
        json_list = self._api_client.http.get('{}?{}'.format(self._base_route, urlencode(body)))
        return list(Model(json_obj, self._api_client) for json_obj in json_list)

    def edit_model_metadata(self, model_id, model_version, long_description=None, technical_details=None, 
                            performance_summary=None, performance_metrics=None, input_details=None, output_details=None):

        '''
        Edit a model's metadata after it is deployed

        Args:
            model_id (str): Model identifier of model to edit
            model_version (str): Model version of model to edit
            long_description (str): Description to appear on model biography page
            technical_details (str): Technical details to appear on model biography page. Markdown is accepted
            performance_summary (str): Description providing model performance to appear on model biography page
            performance_metrics (List): List of arrays describing model performance statistics
            input_details (List): List of dictionaries describing details of model inputs
            output_details (List): List of dictionaries describing details of model outputs

        Returns:
            dict: Metadata of newly edited model information including formatted URL to newly deployed model page.
        Raises:
            ApiError: A subclass of ApiError will be raised if the API returns an error status,
                or the client is unable to connect.        
        '''

        # validate model version exists    
        try:
            json_obj = self._api_client.http.get('{}/{}/versions/{}'.format(self._base_route, model_id, model_version))
            _ = ModelVersion(json_obj, self._api_client)
        except NotFoundError as e:
            raise e

        # update model metadata
        model_metadata_patch = {
            "inputs": input_details, 
            "outputs": output_details,   
            "statistics": performance_metrics,
            "longDescription": long_description,
            "technicalDetails": technical_details,
            "performanceSummary": performance_summary                
        }
        model_data_patch = self._api_client.http.patch(f"{self._base_route}/{model_id}/versions/{model_version}", model_metadata_patch)
        self.logger.info(f"Patched Model Data: {json.dumps(model_data_patch)}")  

        # get edited model URL and return model data
        base_url = self._api_client.base_url.split("api")[0][:-1] 
        container_data = {
            'model_data': json.dumps(model_data_patch),
            'container_url': f"{base_url}{self._base_route}/{model_id}/{model_version}"
        }
        return container_data                 
    
    def deploy(
        self, container_image, model_name, model_version, sample_input_file=None, architecture="amd64", credentials=None, 
        model_id=None, run_timeout=None, status_timeout=None, short_description=None, tags=[], cpu_count:Union[float, int]=None, memory:Union[float, int]=None,
        gpu=False, long_description=None, technical_details=None, performance_summary=None,
        performance_metrics=None, input_details=None, output_details=None, model_picture=None
        ):
        """Deploys a new `Model` instance.

        Args:
            container_image (str): Docker container image to be deployed. This string should represent what follows a `docker pull` command 
            model_name (str): Name of model to be deployed
            model_version (str): Version of model to be deployed
            architecture (str): `{'amd64', 'arm64', 'arm'}` If set to `arm64` or `arm`, deploy method will expedite the deployment process and bypass some Modzy tests that are only available for models compiled for amd64 chips. 
            sample_input_file (str): Path to local file to be used for sample inference
            credentials (dict): Dictionary containing credentials if the container image is private. The keys in this dictionary must be `["user", "pass"]`
            model_id (str): Model identifier if deploying a new version to a model that already exists
            run_timeout (str): Timeout threshold for container `run` route
            status_timeout (str): Timeout threshold for container `status` route
            short_description (str): Short description to appear on model biography page
            tags (list): List of tags to make model more discoverable in model library
            cpu_count (Union[float, int]): Number of CPU cores needed by model container
            memory (Union[float, int]): RAM needed by model container in GB (e.g., 1 = 1GB, 0.5 = 500MB)
            gpu (bool): Flag for whether or not model requires GPU to run
            long_description (str): Description to appear on model biography page
            technical_details (str): Technical details to appear on model biography page. Markdown is accepted
            performance_summary (str): Description providing model performance to appear on model biography page
            performance_metrics (List): List of arrays describing model performance statistics
            input_details (List): List of dictionaries describing details of model inputs
            output_details (List): List of dictionaries describing details of model outputs
            model_picture (str): Filepath to image for model card page

        Returns:
            dict: Newly deployed model information including formatted URL to newly deployed model page.
        Raises:
            ApiError: A subclass of ApiError will be raised if the API returns an error status,
                or the client is unable to connect.
        """ 
        # generate model identifier and version to create new model        
        if model_id:
            identifier, version = model_id, model_version
            # create new version of existing model
            data = {"version": version}
            try:
                response = self._api_client.http.post(f"{self._base_route}/{identifier}/versions", data)
            except BadRequestError as e:
                raise e
        else:
            # create new model object
            data = {'name': model_name, 'version': model_version}
            response = self._api_client.http.post(self._base_route, data)
            identifier, version = response.get('identifier'), model_version

        self.logger.info(f"Created Model Version: {identifier}, {version}")

        # add tags and description
        tags_and_description = {
            'description': short_description or ''
        }
        if len(tags) > 0:
            tags_and_description['tags'] = tags
        response = self._api_client.http.patch(f"{self._base_route}/{identifier}", tags_and_description)

        # upload container image

        registry = {'registry': {'url': container_image, 'username': credentials['user'], 'password': credentials['pass']}} if credentials else {'registry': {'url': container_image}}      
        response = self._api_client.http.post(f"{self._base_route}/{identifier}/versions/{version}/container-image", registry)
        self.logger.info("Uploaded Container Image")

        # add model metadata
        run_timeout_body = int(run_timeout)*1000 if run_timeout else 60000
        status_timeout_body = int(status_timeout)*1000 if status_timeout else 60000      

        if architecture in ["arm64", "arm"]:
            # assign "ARM" hardware requirement to bypass validation tests
            model_metadata = {
                "requirement": {"requirementId": MODEL_HARDWARE_ARM_ID},                
            }     
            model_data = self._api_client.http.patch(f"{self._base_route}/{identifier}/versions/{version}", model_metadata)
            self.logger.info(f"Model Data: {json.dumps(model_data)}")

            # load model container
            try:
                load_model(self._api_client, self.logger, identifier, version)
            except Exception as e:
                raise ValueError("Loading model container failed. Make sure you passed through a valid Docker registry container image. \n\nSee full error below:\n{}".format(e))
            
            # update model metadata
            model_metadata_patch = {
                "inputs": input_details, 
                "outputs": output_details,   
                "statistics": performance_metrics or [],
                "processing": {
                    "minimumParallelCapacity": 0,
                    "maximumParallelCapacity": 1
                },
                "longDescription": long_description or "",
                "technicalDetails": technical_details or "",
                "performanceSummary": performance_summary or ""                
            }
            model_data = self._api_client.http.patch(f"{self._base_route}/{identifier}/versions/{version}", model_metadata_patch)
            self.logger.info(f"Patched Model Data: {json.dumps(model_data)}")            
            
            # upload model picture
            if model_picture:
                files = {'file': open(model_picture, 'rb')}
                params = {'description': "model card image"}
                res = self._api_client.http.post(f"/models/{identifier}/image", params=params, file_data=files)               
            
            # deploy model and skip tests (because model is compiled for arm64)
            try:
                deploy_model(self._api_client, self.logger, identifier, version)
            except Exception as e:
                raise ValueError("Deployment failed. Check to make sure all of your parameters and assets are valid and try again. \n\nSee full error below:\n{}".format(e))
        elif architecture=="amd64":  
            # determine model hardare requirement ID based on CPU, GPU, and memory parameters
            if gpu:
                hardware_requirement_id = MODEL_HARDWARE_GPU_ID
            elif cpu_count and not memory or memory and not cpu_count:
                raise ValueError("You must provide valid values for BOTH memory and cpu_count parameters")
            elif cpu_count and memory:
                # filter config options based on user-specified parameters
                hardware_keep = {k:v for k,v in self.hardware_config_options_lookup.items() if float(self.hardware_config_options_lookup[k]['cpu']) >= cpu_count and float(self.hardware_config_options_lookup[k]['memory']) >= memory}
                hardware_keep_sorted = OrderedDict(sorted(hardware_keep.items(), key=lambda x:(getitem(x[1], 'cpu'), getitem(x[1], 'memory'))))
                try:
                    hardware_requirement_id = list(hardware_keep_sorted.keys())[0]
                except IndexError:
                    raise ValueError("Requested CPU count and memory values exceed available resource configuration options. The following resource options are available:\n\n{}\n\nPlease contact your Modzy administrator if you need a new resource configuration option.".format(self.hardware_config_options))
            else:
                hardware_requirement_id = MODEL_HARDWARE_OTHER_ID
        
            # patch model metadata
            model_metadata = {
                "requirement": {"requirementId": hardware_requirement_id},
                "timeout": {
                    "run": run_timeout_body,
                    "status": status_timeout_body
                },
                "inputs": input_details or self.default_inputs,
                "outputs": output_details or self.default_outputs,    
                "statistics": performance_metrics or [],
                "processing": {
                    "minimumParallelCapacity": 0,
                    "maximumParallelCapacity": 1
                },
                "longDescription": long_description or "",
                "technicalDetails": technical_details or "",
                "performanceSummary": performance_summary or ""
            }
            model_data = self._api_client.http.patch(f"{self._base_route}/{identifier}/versions/{version}", model_metadata)
            self.logger.info(f"Model Data: {json.dumps(model_data)}")

            # load model container
            try:
                load_model(self._api_client, self.logger, identifier, version)
            except Exception as e:
                raise ValueError("Loading model container failed. Make sure you passed through a valid Docker registry container image. \n\nSee full error below:\n{}".format(e))
            # upload sample data for inference test
            try:
                upload_input_example(self._api_client, self.logger, identifier, version, model_data, sample_input_file)
            except Exception as e:
                raise ValueError("Uploading sample input failed. \n\nSee full error below:\n{}".format(e))
            # run sample inference
            try:
                run_model(self._api_client, self.logger, identifier, version)
            except Exception as e:
                raise ValueError("Inference test failed. Make sure the provided input sample is valid and your model can process it for inference. \n\nSee full error below:\n{}".format(e))
            # make sure model metadata reflects user-specified fields
            try:
                model_data = self._api_client.http.patch(f"{self._base_route}/{identifier}/versions/{version}", model_metadata)
                self.logger.info(f"Model Data: {json.dumps(model_data)}")
            except Exception as e:
                raise ValueError("Patching model metadata failed. See full error below:\n\n{}".format(e))
            # upload model picture
            try:
                if model_picture:
                    files = {'file': open(model_picture, 'rb')}
                    params = {'description': "model card image"}
                    res = self._api_client.http.post(f"/models/{identifier}/image", params=params, file_data=files)
            except Exception as e:
                self.logger("Uploading model image card failed. Continuing deployment")
            # deploy model pending all tests have passed
            try:
                deploy_model(self._api_client, self.logger, identifier, version)
            except Exception as e:
                raise ValueError("Deployment failed. Check to make sure all of your parameters and assets are valid and try again. \n\nSee full error below:\n{}".format(e))
        else:
            raise ValueError("Invalid value for `architecture` parameter. Choose option from array: {'amd', 'arm'}")
            
        # get new model URL and return model data
        base_url = self._api_client.base_url.split("api")[0][:-1] 
        container_data = {
            'model_data': json.dumps(model_data),
            'container_url': f"{base_url}{self._base_route}/{identifier}/{version}"
        }
        return container_data


class Model(ApiObject):
    """A model object.

    This object contains a parsed copy of the information returned from the server about a certain model.

    Attributes:
        identifier (str): The model identifier.

    Note:
        This class should not be instantiated directly. Instead, it is returned by various package
        functions.
        This object is a `dict` subclass that also supports attribute access. Information can be
        accessed through dotted attribute notation using "snake_case" or the original "camelCase" JSON
        key name (``model.long_description`` or ``model.longDescription``). Alternatively, the original
        "camelCase" JSON key can be used with bracketed key access notation (``model['longDescription']``).
    """
    def __init__(self, json_obj, api_client=None):
        super().__init__(json_obj, api_client)
        if "identifier" in self.keys():  # Temporal fix for the duplicity between modelId and identifier results
            self["modelId"] = self["identifier"]

    @classmethod
    def _coerce_identifier(cls, maybe_model):
        modelId = getattr(maybe_model, 'modelId', maybe_model)
        if not isinstance(modelId, str):
            raise TypeError('the identifier must be {} or str, not {}'
                            .format(cls.__name__, type(maybe_model).__name__))
        return modelId

    def sync(self):
        """Updates the `Model` instance's data in-place with new data from the API.

        Returns:
            Model: The `Model` instance (self).

        Raises:
            ApiError: A subclass of ApiError will be raised if the API returns an error status,
                or the client is unable to connect.
        """
        updated = self._api_client.models.get(self.modelId)
        self.update(updated)  # is updating in place a bad idea?
        return self

    def get_versions(self):
        """Gets a list of all the versions associated with this model.

        Returns:
            List[Version]: A list of `Version` instances.

        Raises:
            ApiError: A subclass of ApiError will be raised if the API returns an error status,
                or the client is unable to connect.
        """
        return self._api_client.models.get_versions(self.modelId)

    def get_related(self):
        """Gets a list of all the models associated with this model.

        Returns:
            List[Model]: A list of `Model` instances.

        Raises:
            ApiError: A subclass of ApiError will be raised if the API returns an error status,
                or the client is unable to connect.
        """
        return self._api_client.models.get_related(self.modelId)

    def submit_text(self, version, source, source_name='job'):
        """Submits text data for a single source `Job`.

        See:
            :py:meth:`modzy.jobs.Jobs.submit_text`
        """
        return self._api_client.jobs.submit_text(self.modelId, version, source, source_name=source_name)

    def submit_text_bulk(self, version, sources):
        """Submits text data for a multiple source `Job`.

        See:
            :py:meth:`modzy.jobs.Jobs.submit_text_bulk`
        """
        return self._api_client.jobs.submit_text_bulk(self.modelId, version, sources)

    def submit_bytes(self, version, source, source_name='job'):
        """Submits bytes-like data for a single source `Job`.

        See:
            :py:meth:`modzy.jobs.Jobs.submit_bytes`
        """
        return self._api_client.jobs.submit_bytes(self.modelId, version, source, source_name=source_name)

    def submit_bytes_bulk(self, version, sources):
        """Submits bytes-like data for a multiple source `Job`.

        See:
            :py:meth:`modzy.jobs.Jobs.submit_bytes_bulk`
        """
        return self._api_client.jobs.submit_bytes_bulk(self.modelId, version, sources)

    def submit_files(self, version, source, source_name='job'):
        """Submits a filepath or file-like data for a single source `Job`.

        See:
            :py:meth:`modzy.jobs.Jobs.submit_files`
        """

        return self._api_client.jobs.submit_files(self.modelId, version, source, source_name=source_name)

    def submit_files_bulk(self, version, sources):
        """Submits a filepath or file-like data for a multiple source `Job`.

        See:
            :py:meth:`modzy.jobs.Jobs.submit_files_bulk`
        """
        return self._api_client.jobs.submit_files_bulk(self.modelId, version, sources)

    def submit_aws_s3(self, version, source, access_key_id, secret_access_key, region, source_name='job'):
        """Submits AwS S3 hosted data for a single source `Job`.

        See:
            :py:meth:`modzy.jobs.Jobs.submit_aws_s3`
        """
        return self._api_client.jobs.submit_aws_s3(self.modelId, version, source,
                                                   access_key_id, secret_access_key, region, source_name=source_name)

    def submit_aws_s3_bulk(self, version, sources, access_key_id, secret_access_key, region):
        """Submits AwS S3 hosted data for a multiple source `Job`.

        See:
            :py:meth:`modzy.jobs.Jobs.submit_aws_s3_bulk`
        """
        return self._api_client.jobs.submit_aws_s3_bulk(self.modelId, version, sources, access_key_id,
                                                        secret_access_key, region)

    def submit_jdbc(self, version, url, username, password, driver, query):
        """Submits jdbc query as input for a `Job`, each row is interpreted as a input.

        See:
            :py:meth:`modzy.jobs.Jobs.submit_jdbc`
        """
        return self._api_client.jobs.submit_jdbc(self.modelId, version, url, username, password, driver, query)

    def __str__(self):
        return "Model(modelId='{}')".format(self.modelId)


class ModelVersion(ApiObject):
    """A model version object.

    This object contains a parsed copy of the information returned from the server about a certain model version.

    Attributes:
        version (str): The model version identifier.

    Note:
        This class should not be instantiated directly. Instead, it is returned by various package
        functions.
        This object is a `dict` subclass that also supports attribute access. Information can be
        accessed through dotted attribute notation using "snake_case" or the original "camelCase" JSON
        key name (``model.long_description`` or ``model.longDescription``). Alternatively, the original
        "camelCase" JSON key can be used with bracketed key access notation (``model['longDescription']``).
    """

    @classmethod
    def _coerce_identifier(cls, maybe_model_version):
        versionId = getattr(maybe_model_version, 'version', maybe_model_version)
        if not isinstance(versionId, str):
            raise TypeError('the identifier must be {} or str, not {}'
                            .format(cls.__name__, type(maybe_model_version).__name__))
        return versionId

    def __str__(self):
        return "ModelVersion(version='{}')".format(self.version)
