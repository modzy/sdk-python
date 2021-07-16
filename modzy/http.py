# -*- coding: utf-8 -*-
"""The HTTP client implementation."""

import json
import logging
from urllib.parse import urlparse

import requests

from ._api_object import ApiObject
from .error import NetworkError, _create_response_error


def _url_is_absolute(url):
    return bool(urlparse(url).netloc)


def _urlappend(base, url):
    if _url_is_absolute(url):
        return url
    if not base.endswith('/'):
        base = base + '/'
    return base + url.lstrip('/')


class HttpClient:
    """The HTTP Client object.

    This object is responsible for making the actual HTTP requests to the API. User code
    should generally not need to directly access this object.

    This class should not be instantiated directly but rather accessed through the `http`
    attribute of an `ApiClient` instance.

    Attributes:
        session (requests.Session): The requests `Session` used to make HTTP requests.
    """

    def __init__(self, api_client, session=None):
        """Creates an `HttpClient` instance.

        Args:
            api_client (ApiClient): An `ApiClient` instance.
            session (Optional[requests.Session]): A requests `Session` used to make HTTP requests.
                If None is specified one will be created. Defaults to None.
        """
        self._api_client = api_client
        self.session = session if session is not None else requests.Session()
        self.logger = logging.getLogger(__name__)

    def request(self, method, url, json_data=None, file_data=None):
        """Sends an HTTP request.

        The client's API key will automatically be used for authentication.

        Args:
            method (str): The HTTP method for the request.
            url (str): URL to request.
            json_data (Optional[Any]): JSON serializeable object to include in the request body.
            file_data (Optional[Any]): Dictionary to be submitted as files part of the request

        Returns:
            dict: JSON object deserialized from the response body.

        Raises:
            ApiError: A subclass of ApiError will be raised if the API returns an error status,
                or the client is unable to connect.
        """

        url = _urlappend(self._api_client.base_url, url)

        if json_data:
            data = json.dumps(json_data).encode('utf-8')
        else:
            data = None

        headers = {'Accept': 'application/json'}
        if self._api_client.api_key:  # will there be any endpoints that don't need an api key?
            headers['Authorization'] = 'ApiKey {}'.format(self._api_client.api_key)
        if json_data is not None:
            headers['Content-Type'] = 'application/json'
        self.logger.debug("%s: %s - [%s]", method, url, self._api_client.cert)

        try:
            response = self.session.request(method, url, data=data, headers=headers, files=file_data, verify=self._api_client.cert)
            self.logger.debug("response %s - length %s", response.status_code, len(response.content))
        except requests.exceptions.RequestException as ex:
            self.logger.exception('unable to make network request')
            raise NetworkError(str(ex), url, reason=ex)

        try:
            json_data = json.loads(response.content.decode('utf-8'), object_hook=ApiObject)
        except ValueError:
            if len(response.content) > 0:
                json_data = None
            else:
                json_data = {}

        if not (200 <= response.status_code < 300):
            message = None
            if hasattr(json_data, 'get'):
                message = json_data.get('message')
            if not message:
                message = 'HTTP Error {}: {}'.format(response.status_code, response.reason)
            raise _create_response_error(str(message), url, response)

        if json_data is None:
            # will our API *always* return JSON? may change in future
            # do we need a different Exception class for malformed body?
            raise _create_response_error('API did not return valid JSON.', url, response)

        return json_data

    def get(self, url):
        """Sends a GET request.

        Args:
            url (str): URL to request.

        Returns:
            dict: JSON object.

        Raises:
            ApiError: A subclass of ApiError will be raised if the API returns an error status,
                or the client is unable to connect.
        """
        return self.request('GET', url)

    def post(self, url, json_data=None, file_data=None):
        """Sends a POST request.

        Args:
            url (str): URL to request.
            json_data (Optional[dict]): JSON to include in the request body.

        Returns:
            dict: JSON object.

        Raises:
            ApiError: A subclass of ApiError will be raised if the API returns an error status,
                or the client is unable to connect.
        """
        return self.request('POST', url, json_data=json_data, file_data=file_data)

    def patch(self, url, json_data=None):
        """Sends a PATCH request.

        Args:
            url (str): URL to request.
            json_data (Optional[dict]): JSON to include in the request body.

        Returns:
            dict: JSON object.

        Raises:
            ApiError: A subclass of ApiError will be raised if the API returns an error status,
                or the client is unable to connect.
        """
        return self.request('PATCH', url, json_data=json_data)

    def put(self, url, json_data=None):
        """Sends a PUT request.

        Args:
            url (str): URL to request.
            json_data (Optional[dict]): JSON to include in the request body.

        Returns:
            dict: JSON object.

        Raises:
            ApiError: A subclass of ApiError will be raised if the API returns an error status,
                or the client is unable to connect.
        """
        return self.request('PUT', url, json_data=json_data)

    def delete(self, url, json_data=None):
        """Sends a DELETE request.

        Args:
            url (str): URL to request.
            json_data (Optional[dict]): JSON to include in the request body.

        Returns:
            dict: JSON object.

        Raises:
            ApiError: A subclass of ApiError will be raised if the API returns an error status,
                or the client is unable to connect.
        """
        return self.request('DELETE', url, json_data=json_data)
