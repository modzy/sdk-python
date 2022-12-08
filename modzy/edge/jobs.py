import logging
import time

from google.protobuf.json_format import MessageToDict
# NOTE: The following import line does work when the program runs
# even though IntelliJ says it can't find "Struct" in the package.
# This is due to the way that the Python files are generated from
# the proto file in Protobuf 3.20.x+.
from google.protobuf.struct_pb2 import Struct
from grpc import Channel
from grpc._channel import _InactiveRpcError

from .proto.common.v1.common_pb2 import ModelIdentifier
from .proto.jobs.v1.jobs_pb2 import JobFilter, JobIdentifier, JobInput, JobSubmission
from .proto.jobs.v1.jobs_pb2_grpc import JobServiceStub
from .proto.results.v1.results_pb2_grpc import ResultsServiceStub
from .._util import depth, encode_data_uri
from ..error import ApiError, Timeout


def _fix_single_source_job(sources, s3=False):
    """Compatibility function to check and fix the sources parameter if is a single source dict

    Args:
        sources (dict): a single of double source dict

    Returns:
        dict: a properly formatted sources dictionary

    """
    dict_levels = depth(sources)
    if dict_levels == (1 + s3):
        return {'job': sources}
    else:
        return sources


def _parse_inactive_rpc_error(inactive_rpc_error):
    """Parse relevant info from _InactiveRpcError.

    Args:
        inactive_rpc_error (_InactiveRpcError): Error to be parsed.

    Returns:
        str: the error string.

    """
    lines = str(inactive_rpc_error).splitlines()
    details_index = [lines.index(l) for l in lines if l.startswith('\tdetails')][0]
    details_message = lines[details_index].split('=')[1].strip().replace('"', '')

    return details_message


