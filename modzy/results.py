# -*- coding: utf-8 -*-
"""Classes for interacting with results."""

import logging
import time

from ._api_object import ApiObject
from .error import NotFoundError, ResultsError, Timeout


class Results:
    """The `Results` object.

    This object is used to retreive information about results from the API.

    Note:
        This class should not be instantiated directly but rather accessed through the `results`
        attribute of an `ApiClient` instance.
    """

    _base_route = '/results'

    def __init__(self, api_client):
        """Creates a `Results` instance.

        Args:
            api_client (ApiClient): An `ApiClient` instance.
        """
        self._api_client = api_client
        self.logger = logging.getLogger(__name__)

    def get(self, result):
        """Gets a `Result` instance.

        Args:
            job (Union[str, Job, Result]): The job identifier or a `Job` or a `Job` or `Result` instance.

        Returns:
            Result: The `Result` instance.

        Raises:
            ApiError: A subclass of ApiError will be raised if the API returns an error status,
                or the client is unable to connect.
        """
        identifier = Result._coerce_identifier(result)
        self.logger.debug("getting results %s", result)
        json_obj = self._api_client.http.get('{}/{}'.format(self._base_route, identifier))
        return Result(json_obj, self._api_client)

    def block_until_complete(self, result, timeout=60, poll_interval=5):
        """Blocks until the `Result` completes or a timeout is reached.

        This is accomplished by polling the API until the `Result` is marked finished. This may mean
        that the underlying `Job` was completed or canceled.

        Args:
            job (Union[str, Job, Result]): The job identifier or a `Job` or a `Job` or `Result` instance.
            timeout (Optional[float]): Seconds to wait until timeout. `None` indicates wait forever.
                Defaults to 60.
            poll_interval (Optional[float]): Seconds between polls. Defaults to 1.

        Returns:
            Result: The `Result` instance.

        Raises:
            Timeout: The `Result` did not complete before the timeout was reached.
            ApiError: A subclass of ApiError will be raised if the API returns an error status,
                or the client is unable to connect.
        """
        identifier = Result._coerce_identifier(result)
        endby = time.time() + timeout if (timeout is not None) else None
        ignore404 = False
        while True:  # poll at least once
            try:
                result = self.get(identifier)
                self.logger.debug("result %s", result)
            except NotFoundError:
                # work around 404 for recently accepted jobs
                if not ignore404:
                    self._api_client.jobs.get(identifier)  # this didn't error so job must exist
                    # TODO: short-circuit on job cancelation
                    ignore404 = True
            else:
                if result.finished:  # this covers CANCELED/COMPLETED
                    return result
            if (endby is not None) and (time.time() > endby - poll_interval):
                raise Timeout('timed out before completion')
            self.logger.debug("waiting... %d", poll_interval)
            time.sleep(poll_interval)
        # TODO: should probably ramp up poll_interval as wait time increases


class Result(ApiObject):
    """A result object.

    This object contains a parsed copy of the information returned from the server about a certain result.

    Attributes:
        job_identifier (str): The job identifier.

    Note:
        This class should not be instantiated directly. Instead, it is returned by various package
        functions.

        This object is a `dict` subclass that also supports attribute access. Information can be
        accessed through dotted attribute notation using "snake_case" or the original "camelCase" JSON
        key name (``result.job_identifier`` or ``result.jobIdentifier``). Alternatively, the original
        "camelCase" JSON key can be used with bracketed key access notation (``result['jobIdentifier']``).
    """

    @classmethod
    def _coerce_identifier(cls, maybe_result):
        identifier = getattr(maybe_result, 'job_identifier', maybe_result)
        if not isinstance(identifier, str):
            raise TypeError('the identifier must be {} or str, not {}'
                            .format(cls.__name__, type(maybe_result).__name__))
        return identifier

    def sync(self):
        """Updates the `Result` instance's data in-place with new data from the API.

        Returns:
            Result: The `Result` instance (self).

        Raises:
            ApiError: A subclass of ApiError will be raised if the API returns an error status,
                or the client is unable to connect.
        """
        updated = self._api_client.results.get(self.job_identifier)
        self.update(updated)  # is updating in place a bad idea?
        return self

    def block_until_complete(self, timeout=60, poll_interval=5):
        """Block until the `Result` completes or a timeout is reached.

        This is accomplished by polling the API until the `Result` is marked finished. This may mean
        that the underlying `Job` was completed or canceled.

        Args:
            timeout (Optional[float]): Seconds to wait until timeout. `None` indicates wait forever.
                Defaults to 60.
            poll_interval (Optional[float]): Seconds between polls. Defaults to 1.

        Returns:
            Result: The `Result` instance (self).

        Raises:
            Timeout: The `Result` did not complete before the timeout was reached.
            ApiError: A subclass of ApiError will be raised if the API returns an error status,
                or the client is unable to connect.
        """
        # once we can tell if a source exists or not vs isn't finished from the results API
        # we should provide a way to block until a specific source finishes
        if self.finished:
            return self

        updated = self._api_client.results.block_until_complete(self.job_identifier,
                                                                poll_interval=poll_interval, timeout=timeout)
        self.update(updated)  # is updating in place a bad idea?
        return self

    def get_source_outputs(self, source_name):
        """Gets the model outputs for a given source.

        Args:
            source_name (str): The source name.

        Returns:
            dict: A `dict` mapping the output's filenames to JSON parsed data.

        Raises:
            ResultsError: The results for this source indicate a model failure.
            KeyError: The source name was not found.
        """
        try:
            source = self.results[source_name]
            if source_name in source:  # deal with legacy double nesting of source source_name
                source = source[source_name]
            return source
        except (KeyError, AttributeError):
            pass

        try:
            source = self.failures[source_name]
            if source_name in source:  # deal with legacy double nesting of source source_name
                source = source[source_name]
            raise ResultsError(source.error)
        except (KeyError, AttributeError):
            pass

        # TODO: can we give a better error message if job canceled?
        raise KeyError(source_name)

    def get_first_outputs(self):
        """Gets the first or only outputs found in this result.

        This is useful for retrieving the outputs after submitting a job with only a single
        input source where you do not know or care about the source name. For example::

            job = client.jobs.submit_files('my-model', '1.0.0', {'input': './my-file.dat'})
            result = client.results.block_until_complete(job)
            outputs = result.get_first_outputs()
            output_data = outputs['output-file.dat']

        Args:
            source_name (str): The source name.

        Returns:
            dict: A `dict` mapping the output's filenames to JSON parsed data.

        Raises:
            ResultsError: The results for this source indicate a model failure.
            KeyError: No sources have completed.
        """
        source_name = self._get_first_source_name()
        return self.get_source_outputs(source_name)

    def _get_first_source_name(self):
        try:
            return next(iter(self.results))
        except (StopIteration, AttributeError):
            pass

        try:
            return next(iter(self.failures))
        except (StopIteration, AttributeError):
            pass

        # TODO: can we give a better error message if job canceled?
        raise KeyError('no source outputs available, wait for job to complete')

    def __str__(self):
        return "Result(job_identifier='{}',finished='{}')".format(self.job_identifier, self.finished)
