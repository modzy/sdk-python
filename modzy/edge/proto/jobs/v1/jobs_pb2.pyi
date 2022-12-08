from google.protobuf import empty_pb2 as _empty_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf import struct_pb2 as _struct_pb2
from google.api import annotations_pb2 as _annotations_pb2
from google.api import field_behavior_pb2 as _field_behavior_pb2
from modzy.edge.proto.protoc_gen_openapiv2.options import annotations_pb2 as _annotations_pb2_1
from modzy.edge.proto.common.v1 import common_pb2 as _common_pb2
from modzy.edge.proto.common.v1 import errors_pb2 as _errors_pb2
from modzy.edge.proto.accounting.v1 import accounting_pb2 as _accounting_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

CANCELED: JobStatus
COMPLETE: JobStatus
DESCRIPTOR: _descriptor.FileDescriptor
FAILED: JobStatus
IN_PROGRESS: JobStatus
OPEN: JobStatus
SUBMITTED: JobStatus
UNKNOWN: JobStatus

class AppendableJobInput(_message.Message):
    __slots__ = ["data", "datasource_name", "input_name", "job_identifier"]
    DATASOURCE_NAME_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    INPUT_NAME_FIELD_NUMBER: _ClassVar[int]
    JOB_IDENTIFIER_FIELD_NUMBER: _ClassVar[int]
    data: bytes
    datasource_name: str
    input_name: str
    job_identifier: str
    def __init__(self, job_identifier: _Optional[str] = ..., datasource_name: _Optional[str] = ..., input_name: _Optional[str] = ..., data: _Optional[bytes] = ...) -> None: ...

class JobDetails(_message.Message):
    __slots__ = ["completed", "created_at", "elapsed_time", "failed", "job_identifier", "job_inputs", "model", "pending", "status", "submitted_at", "total", "updated_at"]
    class JobInputs(_message.Message):
        __slots__ = ["identifier"]
        IDENTIFIER_FIELD_NUMBER: _ClassVar[int]
        identifier: str
        def __init__(self, identifier: _Optional[str] = ...) -> None: ...
    COMPLETED_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    ELAPSED_TIME_FIELD_NUMBER: _ClassVar[int]
    FAILED_FIELD_NUMBER: _ClassVar[int]
    JOB_IDENTIFIER_FIELD_NUMBER: _ClassVar[int]
    JOB_INPUTS_FIELD_NUMBER: _ClassVar[int]
    MODEL_FIELD_NUMBER: _ClassVar[int]
    PENDING_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    SUBMITTED_AT_FIELD_NUMBER: _ClassVar[int]
    TOTAL_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    completed: int
    created_at: _timestamp_pb2.Timestamp
    elapsed_time: int
    failed: int
    job_identifier: str
    job_inputs: _containers.RepeatedCompositeFieldContainer[JobDetails.JobInputs]
    model: _common_pb2.ModelIdentifier
    pending: int
    status: str
    submitted_at: _timestamp_pb2.Timestamp
    total: int
    updated_at: _timestamp_pb2.Timestamp
    def __init__(self, job_identifier: _Optional[str] = ..., model: _Optional[_Union[_common_pb2.ModelIdentifier, _Mapping]] = ..., status: _Optional[str] = ..., created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., updated_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., submitted_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., total: _Optional[int] = ..., pending: _Optional[int] = ..., completed: _Optional[int] = ..., failed: _Optional[int] = ..., elapsed_time: _Optional[int] = ..., job_inputs: _Optional[_Iterable[_Union[JobDetails.JobInputs, _Mapping]]] = ...) -> None: ...

class JobDetailsList(_message.Message):
    __slots__ = ["jobs", "page_count", "page_number", "page_size", "total_count"]
    JOBS_FIELD_NUMBER: _ClassVar[int]
    PAGE_COUNT_FIELD_NUMBER: _ClassVar[int]
    PAGE_NUMBER_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    TOTAL_COUNT_FIELD_NUMBER: _ClassVar[int]
    jobs: _containers.RepeatedCompositeFieldContainer[JobDetails]
    page_count: int
    page_number: int
    page_size: int
    total_count: int
    def __init__(self, jobs: _Optional[_Iterable[_Union[JobDetails, _Mapping]]] = ..., total_count: _Optional[int] = ..., page_number: _Optional[int] = ..., page_size: _Optional[int] = ..., page_count: _Optional[int] = ...) -> None: ...

