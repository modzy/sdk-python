# -*- coding: utf-8 -*-
"""The API client implementation."""
from .error import NetworkError
from .http import HttpClient
from .jobs import Jobs
from .models import Models
from .results import Results
from .tags import Tags
import logging


class ApiClient:
    """The API client object.

    This class is used to interact with the Modzy API.

    The API models, jobs, and results can be accessed using the :py:attr:`models`,
    :py:attr:`jobs` and :py:attr:`results` attributes::

        client = ApiClient(base_url='https://path/to/api', api_key='my-api-key')
        model = client.models.get('my-model')
        job = client.jobs.submit_files('my-model', '1.0.0', {'input': './my-file.dat'})
        result = client.results.block_until_complete(job)

    Attributes:
        base_url (str): The base url for the API.
        api_key (str): The API key used for authentication.
        http (HttpClient): `HttpClient` object used for making direct HTTP calls.
        models (Models): `Models` object used to interact with models.
        jobs (Jobs): `Jobs` object used to interact with jobs.
        results (Results): `Results` object used to interact with results.
    """

    def __init__(self, base_url, api_key, cert=None):
        """Creates an `ApiClient` instance.

        Args:
            base_url (str): The base url for the API.
            api_key (str): The API key to use for authentication.
            certs (str): A tuple to use custom cert and key, i.e.: (cert_file_path, key_file_path)
        """
        self.logger = logging.getLogger(__name__)
        self.base_url = base_url
        self.api_key = api_key
        self.cert = cert

        self.http = HttpClient(self)
        self.check_client()

        self.models = Models(self)
        self.jobs = Jobs(self)
        self.results = Results(self)
        self.tags = Tags(self)

    def check_client(self):
        self.logger.debug("Checking base_url %s", self.base_url)
        if self.base_url is None or self.base_url == "":
            raise ValueError("Cannot initialize the modzy client: the base_url param should be a valid not empty string")
        if self.api_key is None or self.api_key == "":
            raise ValueError("Cannot initialize the modzy client: the api_key param should be a valid not empty string")
        req_check = False
        try:
            self.http.get('/models')
            req_check = True
        except Exception as e:
            if not self.base_url.endswith('api') and not self.base_url.endswith('api/'):
                self.base_url = self.base_url + ("" if self.base_url.endswith("/") else "/") + "api/"
                # Try again with the new URL
                self.check_client()
                req_check = True

        if not req_check:
            raise ValueError("Cannot initialize the modzy client: the base_url param should point to a valid API "
                             "endpoint and the api_key should be a valid key for the env")

