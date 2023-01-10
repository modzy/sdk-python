from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf import duration_pb2 as _duration_pb2
from google.api import annotations_pb2 as _annotations_pb2
from google.api import field_behavior_pb2 as _field_behavior_pb2
from ....protoc_gen_openapiv2.options import annotations_pb2 as _annotations_pb2_1
from ....common.v1 import common_pb2 as _common_pb2
from ....common.v1 import errors_pb2 as _errors_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

CANCELED: InferenceStatus
COMPLETE: InferenceStatus
DESCRIPTOR: _descriptor.FileDescriptor
FAILED: InferenceStatus
FETCHING: InferenceStatus
IN_PROGRESS: InferenceStatus
QUEUED: InferenceStatus
UNKNOWN_INFERENCE_STATUS: InferenceStatus

class AzureInputSource(_message.Message):
    __slots__ = ["container", "path", "storage_account", "storage_account_key"]
    CONTAINER_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    STORAGE_ACCOUNT_FIELD_NUMBER: _ClassVar[int]
    STORAGE_ACCOUNT_KEY_FIELD_NUMBER: _ClassVar[int]
    container: str
    path: str
    storage_account: str
    storage_account_key: str
    def __init__(self, storage_account: _Optional[str] = ..., storage_account_key: _Optional[str] = ..., container: _Optional[str] = ..., path: _Optional[str] = ...) -> None: ...

class EmbeddedInputSource(_message.Message):
    __slots__ = ["data", "name"]
    DATA_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    data: bytes
    name: str
    def __init__(self, name: _Optional[str] = ..., data: _Optional[bytes] = ...) -> None: ...

class Inference(_message.Message):
    __slots__ = ["completed_at", "elapsed_time", "explain", "identifier", "inputs", "model", "result", "status", "submitted_at", "tags"]
    class TagsEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    COMPLETED_AT_FIELD_NUMBER: _ClassVar[int]
    ELAPSED_TIME_FIELD_NUMBER: _ClassVar[int]
    EXPLAIN_FIELD_NUMBER: _ClassVar[int]
    IDENTIFIER_FIELD_NUMBER: _ClassVar[int]
    INPUTS_FIELD_NUMBER: _ClassVar[int]
    MODEL_FIELD_NUMBER: _ClassVar[int]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    SUBMITTED_AT_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    completed_at: _timestamp_pb2.Timestamp
    elapsed_time: _duration_pb2.Duration
    explain: bool
    identifier: str
    inputs: _containers.RepeatedCompositeFieldContainer[RedactedInputSource]
    model: _common_pb2.ModelIdentifier
    result: InferenceResult
    status: InferenceStatus
    submitted_at: _timestamp_pb2.Timestamp
    tags: _containers.ScalarMap[str, str]
    def __init__(self, identifier: _Optional[str] = ..., model: _Optional[_Union[_common_pb2.ModelIdentifier, _Mapping]] = ..., inputs: _Optional[_Iterable[_Union[RedactedInputSource, _Mapping]]] = ..., tags: _Optional[_Mapping[str, str]] = ..., explain: bool = ..., status: _Optional[_Union[InferenceStatus, str]] = ..., submitted_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., completed_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., elapsed_time: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ..., result: _Optional[_Union[InferenceResult, _Mapping]] = ...) -> None: ...

class InferenceIdentifier(_message.Message):
    __slots__ = ["identifier"]
    IDENTIFIER_FIELD_NUMBER: _ClassVar[int]
    identifier: str
    def __init__(self, identifier: _Optional[str] = ...) -> None: ...

class InferenceRequest(_message.Message):
    __slots__ = ["explain", "inputs", "model", "tags"]
    class TagsEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    EXPLAIN_FIELD_NUMBER: _ClassVar[int]
    INPUTS_FIELD_NUMBER: _ClassVar[int]
    MODEL_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    explain: bool
    inputs: _containers.RepeatedCompositeFieldContainer[InputSource]
    model: _common_pb2.ModelIdentifier
    tags: _containers.ScalarMap[str, str]
    def __init__(self, model: _Optional[_Union[_common_pb2.ModelIdentifier, _Mapping]] = ..., inputs: _Optional[_Iterable[_Union[InputSource, _Mapping]]] = ..., tags: _Optional[_Mapping[str, str]] = ..., explain: bool = ...) -> None: ...

class InferenceResult(_message.Message):
    __slots__ = ["outputs"]
    class Output(_message.Message):
        __slots__ = ["content_type", "data"]
        CONTENT_TYPE_FIELD_NUMBER: _ClassVar[int]
        DATA_FIELD_NUMBER: _ClassVar[int]
        content_type: str
        data: bytes
        def __init__(self, data: _Optional[bytes] = ..., content_type: _Optional[str] = ...) -> None: ...
    class OutputsEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: InferenceResult.Output
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[InferenceResult.Output, _Mapping]] = ...) -> None: ...
    OUTPUTS_FIELD_NUMBER: _ClassVar[int]
    outputs: _containers.MessageMap[str, InferenceResult.Output]
    def __init__(self, outputs: _Optional[_Mapping[str, InferenceResult.Output]] = ...) -> None: ...