class JobFeatures(_message.Message):
    __slots__ = ["input_chunk_maximum_size", "maximum_input_chunks", "maximum_inputs_per_job"]
    INPUT_CHUNK_MAXIMUM_SIZE_FIELD_NUMBER: _ClassVar[int]
    MAXIMUM_INPUTS_PER_JOB_FIELD_NUMBER: _ClassVar[int]
    MAXIMUM_INPUT_CHUNKS_FIELD_NUMBER: _ClassVar[int]
    input_chunk_maximum_size: str
    maximum_input_chunks: int
    maximum_inputs_per_job: int
    def __init__(self, input_chunk_maximum_size: _Optional[str] = ..., maximum_input_chunks: _Optional[int] = ..., maximum_inputs_per_job: _Optional[int] = ...) -> None: ...

class JobFilter(_message.Message):
    __slots__ = ["access_key", "end_date", "model", "start_date", "status", "user"]
    ACCESS_KEY_FIELD_NUMBER: _ClassVar[int]
    END_DATE_FIELD_NUMBER: _ClassVar[int]
    MODEL_FIELD_NUMBER: _ClassVar[int]
    START_DATE_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    USER_FIELD_NUMBER: _ClassVar[int]
    access_key: str
    end_date: str
    model: str
    start_date: str
    status: str
    user: str
    def __init__(self, start_date: _Optional[str] = ..., end_date: _Optional[str] = ..., status: _Optional[str] = ..., model: _Optional[str] = ..., user: _Optional[str] = ..., access_key: _Optional[str] = ...) -> None: ...

class JobHistoryFilter(_message.Message):
    __slots__ = ["access_key", "end_date", "model", "model_identifier", "model_version", "search", "start_date", "status", "user"]
    ACCESS_KEY_FIELD_NUMBER: _ClassVar[int]
    END_DATE_FIELD_NUMBER: _ClassVar[int]
    MODEL_FIELD_NUMBER: _ClassVar[int]
    MODEL_IDENTIFIER_FIELD_NUMBER: _ClassVar[int]
    MODEL_VERSION_FIELD_NUMBER: _ClassVar[int]
    SEARCH_FIELD_NUMBER: _ClassVar[int]
    START_DATE_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    USER_FIELD_NUMBER: _ClassVar[int]
    access_key: str
    end_date: str
    model: str
    model_identifier: str
    model_version: str
    search: str
    start_date: str
    status: str
    user: str
    def __init__(self, search: _Optional[str] = ..., user: _Optional[str] = ..., model: _Optional[str] = ..., access_key: _Optional[str] = ..., start_date: _Optional[str] = ..., end_date: _Optional[str] = ..., status: _Optional[str] = ..., model_identifier: _Optional[str] = ..., model_version: _Optional[str] = ...) -> None: ...

class JobIdentifier(_message.Message):
    __slots__ = ["identifier"]
    IDENTIFIER_FIELD_NUMBER: _ClassVar[int]
    identifier: str
    def __init__(self, identifier: _Optional[str] = ...) -> None: ...

class JobInput(_message.Message):
    __slots__ = ["accessKeyID", "endpoint", "region", "secretAccessKey", "sources", "storageAccount", "storageAccountKey", "timeout", "type"]
    class SourcesEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: _struct_pb2.Struct
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...) -> None: ...
    ACCESSKEYID_FIELD_NUMBER: _ClassVar[int]
    ENDPOINT_FIELD_NUMBER: _ClassVar[int]
    REGION_FIELD_NUMBER: _ClassVar[int]
    SECRETACCESSKEY_FIELD_NUMBER: _ClassVar[int]
    SOURCES_FIELD_NUMBER: _ClassVar[int]
    STORAGEACCOUNTKEY_FIELD_NUMBER: _ClassVar[int]
    STORAGEACCOUNT_FIELD_NUMBER: _ClassVar[int]
    TIMEOUT_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    accessKeyID: str
    endpoint: str
    region: str
    secretAccessKey: str
    sources: _containers.MessageMap[str, _struct_pb2.Struct]
    storageAccount: str
    storageAccountKey: str
    timeout: int
    type: str
    def __init__(self, type: _Optional[str] = ..., sources: _Optional[_Mapping[str, _struct_pb2.Struct]] = ..., timeout: _Optional[int] = ..., accessKeyID: _Optional[str] = ..., secretAccessKey: _Optional[str] = ..., region: _Optional[str] = ..., endpoint: _Optional[str] = ..., storageAccount: _Optional[str] = ..., storageAccountKey: _Optional[str] = ...) -> None: ...

