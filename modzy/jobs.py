# -*- coding: utf-8 -*-
"""Classes for interacting with jobs."""

import logging
import time
from datetime import datetime
from types import SimpleNamespace
from urllib.parse import urlencode
from ._api_object import ApiObject
from ._size import human_read_to_bytes
from ._util import encode_data_uri, depth, file_to_chunks, bytes_to_chunks
from .error import Timeout
from .models import Model
from deprecation import deprecated


class Jobs:
    """The `Jobs` object.

    This object is used to retrieve information about jobs from the API.

    Note:
        This class should not be instantiated directly but rather accessed through the `jobs`
        attribute of an `ApiClient` instance.
    """

    _base_route = '/jobs'

    # is this the best place to put these?
    status = SimpleNamespace(
        SUBMITTED='SUBMITTED',
        IN_PROGRESS='IN_PROGRESS',
        COMPLETED='COMPLETED',
        CANCELED='CANCELED',
        TIMEDOUT='TIMEDOUT',
    )
    """Possible job statuses."""

    def __init__(self, api_client):
        """Creates a `Jobs` instance.

        Args:
            api_client (ApiClient): An `ApiClient` instance.
        """
        self._api_client = api_client
        self.logger = logging.getLogger(__name__)

    def get(self, job):
        """Gets a `Job` instance.

        Args:
            job (Union[str, Job, Result]): The job identifier or a `Job` or `Result` instance.

        Returns:
            Job: The `Job` instance.

        Raises:
            ApiError: A subclass of ApiError will be raised if the API returns an error status,
                or the client is unable to connect.
        """
        self.logger.debug("getting job %s", job)
        identifier = Job._coerce_identifier(job)
        json_obj = self._api_client.http.get('{}/{}'.format(self._base_route, identifier))
        return Job(json_obj, self._api_client)

    def get_history(self, user=None, access_key=None, start_date=None, end_date=None, model=None,
                    status='all', sort_by=None, direction=None, page=None, per_page=None):
        """Gets a list of `Job` instances within a set of parameters.

        Args:
            user (Optional[str]): Name of the job submitter
            access_key (Optional[str]): Identifier of the access key to be assigned to the user
            start_date (Optional[datetime, str]): initial date to filter records
            end_date (Optional[datetime, str]): final date to filter records
            model (Optional[str]): Model name or version identifier
            status (Optional[str]): Status of the jobs (all, pending, terminated)
            sort_by (Optional[str]): attribute name to sort results
            direction (Optional[str]): Direction of the sorting algorithm (asc, desc)
            page (Optional[float]): The page number for which results are being returned
            per_page (Optional[float]): The number of job identifiers returned by page

        Returns:
            List[Job]: A list of `Job` instances.
        Raises:
            ApiError: A subclass of ApiError will be raised if the API returns an error status,
                or the client is unable to connect.
        """
        if user is not None and not isinstance(user, str):
            raise TypeError("the user param should be a string")
        if access_key is not None and not isinstance(access_key, str):
            raise TypeError("the access_key param should be a string")
        if start_date is not None:
            if isinstance(start_date, datetime):
                start_date = start_date.isoformat(timespec='milliseconds')
            elif not isinstance(start_date, str):
                raise TypeError("the start_date param should be a datetime or string")
        if end_date is not None:
            if isinstance(end_date, datetime):
                end_date = end_date.isoformat(timespec='milliseconds')
            elif not isinstance(end_date, str):
                raise TypeError("the end_date param should be a datetime or string")
        if status is not None and not isinstance(status, str):
            raise TypeError("the status param should be a string")
        if model is not None and not isinstance(model, str):
            raise TypeError("the model param should be a string")
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
            "user": user,
            "accessKey": access_key,
            "startDate": start_date,
            "endDate": end_date,
            "model": model,
            "status": status,
            "sort-by": sort_by,
            "direction": direction,
            "page": page,
            "per-page": per_page
        }
        body = {k: v for (k, v) in body.items() if v is not None}
        self.logger.debug("body 2? %s", body)
        json_list = self._api_client.http.get('{}/history?{}'.format(self._base_route, urlencode(body)))
        return list(Job(json_obj, self._api_client) for json_obj in json_list)

    def cancel(self, job):
        """Attempts to cancel a `Job`.

        Args:
            job (Union[str, Job, Result]): The job identifier or a `Job` or `Result` instance.

        Returns:
            Job: The `Job` instance.

        Raises:
            ApiError: A subclass of ApiError will be raised if the API returns an error status,
                or the client is unable to connect.
        """
        identifier = Job._coerce_identifier(job)
        self.logger.debug("canceling job %s", job)
        json_obj = self._api_client.http.delete('{}/{}'.format(self._base_route, identifier))
        return Job(json_obj, self._api_client)

    def block_until_complete(self, job, timeout=60, poll_interval=5):
        """Blocks until the `Job` completes or a timeout is reached.

        This is accomplished by polling the API until the `Job` status is set to `COMPLETED`
        or `CANCELED`.

        Args:
            job (Union[str, Job, Result]): The job identifier or a `Job` or `Result` instance.
            timeout (Optional[float]): Seconds to wait until timeout. `None` indicates wait forever.
                Defaults to 60.
            poll_interval (Optional[float]): Seconds between polls. Defaults to 1.

        Returns:
            Job: The `Job` instance.

        Raises:
            Timeout: The `Job` did not complete before the timeout was reached.
            ApiError: A subclass of ApiError will be raised if the API returns an error status,
                or the client is unable to connect.
        """
        identifier = Job._coerce_identifier(job)
        endby = time.time() + timeout if (timeout is not None) else None
        while True:  # wait one poll at least once
            self.logger.debug("waiting... %g", poll_interval)
            time.sleep(poll_interval)
            job = self.get(identifier)
            self.logger.debug("job %s", job)
            if job.status not in (Jobs.status.SUBMITTED, Jobs.status.IN_PROGRESS):
                return job
            if (endby is not None) and (time.time() > endby - poll_interval):
                raise Timeout('timed out before completion')
        # TODO: should probably ramp up poll_interval as wait time increases

    def __fix_single_source_job(self, sources):
        """Compatibility function to check and fix the sources parameter if is a single source dict

        Args:
            sources (dict): a single of double source dict

        Returns:
            dict: a properly formatted sources dictionary

        """
        dict_levels = depth(sources)
        if dict_levels == 1:
            return {'job': sources}
        else:
            return sources

    def submit_text(self, model, version, sources, explain=False):
        """Submits text data for a multiple source `Job`.

        Args:
            model (Union[str, Model]): The model identifier or a `Model` instance.
            version (str): The model version string.
            sources (dict): A mapping of source names to text sources. Each source should be a
                mapping of model input filename to text string.
            explain (bool): indicates if you desire an explainable result for your model.`

        Returns:
            Job: The submitted `Job` instance.

        Raises:
            ApiError: A subclass of ApiError will be raised if the API returns an error status,
                or the client is unable to connect.

            Example:
                .. code-block::

                    job = client.jobs.submit_text_bulk('model-identifier', '1.2.3',
                    {
                        'source-name-1': {
                            'model-input-name-1': 'some text',
                            'model-input-name-2': 'some more text',
                        },
                        'source-name-2': {
                            'model-input-name-1': 'some text 2',
                            'model-input-name-2': 'some more text 2',
                        }
                    })
        """
        identifier = Model._coerce_identifier(model)
        version = str(version)
        body = {
            "model": {
                "identifier": identifier,
                "version": version
            },
            "explain": explain,
            "input": {
                "type": "text",
                "sources": self.__fix_single_source_job(sources)
            }
        }
        response = self._api_client.http.post(self._base_route, body)
        return Job(response, self._api_client)

    @deprecated(deprecated_in="0.5.6", removed_in="1.0", details="Use jobs.submit_text function instead")
    def submit_text_bulk(self, model, version, sources, explain=False):
        return self.submit_text(model, version, sources, explain)

    def submit_embedded(self, model, version, sources, explain=False):
        """Submits embedded data for a multiple source `Job`.

        Args:
            model (Union[str, Model]): The model identifier or a `Model` instance.
            version (str): The model version string.
            sources (dict): A mapping of source names to text sources. Each source should be a
                mapping of model input filename to bytes-like object.
            explain (bool): indicates if you desire an explainable result for your model.`

        Returns:
            Job: The submitted `Job` instance.

        Raises:
            ApiError: A subclass of ApiError will be raised if the API returns an error status,
                or the client is unable to connect.

            Example:
                .. code-block::

                    job = client.jobs.submit_bytes_bulk('model-identifier', '1.2.3',
                    {
                        'source-name-1': {
                            'model-input-name-1': b'some bytes',
                            'model-input-name-2': bytearray([1,2,3,4]),
                        },
                        'source-name-2': {
                            'model-input-name-1': b'some bytes',
                            'model-input-name-2': bytearray([1,2,3,4]),
                        }
                    })
        """
        identifier = Model._coerce_identifier(model)
        version = str(version)
        sources = {
            source: {
                key: encode_data_uri(value)
                for key, value in inputs.items()
            }
            for source, inputs in sources.items()
        }

        body = {
            "model": {
                "identifier": identifier,
                "version": version
            },
            "explain": explain,
            "input": {
                "type": "embedded",
                "sources": self.__fix_single_source_job(sources)
            }
        }

        response = self._api_client.http.post(self._base_route, body)
        return Job(response, self._api_client)

    @deprecated(deprecated_in="0.5.6", removed_in="1.0", details="Use jobs.submit_embedded function instead")
    def submit_bytes(self, model, version, source, explain=False, source_name='job'):
        return self.submit_embedded(model, version, source, explain)

    @deprecated(deprecated_in="0.5.6", removed_in="1.0", details="Use jobs.submit_embedded function instead")
    def submit_bytes_bulk(self, model, version, sources, explain=False):
        return self.submit_embedded(model, version, sources, explain)

    def submit_file(self, model, version, sources, explain=False):
        """Submits filepath or file-like data data for a multiple source `Job`.

                Args:
                    model (Union[str, Model]): The model identifier or a `Model` instance.
                    version (str): The model version string.
                    sources (dict): A mapping of source names to text sources. Each source should be a
                        mapping of model input filename to filepath or file-like object.
                    explain (bool): indicates if you desire an explainable result for your model.`

                Returns:
                    Job: The submitted `Job` instance.

                Raises:
                    ApiError: A subclass of ApiError will be raised if the API returns an error status,
                        or the client is unable to connect.

                    Example:
                        .. code-block::

                            job = client.jobs.submit_files_bulk('model-identifier', '1.2.3',
                            {
                                'source-name-1': {
                                    'model-input-name-1': '/path/to/file.dat',
                                    'model-input-name-2': pathlib.Path('./path/to/file.dat'),
                                },
                                'source-name-2': {
                                    'model-input-name-1': open('/path/to/file.dat', 'rb'),
                                    'model-input-name-2': io.BytesIO(b'file-like object'),
                                }
                            })
                """
        identifier = Model._coerce_identifier(model)
        version = str(version)
        body = {
            "model": {
                "identifier": identifier,
                "version": version
            },
            "explain": explain
        }
        # Open the job with an empty call to the job api
        open_job = Job(self._api_client.http.post(self._base_route, body), self._api_client)
        self.logger.debug("open job %s", open_job)
        chunk_size = None
        try:
            job_features = self.get_features()
            chunk_size = human_read_to_bytes(job_features["input_chunk_maximum_size"])
        except:
            self.logger.warning("Error getting features, assuming defaults")
            chunk_size = 1024 * 1024

        try:
            # Iterate on the sources, submitting each input as a multipart post request
            # jobIdentifier/input-item-name/model-input-name
            for source, inputs in self.__fix_single_source_job(sources).items():
                for key, value in inputs.items():
                    self.__append_input(open_job, source, key, value, chunk_size)

            open_job = self._api_client.http.post('{}/{}/close'.format(self._base_route, open_job.job_identifier))
            self.logger.debug("close job %s", open_job)
        except:
            try:
                # Try to cancel the job as something unexpected happened, ignore any error if something bad happen
                # with this call in order to pass the real cause to the caller
                self.logger.debug("canceling job %s", open_job)
                open_job.cancel()
            finally:
                pass
            raise
        return Job(open_job, self._api_client)

    @deprecated(deprecated_in="0.5.6", removed_in="1.0", details="Use jobs.submit_file function instead")
    def submit_files(self, model, version, source, explain=False, source_name='job'):
        sources = {source_name: source}
        return self.submit_file(model, version, sources, explain)

    @deprecated(deprecated_in="0.5.6", removed_in="1.0", details="Use jobs.submit_file function instead")
    def submit_files_bulk(self, model, version, sources, explain=False):
        return self.submit_file(model, version, sources, explain)

    def __append_input(self, job, input_item_name, data_item_name, input_value, chunk_size):
        iterable = None
        if isinstance(input_value, (bytes, bytearray)):
            iterable = bytes_to_chunks(input_value, chunk_size)
        else:
            iterable = file_to_chunks(input_value, chunk_size)

        for i, chunk in enumerate(iterable):
            self.logger.debug("__append_input(%s, %s, %s, %s, %s) chunk %i", job.job_identifier, input_item_name,
                              data_item_name, type(input_value), chunk_size, i)
            self._api_client.http.post(
                '{}/{}/{}/{}'.format(self._base_route, job.job_identifier, input_item_name, data_item_name),
                None,
                {"input": chunk}
            )

    def submit_aws_s3(self, model, version, sources, access_key_id, secret_access_key, region, explain=False):
        """Submits AwS S3 hosted data for a multiple source `Job`.

        Args:
            model (Union[str, Model]): The model identifier or a `Model` instance.
            version (str): The model version string.
            sources (dict): A mapping of source names to text sources. Each source should be a
                mapping of model input filename to S3 bucket and key.
            access_key_id (str): The AWS Access Key ID.
            secret_access_key (str): The AWS Secret Access Key.
            region (str): The AWS Region.
            explain (bool): indicates if you desire an explainable result for your model.`

        Returns:
            Job: The submitted `Job` instance.

        Raises:
            ApiError: A subclass of ApiError will be raised if the API returns an error status,
                or the client is unable to connect.

            Example:
                .. code-block::

                    job = client.jobs.submit_aws_s3('model-identifier', '1.2.3',
                    {
                        'source-name-1': {
                            'model-input-name-1': {
                                'bucket': 'my-bucket',
                                'key': '/my/data/file-1.dat'
                            },
                            'model-input-name-2': {
                                'bucket': 'my-bucket',
                                'key': '/my/data/file-2.dat'
                            }
                        },
                        'source-name-2': {
                            'model-input-name-1': {
                                'bucket': 'my-bucket',
                                'key': '/my/data/file-3.dat'
                            },
                            'model-input-name-2': {
                                'bucket': 'my-bucket',
                                'key': '/my/data/file-4.dat'
                            }
                        }
                    },
                        access_key_id='AWS_ACCESS_KEY_ID',
                        secret_access_key='AWS_SECRET_ACCESS_KEY',
                        region='us-east-1',
                    )
        """
        identifier = Model._coerce_identifier(model)
        version = str(version)
        access_key_id = str(access_key_id)
        region = str(region)

        body = {
            "model": {
                "identifier": identifier,
                "version": version
            },
            "explain": explain,
            "input": {
                "type": "aws-s3",
                "accessKeyID": access_key_id,
                "secretAccessKey": secret_access_key,
                "region": region,
                "sources": self.__fix_single_source_job(sources)
            }
        }

        response = self._api_client.http.post(self._base_route, body)
        return Job(response, self._api_client)

    @deprecated(deprecated_in="0.5.6", removed_in="1.0", details="Use jobs.submit_aws_s3 function instead")
    def submit_aws_s3_bulk(self, model, version, sources, access_key_id, secret_access_key, region, explain=False):
        return self.submit_aws_s3(model, version, sources, access_key_id, secret_access_key, region, explain)

    def submit_jdbc(self, model, version, url, username, password, driver, query, explain=False):
        """Submits jdbc query as input for a `Job`, each row is interpreted as a input.
            Modzy will create a data source with the parameters provided and will execute
            the query provided, then will match the inputs defined of the model with the columns
            of the resultset.

        Args:
            model (Union[str, Model]): The model identifier or a `Model` instance.
            version (str): The model version string.
            url (str): URL to connect to the database
            username (str): the username to access the database
            password (str): the password to access the database
            driver (str): full driver class name
            query (str): the query to execute
            explain (bool): indicates if you desire an explainable result for your model.`

        Returns:
            Job: The submitted `Job` instance.

        Raises:
            ApiError: A subclass of ApiError will be raised if the API returns an error status,
                or the client is unable to connect.

            Example:
                .. code-block::

                    job = client.jobs.submit_jdbc(
                        'model-identifier',
                        '1.2.3',
                        'jdbc:postgresql://database-host:5432/mydatabase',
                        'username',
                        'password',
                        'org.postgresql.Driver',
                        'select description as \'input.txt\' from my-table'
                    )
        """
        identifier = Model._coerce_identifier(model)
        version = str(version)
        url = str(url)
        username = str(username)
        password = str(password)
        driver = str(driver)
        query = str(query)

        body = {
            "model": {
                "identifier": identifier,
                "version": version
            },
            "explain": explain,
            "input": {
                "type": "jdbc",
                "url": url,
                "username": username,
                "password": password,
                "driver": driver,
                "query": query
            }
        }

        response = self._api_client.http.post(self._base_route, body)
        return Job(response, self._api_client)

    def get_features(self):
        """Gets the `Job` features

        Returns:
            ApiObject: a generic api object with the feature name as keys.

        Raises:
            ApiError: A subclass of ApiError will be raised if the API returns an error status,
                or the client is unable to connect.
        """
        self.logger.debug("getting features ")

        json_obj = self._api_client.http.get('{}/features'.format(self._base_route))
        return ApiObject(json_obj, self._api_client)