class InputSource(_message.Message):
    __slots__ = ["azure", "data", "key", "s3", "text"]
    AZURE_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    KEY_FIELD_NUMBER: _ClassVar[int]
    S3_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    azure: AzureInputSource
    data: bytes
    key: str
    s3: S3InputSource
    text: str
    def __init__(self, key: _Optional[str] = ..., text: _Optional[str] = ..., data: _Optional[bytes] = ..., s3: _Optional[_Union[S3InputSource, _Mapping]] = ..., azure: _Optional[_Union[AzureInputSource, _Mapping]] = ...) -> None: ...

class RedactedInputSource(_message.Message):
    __slots__ = ["azure", "data", "key", "s3", "text"]
    class AzureContentInfo(_message.Message):
        __slots__ = ["container", "path", "sha256_digest", "size_in_bytes", "storage_account"]
        CONTAINER_FIELD_NUMBER: _ClassVar[int]
        PATH_FIELD_NUMBER: _ClassVar[int]
        SHA256_DIGEST_FIELD_NUMBER: _ClassVar[int]
        SIZE_IN_BYTES_FIELD_NUMBER: _ClassVar[int]
        STORAGE_ACCOUNT_FIELD_NUMBER: _ClassVar[int]
        container: str
        path: str
        sha256_digest: str
        size_in_bytes: int
        storage_account: str
        def __init__(self, size_in_bytes: _Optional[int] = ..., sha256_digest: _Optional[str] = ..., storage_account: _Optional[str] = ..., container: _Optional[str] = ..., path: _Optional[str] = ...) -> None: ...
    class EmbeddedContentInfo(_message.Message):
        __slots__ = ["sha256_digest", "size_in_bytes"]
        SHA256_DIGEST_FIELD_NUMBER: _ClassVar[int]
        SIZE_IN_BYTES_FIELD_NUMBER: _ClassVar[int]
        sha256_digest: str
        size_in_bytes: int
        def __init__(self, size_in_bytes: _Optional[int] = ..., sha256_digest: _Optional[str] = ...) -> None: ...
    class S3ContentInfo(_message.Message):
        __slots__ = ["bucket", "endpoint", "path", "region", "sha256_digest", "size_in_bytes"]
        BUCKET_FIELD_NUMBER: _ClassVar[int]
        ENDPOINT_FIELD_NUMBER: _ClassVar[int]
        PATH_FIELD_NUMBER: _ClassVar[int]
        REGION_FIELD_NUMBER: _ClassVar[int]
        SHA256_DIGEST_FIELD_NUMBER: _ClassVar[int]
        SIZE_IN_BYTES_FIELD_NUMBER: _ClassVar[int]
        bucket: str
        endpoint: str
        path: str
        region: str
        sha256_digest: str
        size_in_bytes: int
        def __init__(self, size_in_bytes: _Optional[int] = ..., sha256_digest: _Optional[str] = ..., endpoint: _Optional[str] = ..., region: _Optional[str] = ..., bucket: _Optional[str] = ..., path: _Optional[str] = ...) -> None: ...
    AZURE_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    KEY_FIELD_NUMBER: _ClassVar[int]
    S3_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    azure: RedactedInputSource.AzureContentInfo
    data: RedactedInputSource.EmbeddedContentInfo
    key: str
    s3: RedactedInputSource.S3ContentInfo
    text: RedactedInputSource.EmbeddedContentInfo
    def __init__(self, key: _Optional[str] = ..., text: _Optional[_Union[RedactedInputSource.EmbeddedContentInfo, _Mapping]] = ..., data: _Optional[_Union[RedactedInputSource.EmbeddedContentInfo, _Mapping]] = ..., s3: _Optional[_Union[RedactedInputSource.S3ContentInfo, _Mapping]] = ..., azure: _Optional[_Union[RedactedInputSource.AzureContentInfo, _Mapping]] = ...) -> None: ...

class S3InputSource(_message.Message):
    __slots__ = ["access_key_id", "access_key_secret", "bucket", "endpoint", "path", "region"]
    ACCESS_KEY_ID_FIELD_NUMBER: _ClassVar[int]
    ACCESS_KEY_SECRET_FIELD_NUMBER: _ClassVar[int]
    BUCKET_FIELD_NUMBER: _ClassVar[int]
    ENDPOINT_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    REGION_FIELD_NUMBER: _ClassVar[int]
    access_key_id: str
    access_key_secret: str
    bucket: str
    endpoint: str
    path: str
    region: str
    def __init__(self, endpoint: _Optional[str] = ..., region: _Optional[str] = ..., bucket: _Optional[str] = ..., path: _Optional[str] = ..., access_key_id: _Optional[str] = ..., access_key_secret: _Optional[str] = ...) -> None: ...

class TextInputSource(_message.Message):
    __slots__ = ["name", "text"]
    NAME_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    name: str
    text: str
    def __init__(self, name: _Optional[str] = ..., text: _Optional[str] = ...) -> None: ...

class InferenceStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