class JobStatistics(_message.Message):
    __slots__ = ["access_key", "jobs_count", "last_api_usage", "models_count", "models_list"]
    class Model(_message.Message):
        __slots__ = ["identifier", "name", "processed_jobs_count", "version"]
        IDENTIFIER_FIELD_NUMBER: _ClassVar[int]
        NAME_FIELD_NUMBER: _ClassVar[int]
        PROCESSED_JOBS_COUNT_FIELD_NUMBER: _ClassVar[int]
        VERSION_FIELD_NUMBER: _ClassVar[int]
        identifier: str
        name: str
        processed_jobs_count: int
        version: str
        def __init__(self, identifier: _Optional[str] = ..., name: _Optional[str] = ..., processed_jobs_count: _Optional[int] = ..., version: _Optional[str] = ...) -> None: ...
    ACCESS_KEY_FIELD_NUMBER: _ClassVar[int]
    JOBS_COUNT_FIELD_NUMBER: _ClassVar[int]
    LAST_API_USAGE_FIELD_NUMBER: _ClassVar[int]
    MODELS_COUNT_FIELD_NUMBER: _ClassVar[int]
    MODELS_LIST_FIELD_NUMBER: _ClassVar[int]
    access_key: str
    jobs_count: int
    last_api_usage: _timestamp_pb2.Timestamp
    models_count: int
    models_list: _containers.RepeatedCompositeFieldContainer[JobStatistics.Model]
    def __init__(self, access_key: _Optional[str] = ..., jobs_count: _Optional[int] = ..., last_api_usage: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., models_count: _Optional[int] = ..., models_list: _Optional[_Iterable[_Union[JobStatistics.Model, _Mapping]]] = ...) -> None: ...

class JobStatisticsList(_message.Message):
    __slots__ = ["page_count", "page_number", "page_size", "statistics", "total_count"]
    PAGE_COUNT_FIELD_NUMBER: _ClassVar[int]
    PAGE_NUMBER_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    STATISTICS_FIELD_NUMBER: _ClassVar[int]
    TOTAL_COUNT_FIELD_NUMBER: _ClassVar[int]
    page_count: int
    page_number: int
    page_size: int
    statistics: _containers.RepeatedCompositeFieldContainer[JobStatistics]
    total_count: int
    def __init__(self, statistics: _Optional[_Iterable[_Union[JobStatistics, _Mapping]]] = ..., total_count: _Optional[int] = ..., page_number: _Optional[int] = ..., page_size: _Optional[int] = ..., page_count: _Optional[int] = ...) -> None: ...

class JobSubmission(_message.Message):
    __slots__ = ["explain", "input", "model"]
    EXPLAIN_FIELD_NUMBER: _ClassVar[int]
    INPUT_FIELD_NUMBER: _ClassVar[int]
    MODEL_FIELD_NUMBER: _ClassVar[int]
    explain: bool
    input: JobInput
    model: _common_pb2.ModelIdentifier
    def __init__(self, model: _Optional[_Union[_common_pb2.ModelIdentifier, _Mapping]] = ..., input: _Optional[_Union[JobInput, _Mapping]] = ..., explain: bool = ...) -> None: ...

