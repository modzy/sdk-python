import logging
import time
from typing import Iterable, List

from grpc.aio import Channel

from .proto.common.v1.common_pb2 import ModelIdentifier
from .proto.inferences.api.v1.inferences_pb2 import CANCELED, COMPLETE, FAILED, Inference, InferenceIdentifier, InferenceRequest, InputSource
from .proto.inferences.api.v1.inferences_pb2_grpc import InferenceServiceStub
from ..error import Timeout


def _inference_is_finished(inference: Inference) -> bool:
    return inference.status in [COMPLETE, CANCELED, FAILED]


class EdgeInferenceClient:

    def __init__(self, channel: Channel, origin=""):
        self.logger = logging.getLogger(__name__)
        self.origin = origin
        self._channel = channel
        self.client = InferenceServiceStub(self._channel)

    def build_inference_request(self, model_identifier: str, model_version: str, input_sources: List[InputSource], explain=False, tags=None) -> InferenceRequest:
        if tags is None:
            tags = {}
        return InferenceRequest(
            model=ModelIdentifier(identifier=model_identifier, version=model_version),
            inputs=input_sources,
            explain=explain,
            tags=tags,
        )

    def perform_inference(self, model_identifier: str, model_version: str, input_sources: List[InputSource], explain=False, tags=None) -> Inference:
        """
        Perform an inference on some data against a particular model version.

        To supply data to the model, please provide one or more InputSource objects in a List.
        Each InputSource has a key and can have one of the following data types:

            - text: a UTF-8 encoded string
            - data: a Base64 encoded byte string
            - s3 (see below)
            - azure (see below)

        The key of each InputSource should be one of the keys expected by the model. Please refer
        to the model's documentation page to see what input keys the model expects. Most models only
        take one piece of data as input and thus will only have one InputSource in the list. For
        models that require more than one piece of data to perform a single inference, please provide
        one InputSource object for each piece of data that the model expects in order to perform the
        inference.

        The data for each InputSource can be provided in one of several ways. Each InputSource object
        should have exactly one of the data fields defined, the rest should be left blank.

        For the following examples, we will be using an exemplar text classification model that takes
        a single input whose key is "input.txt".

        Examples:

            .. code-block::
                # Submit a piece of text to the model.
                from modzy.edge.proto.inferences.api.v1.inferences_pb2 import InputSource
                inference = edge_client.submit(
                    "text-classifier",
                    "1.0.0",
                    [
                        InputSource(
                            key="input.txt",
                            text="A sample bit of text to run an inference on."
                        )
                    ],
                    explain=False,
                    tags={
                        "a tag key": "some tag value",
                        "another tag key": "another tag value",
                    },
                )

            .. code-block::
                # Submit a piece of text to the model as a binary string.
                from modzy.edge.proto.inferences.api.v1.inferences_pb2 import InputSource
                inference = edge_client.submit(
                    "text-classifier",
                    "1.0.0",
                    [
                        InputSource(
                            key="input.txt",
                            data=b"QSBzYW1wbGUgYml0IG9mIHRleHQgdG8gcnVuIGFuIGluZmVyZW5jZSBvbi4K"
                        )
                    ],
                    explain=False,
                    tags={
                        "a tag key": "some tag value",
                        "another tag key": "another tag value",
                    },
                )

            .. code-block::
                # Submit a piece of text to the model from a file in AWS S3.
                from modzy.edge.proto.inferences.api.v1.inferences_pb2 import InputSource, S3InputSource
                inference = edge_client.submit(
                    "text-classifier",
                    "1.0.0",
                    [
                        InputSource(
                            key="input.txt",
                            s3=S3InputSource(
                                region="us-east-1",
                                bucket="my-bucket",
                                path="path/to/my-file.txt",
                                access_key_id=os.getenv("AWS_ACCESS_KEY_ID")
                                access_key_secret=os.getenv("AWS_SECRET_ACCESS_KEY")
                            )
                        )
                    ],
                    explain=False,
                    tags={
                        "a tag key": "some tag value",
                        "another tag key": "another tag value",
                    },
                )

            .. code-block::
                # Submit a piece of text to the model from a file in a S3-compatible storage provider
                # like MinIO or NetApp StorageGrid.
                from modzy.edge.proto.inferences.api.v1.inferences_pb2 import InputSource, S3InputSource
                inference = edge_client.submit(
                    "text-classifier",
                    "1.0.0",
                    [
                        InputSource(
                            key="input.txt",
                            s3=S3InputSource(
                                endpoint="https://my-storage-provider.example.com",
                                bucket="my-bucket",
                                path="path/to/my-file.txt",
                                access_key_id=os.getenv("AWS_ACCESS_KEY_ID")
                                access_key_secret=os.getenv("AWS_SECRET_ACCESS_KEY")
                            )
                        )
                    ],
                    explain=False,
                    tags={
                        "a tag key": "some tag value",
                        "another tag key": "another tag value",
                    },
                )

            .. code-block::
                # Submit a piece of text to the model from a file in Azure BlobStorage.
                from modzy.edge.proto.inferences.api.v1.inferences_pb2 import InputSource, AzureInputSource
                inference = edge_client.submit(
                    "text-classifier",
                    "1.0.0",
                    [
                        InputSource(
                            key="input.txt",
                            azure=AzureInputSource(
                                container="my-blob-container",
                                path="path/to/my-file.txt",
                                storage_account="my-azure-storage-account-name"
                                storage_account_key=os.getenv("AZURE_STORAGE_KEY")
                            )
                        )
                    ],
                    explain=False,
                    tags={
                        "a tag key": "some tag value",
                        "another tag key": "another tag value",
                    },
                )

        Args:
            model_identifier (str): The model identifier.
            model_version (str): The model version string in semantic version format.
            input_sources (List[InputSource]): A list of input sources.
                For more information about the format, please see the above examples.
            explain (bool): Set to `True` to produce explainable results.
            tags (Mapping[str, str]): An arbitrary set of key/value tags to associate with this inference.

        Returns:
            Inference: An Inference object
        """
        inference_request = self.build_inference_request(model_identifier, model_version, input_sources, explain, tags)
        return self.client.PerformInference(inference_request)

    def run(self, model_identifier: str, model_version: str, input_sources: List[InputSource], explain=False, tags=None) -> Inference:
        """
        Provides a synchronous way to run an inference.

        This is simply a convenience function that is equivalent to:

        .. code-block::
            inference = self.submit(model_identifier, model_version, input_sources, explain, tags)
            inference = self.block_until_complete(inference.identifier)

        For information about parameters and return values, please the docs for `EdgeInferenceClient.submit`.
        """
        inference = self.perform_inference(model_identifier, model_version, input_sources, explain, tags)
        return self.block_until_complete(inference.identifier)

    def get_inference_details(self, inference_identifier: str) -> Inference:
        return self.client.GetInferenceDetails(InferenceIdentifier(identifier=inference_identifier))

    def block_until_complete(self, inference_identifier, poll_interval=0.01, timeout=30) -> Inference:
        end_time = time.time() + timeout if (timeout is not None) else None
        while True:
            inference = self.get_inference_details(inference_identifier)
            if _inference_is_finished(inference):
                return inference
            time.sleep(poll_interval)
            if (end_time is not None) and (time.time() > end_time - poll_interval):
                raise Timeout("timed out before completion")

    def stream(self, input_iterator: Iterable[InferenceRequest]) -> Iterable[Inference]:
        # For now we're going to "fake" streaming by just iterating over each of the inputs and
        # collecting the outputs before returning. The performance docs for gRPC recommend using
        # Unary calls over Stream calls in Python because it's much faster.
        # c.f. https://grpc.io/docs/guides/performance/#python
        #
        # This method definition should support _actual_ streaming in the future if/when it's
        # reasonable to do so.
        results = []
        for input in input_iterator:
            inference = self.client.PerformInference(input)
            results.append(self.block_until_complete(inference.identifier))
        return results
