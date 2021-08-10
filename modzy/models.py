# -*- coding: utf-8 -*-
"""Classes for interacting with models."""

import logging
from datetime import datetime
from ._api_object import ApiObject
from urllib.parse import urlencode
from .error import NotFoundError, ResponseError
from typing import Union
from time import time as t
from time import sleep

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

        # TODO: this was moved from the models api to the resources api, perhaps it should go in a different module?
        endpoint = "/resources/processing/models"

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
                    engines_ready = sum([engine["ready"] for engine in model_details["engines"]])
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