class JobSubmissionReceipt(_message.Message):
    __slots__ = ["access_key", "details", "explain", "input_byte_amount", "job_identifier", "job_inputs", "model", "status", "submitted_at", "total_inputs"]
    class JobDetails(_message.Message):
        __slots__ = ["account_identifier", "completed", "created_at", "elapsed_time", "failed", "pending", "total", "updated_at"]
        ACCOUNT_IDENTIFIER_FIELD_NUMBER: _ClassVar[int]
        COMPLETED_FIELD_NUMBER: _ClassVar[int]
        CREATED_AT_FIELD_NUMBER: _ClassVar[int]
        ELAPSED_TIME_FIELD_NUMBER: _ClassVar[int]
        FAILED_FIELD_NUMBER: _ClassVar[int]
        PENDING_FIELD_NUMBER: _ClassVar[int]
        TOTAL_FIELD_NUMBER: _ClassVar[int]
        UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
        account_identifier: str
        completed: int
        created_at: _timestamp_pb2.Timestamp
        elapsed_time: int
        failed: int
        pending: int
        total: int
        updated_at: _timestamp_pb2.Timestamp
        def __init__(self, account_identifier: _Optional[str] = ..., created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., updated_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., total: _Optional[int] = ..., pending: _Optional[int] = ..., completed: _Optional[int] = ..., failed: _Optional[int] = ..., elapsed_time: _Optional[int] = ...) -> None: ...
    class JobInputs(_message.Message):
        __slots__ = ["identifier"]
        IDENTIFIER_FIELD_NUMBER: _ClassVar[int]
        identifier: _containers.RepeatedScalarFieldContainer[str]
        def __init__(self, identifier: _Optional[_Iterable[str]] = ...) -> None: ...
    ACCESS_KEY_FIELD_NUMBER: _ClassVar[int]
    DETAILS_FIELD_NUMBER: _ClassVar[int]
    EXPLAIN_FIELD_NUMBER: _ClassVar[int]
    INPUT_BYTE_AMOUNT_FIELD_NUMBER: _ClassVar[int]
    JOB_IDENTIFIER_FIELD_NUMBER: _ClassVar[int]
    JOB_INPUTS_FIELD_NUMBER: _ClassVar[int]
    MODEL_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    SUBMITTED_AT_FIELD_NUMBER: _ClassVar[int]
    TOTAL_INPUTS_FIELD_NUMBER: _ClassVar[int]
    access_key: str
    details: JobSubmissionReceipt.JobDetails
    explain: bool
    input_byte_amount: int
    job_identifier: str
    job_inputs: JobSubmissionReceipt.JobInputs
    model: _common_pb2.ModelIdentifier
    status: JobStatus
    submitted_at: _timestamp_pb2.Timestamp
    total_inputs: int
    def __init__(self, job_identifier: _Optional[str] = ..., model: _Optional[_Union[_common_pb2.ModelIdentifier, _Mapping]] = ..., access_key: _Optional[str] = ..., total_inputs: _Optional[int] = ..., input_byte_amount: _Optional[int] = ..., job_inputs: _Optional[_Union[JobSubmissionReceipt.JobInputs, _Mapping]] = ..., submitted_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., status: _Optional[_Union[JobStatus, str]] = ..., details: _Optional[_Union[JobSubmissionReceipt.JobDetails, _Mapping]] = ..., explain: bool = ...) -> None: ...

class JobSummary(_message.Message):
    __slots__ = ["job_identifier", "model", "status"]
    JOB_IDENTIFIER_FIELD_NUMBER: _ClassVar[int]
    MODEL_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    job_identifier: str
    model: _common_pb2.ModelIdentifier
    status: str
    def __init__(self, job_identifier: _Optional[str] = ..., status: _Optional[str] = ..., model: _Optional[_Union[_common_pb2.ModelIdentifier, _Mapping]] = ...) -> None: ...

class JobSummaryList(_message.Message):
    __slots__ = ["jobs", "page_count", "page_number", "page_size", "total_count"]
    JOBS_FIELD_NUMBER: _ClassVar[int]
    PAGE_COUNT_FIELD_NUMBER: _ClassVar[int]
    PAGE_NUMBER_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    TOTAL_COUNT_FIELD_NUMBER: _ClassVar[int]
    jobs: _containers.RepeatedCompositeFieldContainer[JobSummary]
    page_count: int
    page_number: int
    page_size: int
    total_count: int
    def __init__(self, jobs: _Optional[_Iterable[_Union[JobSummary, _Mapping]]] = ..., total_count: _Optional[int] = ..., page_number: _Optional[int] = ..., page_size: _Optional[int] = ..., page_count: _Optional[int] = ...) -> None: ...

class JobStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