class Job(ApiObject):
    """A job object.

    This object contains a parsed copy of the information returned from the server about a certain job.

    Attributes:
        job_identifier (str): The job identifier.

    Note:
        This class should not be instantiated directly. Instead, it is returned by various package
        functions.

        This object is a `dict` subclass that also supports attribute access. Information can be
        accessed through dotted attribute notation using "snake_case" or the original "camelCase" JSON
        key name (``job.job_identifier`` or ``job.jobIdentifier``). Alternatively, the original
        "camelCase" JSON key can be used with bracketed key access notation (``job['jobIdentifier']``).
    """

    def __init__(self, json_obj, api_client=None):
        if 'status' not in json_obj:
            json_obj['status'] = Jobs.status.SUBMITTED
        super().__init__(json_obj, api_client)

    @classmethod
    def _coerce_identifier(cls, maybe_job):
        identifier = getattr(maybe_job, 'job_identifier', maybe_job)
        if not isinstance(identifier, str):
            raise TypeError('the identifier must be {} or str, not {}'
                            .format(cls.__name__, type(maybe_job).__name__))
        return identifier

    def sync(self):
        """Updates the `Job` instance's data in-place with new data from the API.

        Returns:
            Job: The `Job` instance (self).

        Raises:
            ApiError: A subclass of ApiError will be raised if the API returns an error status,
                or the client is unable to connect.
        """
        updated = self._api_client.jobs.get(self.job_identifier)
        self.update(updated)  # is updating in place a bad idea?
        return self

    def cancel(self):
        """Attempts to cancel the `Job`.

        Returns:
            Job: The `Job` instance (self).

        Raises:
            ApiError: A subclass of ApiError will be raised if the API returns an error status,
                or the client is unable to connect.
        """
        updated = self._api_client.jobs.cancel(self.job_identifier)
        self.update(updated)  # is updating in place a bad idea?
        return self

    def get_result(self):
        """Gets the `Result` instance for this `Job`.

        Returns:
            Result: The `Result` instance.

        Raises:
            ApiError: A subclass of ApiError will be raised if the API returns an error status,
                or the client is unable to connect.
        """
        return self._api_client.results.get(self.job_identifier)

    def block_until_complete(self, timeout=60, poll_interval=5):
        """Blocks until the `Job` completes or a timeout is reached.

        This is accomplished by polling the API until the `Job` status is set to `COMPLETED`
        or `CANCELED`.

        Args:
            timeout (Optional[float]): Seconds to wait until timeout. `None` indicates wait forever.
                Defaults to 60.
            poll_interval (Optional[float]): Seconds between polls. Defaults to 1.

        Returns:
            Job: The `Job` instance (self).

        Raises:
            Timeout: The `Job` did not complete before the timeout was reached.
            ApiError: A subclass of ApiError will be raised if the API returns an error status,
                or the client is unable to connect.
        """
        if self.status not in (Jobs.status.SUBMITTED, Jobs.status.IN_PROGRESS):
            return self

        updated = self._api_client.jobs.block_until_complete(self.job_identifier,
                                                             poll_interval=poll_interval, timeout=timeout)
        self.update(updated)  # is updating in place a bad idea?
        return self

    def __str__(self):
        return "Job(job_identifier='{}',status='{}')".format(self.job_identifier, self.status)
