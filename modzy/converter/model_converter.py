import logging
import requests
import json

CONVERTER_HOST = "127.0.0.1"
CONVERTER_PORT = "8080"


class ModelConverter:
    """The `Models` object.

    This object is used to retrieve information about models from the API.

    Note:
        This class should not be instantiated directly but rather accessed through the `converter`
        attribute of an `ApiClient` instance.
    """

    _base_route = f'http://{CONVERTER_HOST}:{CONVERTER_PORT}'

    def __init__(self, api_client):
        """Creates a `ModelConverter` instance.

        Args:
            api_client (ApiClient): An `ApiClient` instance.
        """
        self._api_client = api_client
        self.logger = logging.getLogger(__name__)

    def env_status(self):
        raw_response = self._api_client.http.get(f"{self._base_route}/env-status")
        response = raw_response["responseEntries"][0]
        response_code = int(response["httpCode"])
        response_message = response["message"]
        self.logger.info(f"Environment status returned with code {response_code}: {response_message}")
        return True if response_code == 200 else False

    def check_endpoints(
        self,
        sp_access_key_id,
        sp_secret_access_key,
        blobstore_container,
        weights_path,
        resources_path,
        model_type,
        platform,
        blobstore_provider
    ):
        converter_request = {
            "aws_key_id": sp_access_key_id,
            "aws_access_key": sp_secret_access_key,
            "s3Bucket": blobstore_container,
            "weightsPath": weights_path,
            "resourcesPath": resources_path,
            "model_type": model_type,
            "platform": platform,
            "blobStoreProvider": blobstore_provider
        }
        raw_response = requests.get(
            f"{self._base_route}/check-endpoints",
            params=converter_request
        ).json()
        response = raw_response["responseEntries"][0]
        status_code = response["httpCode"]
        message = response["message"]
        self.logger.info(f"Response received with status code {status_code}: {message}")
        return status_code == 200

    def run(
        self,
        sp_access_key_id,
        sp_secret_access_key,
        blobstore_container,
        weights_path,
        resources_path,
        model_type,
        platform,
        blobstore_provider
    ):
        converter_request = {
            "aws_key_id": sp_access_key_id,
            "aws_access_key": sp_secret_access_key,
            "s3Bucket": blobstore_container,
            "weightsPath": weights_path,
            "resourcesPath": resources_path,
            "model_type": model_type,
            "platform": platform,
            "blobStoreProvider": blobstore_provider
        }
        raw_response = requests.get(f"{self._base_route}/run", params=converter_request).json()
        response = raw_response["responseEntries"][0]
        status_code = response["httpCode"]
        message = response["message"]
        self.logger.info(f"Response received with status code {status_code}: {message}")

        # TODO: This may not be possible if status code is not 200
        if status_code == "200":
            success = raw_response["successEntry"]
            self.logger.info(f"Details: {json.dumps(success, indent=4)}")
        else:
            success = None

        return status_code, success
