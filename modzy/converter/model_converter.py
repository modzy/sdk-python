import logging
from types import BuiltinMethodType
from ..error import Timeout
import time
import requests

class ModelConverter:
    """The `Models` object.

    This object is used to retrieve information about models from the API.

    Note:
        This class should not be instantiated directly but rather accessed through the `converter`
        attribute of an `ApiClient` instance.
    """

    _base_route = '/converter'

    def __init__(self, api_client):
        """Creates a `ModelConverter` instance.

        Args:
            api_client (ApiClient): An `ApiClient` instance.
        """
        self._api_client = api_client
        self.logger = logging.getLogger(__name__)
    
    def start(
        self,
        sp_access_key_id,
        sp_secret_access_key,
        blobstore_container,
        weights_path,
        resources_path,
        model_type,
        platform,
        blobstore_provider,
        base_image_registry=None,
        base_image_user=None,
        base_image_pass=None       
        ):
        """Kicks off a `ModelConverter` job run

        Args:
            sp_access_key_id (str): Access key for accessing cloud blob storage
            sp_secret_access_key (str): Secret access key for accessing cloud blob storage
            blobstore_container (str): Blob container storage name
            weights_path (str): Path to weights archive in blob container storage
            resource_path (str): Path to resources archive in blob container storage
            model_type (str): Type of model to be converted 
            platform (str): The model provider where the input artifacts are generated. Options: `["sagemaker", "mlflow", "azure"]`
            blobstore_provider (str): Cloud provider where model artifacts are saved. Options: `["gcp", "azure", "S3"]`
            base_image_registry (str): Only required for Azure, registry location output by prepare_azure_model()
            base_image_registry_user (str): Only required for Azure, registry username output by prepare_azure_model()
            base_image_registry_pass (str): Only required for Azure, registry password output by prepare_azure_model()

        Returns:
            converter_response (ApiObject): Raw response from `ModelConverter` with the status of the converter job, message, and http code 

        Raises:
            ApiError: A subclass of ApiError will be raised if the API returns an error status,
                or the client is unable to connect.            
        """

        converter_request = {
            "sp_access_key_id": sp_access_key_id,
            "sp_secret_access_key": sp_secret_access_key,
            "blobstore_container": blobstore_container,
            "weights_path": weights_path,
            "resource_path": resources_path,
            "model_type": model_type,
            "platform": platform,
            "blobstore_provider": blobstore_provider
        }

        if platform == "azure":
            converter_request['base_image_registry'] = base_image_registry
            converter_request['base_image_registry_user'] = base_image_user
            converter_request['base_image_registry_pass'] = base_image_pass

        converter_response = self._api_client.http.post('{}/{}'.format(self._base_route, "start"), json_data=converter_request)
        return converter_response
    
    
    def get_status(self, job_id):
        """Retrieves status of a `ModelConverter` `Job` instance.

        Args:
            job_id (str): The job identifier of a `ModelConverter` job.

        Returns:
            Status: The Status of the `ModelConverter` job.

        Raises:
            ApiError: A subclass of ApiError will be raised if the API returns an error status,
                or the client is unable to connect.
        """        

        status_raw_response = self._api_client.http.get("{}/{}?job_id={}".format(self._base_route, "get-status", job_id))

        return status_raw_response
    
    def block_until_complete(self, job_id, timeout=600, poll_interval=5):
        """Blocks until the `Job` completes or a timeout is reached.

        This is accomplished by polling the API until the `Job` status is set to `COMPLETED`
        or `FAILED`.

        Args:
            job_id (Union[str, Job, Result]): The job identifier of a `ModelConverter` `Job` instance.
            timeout (Optional[float]): Seconds to wait until timeout. `None` indicates wait forever.
                Defaults to 60.
            poll_interval (Optional[float]): Seconds between polls. Defaults to 1.

        Returns:
            Status: The completed status of the `ModelConverter` `Job` instance and the completed job's processing time.

        Raises:
            Timeout: The `Job` did not complete before the timeout was reached.
            ApiError: A subclass of ApiError will be raised if the API returns an error status,
                or the client is unable to connect.
        """
        endby = time.time() + timeout if (timeout is not None) else None
        while True:  # wait one poll at least once
            self.logger.debug("waiting... %g", poll_interval)
            time.sleep(poll_interval)
            status = self.get_status(job_id)
            self.logger.debug("job %s", job_id)
            if status["jobStatus"] not in ["BUSY", "IMAGE_CREATION", "IMPORTER_PROC","ASSERTION"]:
                return status
            if (endby is not None) and (time.time() > endby - poll_interval):
                raise Timeout('timed out before completion')
    


