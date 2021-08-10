# -*- coding: utf-8 -*-
"""The API client implementation."""

from .http import HttpClient
from .jobs import Jobs
from .models import Models
from .results import Results
from .tags import Tags


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
        if base_url is None or base_url == "":
            raise ValueError("Cannot initialize the modzy client: the base_url param should be a valid not empty string")
        if api_key is None or api_key == "":
            raise ValueError("Cannot initialize the modzy client: the api_key param should be a valid not empty string")
        self.base_url = base_url
        self.api_key = api_key
        self.cert = cert

        self.http = HttpClient(self)
        
        self.models = Models(self)
        self.jobs = Jobs(self)
        self.results = Results(self)
        self.tags = Tags(self)