class EdgeJobsClient:

    def __init__(self, channel: Channel, origin=""):
        self.logger = logging.getLogger(__name__)
        self.origin = origin
        self._channel = channel
        self._jobs_client = JobServiceStub(self._channel)
        self._results_client = ResultsServiceStub(self._channel)

    def submit_embedded(self, identifier, version, sources, explain=False):
        """Submits a job containing embedded data.

        Args:
            identifier (str): The model identifier.
            version (str): The model version string.
            sources (dict): A mapping of source names to text sources. Each source should be a
                mapping of model input filename to filepath or file-like object.
            explain (bool): indicates if you desire an explainable result for your model.`

        Returns:
            str: Job identifier returned by Modzy Edge.

        Raises:
            ApiError: An ApiError will be raised if the API returns an error status,
                or the client is unable to connect.

            Example:
                .. code-block::

                    job = client.submit_embedded('model-identifier', '1.2.3',
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

        sources = {
            source: {
                key: encode_data_uri(value)
                for key, value in inputs.items()
            }
            for source, inputs in _fix_single_source_job(sources).items()
        }

        sources_struct = Struct()
        for k, v in sources.items():
            sources_struct[k] = v

        job_input = JobInput(type="embedded", sources=sources_struct)
        model_identifier = ModelIdentifier(identifier=identifier, version=version)
        job_submission = JobSubmission(model=model_identifier, input=job_input, explain=explain)

        try:
            job_receipt = self._jobs_client.SubmitJob(job_submission)
        except _InactiveRpcError as e:
            raise ApiError(_parse_inactive_rpc_error(e), self.origin) from e

        return job_receipt.job_identifier

    def submit_text(self, identifier, version, sources, explain=False):
        """Submits text data for a multiple source `Job`.

        Args:
            identifier (str): The model identifier.
            version (str): The model version string.
            sources (dict): A mapping of source names to text sources. Each source should be a
                mapping of model input filename to filepath or file-like object.
            explain (bool): indicates if you desire an explainable result for your model.`

        Returns:
            str: Job identifier returned by Modzy Edge.

        Raises:
            ApiError: An ApiError will be raised if the API returns an error status,
                or the client is unable to connect.

            Example:
                .. code-block::

                    job = client.submit_text('model-identifier', '1.2.3',
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
        sources_struct = Struct()
        for k, v in _fix_single_source_job(sources).items():
            sources_struct[k] = v

        job_input = JobInput(type="text", sources=sources_struct)
        model_identifier = ModelIdentifier(identifier=identifier, version=version)
        job_submission = JobSubmission(model=model_identifier, input=job_input, explain=explain)

        try:
            job_receipt = self._jobs_client.SubmitJob(job_submission)
        except _InactiveRpcError as e:
            raise ApiError(_parse_inactive_rpc_error(e), self.origin) from e

        return job_receipt.job_identifier

    def submit_aws_s3(self, identifier, version, sources, access_key_id, secret_access_key, region, explain=False):
        """Submits AwS S3 hosted data for a multiple source `Job`.

        Args:
            identifier (str): The model identifier or a `Model` instance.
            version (str): The model version string.
            sources (dict): A mapping of source names to text sources. Each source should be a
                mapping of model input filename to S3 bucket and key.
            access_key_id (str): The AWS Access Key ID.
            secret_access_key (str): The AWS Secret Access Key.
            region (str): The AWS Region.
            explain (bool): indicates if you desire an explainable result for your model.`

        Returns:
            str: Job identifier returned by Modzy Edge.

        Raises:
            ApiError: An ApiError will be raised if the API returns an error status,
                or the client is unable to connect.

            Example:
                .. code-block::

                    job = client.submit_aws_s3('model-identifier', '1.2.3',
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
        sources_struct = Struct()
        for k, v in _fix_single_source_job(sources, s3=True).items():
            sources_struct[k] = v

        job_input = JobInput(type="aws-s3", accessKeyID=access_key_id, secretAccessKey=secret_access_key,
                             region=region, sources=sources_struct)

        model_identifier = ModelIdentifier(identifier=identifier, version=version)
        job_submission = JobSubmission(model=model_identifier, input=job_input, explain=explain)

        try:
            job_receipt = self._jobs_client.SubmitJob(job_submission)
        except _InactiveRpcError as e:
            raise ApiError(_parse_inactive_rpc_error(e), self.origin) from e

        return job_receipt.job_identifier

    def get_job_details(self, job_identifier):
        """Get job details.

        Args:
            job_identifier (str): The job identifier.

        Returns:
            dict: Details for requested job.

        Raises:
            ApiError: An ApiError will be raised if the API returns an error status,
                or the client is unable to connect.
        """
        job_identifier = JobIdentifier(identifier=job_identifier)

        try:
            job_details = self._jobs_client.GetJob(job_identifier)
        except _InactiveRpcError as e:
            raise ApiError(_parse_inactive_rpc_error(e), self.origin) from e

        return MessageToDict(job_details)

    def get_all_job_details(self, timeout=None):
        """Get job details for all jobs.

        Args:
            timeout (int): Optional timeout value in seconds.

        Returns:
            dict: Details for all jobs that have been run.

        Raises:
            ApiError: An ApiError will be raised if the API returns an error status,
                or the client is unable to connect.
        """
        try:
            all_job_details = self._jobs_client.GetJobs(JobFilter(), timeout=timeout)
        except _InactiveRpcError as e:
            raise ApiError(_parse_inactive_rpc_error(e), self.origin) from e

        return MessageToDict(all_job_details)

    def block_until_complete(self, job_identifier, poll_interval=0.01, timeout=30):
        """Block until job complete.

        Args:
            job_identifier (str): The job identifier.

        Returns:
            dict: Final job details.

        Raises:
            ApiError: An ApiError will be raised if the API returns an error status,
                or the client is unable to connect.
        """
        endby = time.time() + timeout if (timeout is not None) else None
        while True:
            job_details = self.get_job_details(job_identifier)
            if job_details['status'] in {"COMPLETE", "CANCELLED", "FAILED"}:
                return job_details
            time.sleep(poll_interval)
            if (endby is not None) and (time.time() > endby - poll_interval):
                raise Timeout('timed out before completion')

    def get_results(self, job_identifier):
        """Block until job complete.

        Args:
            job_identifier (str): The job identifier.

        Returns:
            dict: Results for the requested job.

        Raises:
            ApiError: An ApiError will be raised if the API returns an error status,
                or the client is unable to connect.
        """
        job_identifier = JobIdentifier(identifier=job_identifier)
        try:
            results = self._results_client.GetResults(job_identifier)
        except _InactiveRpcError as e:
            raise ApiError(_parse_inactive_rpc_error(e), self.origin) from e

        return MessageToDict(results)
