from google.protobuf import any_pb2 as _any_pb2
from google.protobuf import empty_pb2 as _empty_pb2
from google.protobuf import struct_pb2 as _struct_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.api import annotations_pb2 as _annotations_pb2
from google.api import field_behavior_pb2 as _field_behavior_pb2
from modzy.edge.proto.protoc_gen_openapiv2.options import annotations_pb2 as _annotations_pb2_1
from modzy.edge.proto.common.v1 import common_pb2 as _common_pb2
from modzy.edge.proto.common.v1 import errors_pb2 as _errors_pb2
from modzy.edge.proto.accounting.v1 import accounting_pb2 as _accounting_pb2
from modzy.edge.proto.jobs.v1 import jobs_pb2 as _jobs_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class OutputIdentifier(_message.Message):
    __slots__ = ["output_identifier", "result_identifier"]
    OUTPUT_IDENTIFIER_FIELD_NUMBER: _ClassVar[int]
    RESULT_IDENTIFIER_FIELD_NUMBER: _ClassVar[int]
    output_identifier: str
    result_identifier: ResultIdentifier
    def __init__(self, result_identifier: _Optional[_Union[ResultIdentifier, _Mapping]] = ..., output_identifier: _Optional[str] = ...) -> None: ...

class Result(_message.Message):
    __slots__ = ["access_key", "end_time", "engine", "explained", "input_completed_time", "input_fetching_time", "input_name", "input_size", "job", "model_latency", "output_uploading_time", "queue_time", "result", "start_time", "update_time", "use_legacy_datasource_json", "voting"]
    class Job(_message.Message):
        __slots__ = ["account", "average_model_latency", "completed_input_count", "created_at", "elapsed_time", "failed_input_count", "finished", "identifier", "initial_queue_time", "input_size", "model", "result_summarizing_time", "result_summary_started_at", "submitted_at", "submitted_by", "tags", "team", "total_input_count", "total_queue_time", "updated_at", "user"]
        ACCOUNT_FIELD_NUMBER: _ClassVar[int]
        AVERAGE_MODEL_LATENCY_FIELD_NUMBER: _ClassVar[int]
        COMPLETED_INPUT_COUNT_FIELD_NUMBER: _ClassVar[int]
        CREATED_AT_FIELD_NUMBER: _ClassVar[int]
        ELAPSED_TIME_FIELD_NUMBER: _ClassVar[int]
        FAILED_INPUT_COUNT_FIELD_NUMBER: _ClassVar[int]
        FINISHED_FIELD_NUMBER: _ClassVar[int]
        IDENTIFIER_FIELD_NUMBER: _ClassVar[int]
        INITIAL_QUEUE_TIME_FIELD_NUMBER: _ClassVar[int]
        INPUT_SIZE_FIELD_NUMBER: _ClassVar[int]
        MODEL_FIELD_NUMBER: _ClassVar[int]
        RESULT_SUMMARIZING_TIME_FIELD_NUMBER: _ClassVar[int]
        RESULT_SUMMARY_STARTED_AT_FIELD_NUMBER: _ClassVar[int]
        SUBMITTED_AT_FIELD_NUMBER: _ClassVar[int]
        SUBMITTED_BY_FIELD_NUMBER: _ClassVar[int]
        TAGS_FIELD_NUMBER: _ClassVar[int]
        TEAM_FIELD_NUMBER: _ClassVar[int]
        TOTAL_INPUT_COUNT_FIELD_NUMBER: _ClassVar[int]
        TOTAL_QUEUE_TIME_FIELD_NUMBER: _ClassVar[int]
        UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
        USER_FIELD_NUMBER: _ClassVar[int]
        account: _accounting_pb2.AccountIdentifier
        average_model_latency: float
        completed_input_count: int
        created_at: int
        elapsed_time: int
        failed_input_count: int
        finished: bool
        identifier: str
        initial_queue_time: int
        input_size: int
        model: _common_pb2.ModelIdentifier
        result_summarizing_time: int
        result_summary_started_at: int
        submitted_at: int
        submitted_by: str
        tags: _containers.RepeatedScalarFieldContainer[str]
        team: _accounting_pb2.TeamIdentifier
        total_input_count: int
        total_queue_time: int
        updated_at: int
        user: _accounting_pb2.UserIdentifier
        def __init__(self, identifier: _Optional[str] = ..., created_at: _Optional[int] = ..., updated_at: _Optional[int] = ..., model: _Optional[_Union[_common_pb2.ModelIdentifier, _Mapping]] = ..., user: _Optional[_Union[_accounting_pb2.UserIdentifier, _Mapping]] = ..., submitted_by: _Optional[str] = ..., team: _Optional[_Union[_accounting_pb2.TeamIdentifier, _Mapping]] = ..., account: _Optional[_Union[_accounting_pb2.AccountIdentifier, _Mapping]] = ..., tags: _Optional[_Iterable[str]] = ..., total_input_count: _Optional[int] = ..., completed_input_count: _Optional[int] = ..., failed_input_count: _Optional[int] = ..., submitted_at: _Optional[int] = ..., initial_queue_time: _Optional[int] = ..., total_queue_time: _Optional[int] = ..., average_model_latency: _Optional[float] = ..., result_summary_started_at: _Optional[int] = ..., input_size: _Optional[int] = ..., finished: bool = ..., elapsed_time: _Optional[int] = ..., result_summarizing_time: _Optional[int] = ...) -> None: ...
    ACCESS_KEY_FIELD_NUMBER: _ClassVar[int]
    END_TIME_FIELD_NUMBER: _ClassVar[int]
    ENGINE_FIELD_NUMBER: _ClassVar[int]
    EXPLAINED_FIELD_NUMBER: _ClassVar[int]
    INPUT_COMPLETED_TIME_FIELD_NUMBER: _ClassVar[int]
    INPUT_FETCHING_TIME_FIELD_NUMBER: _ClassVar[int]
    INPUT_NAME_FIELD_NUMBER: _ClassVar[int]
    INPUT_SIZE_FIELD_NUMBER: _ClassVar[int]
    JOB_FIELD_NUMBER: _ClassVar[int]
    MODEL_LATENCY_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_UPLOADING_TIME_FIELD_NUMBER: _ClassVar[int]
    QUEUE_TIME_FIELD_NUMBER: _ClassVar[int]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    UPDATE_TIME_FIELD_NUMBER: _ClassVar[int]
    USE_LEGACY_DATASOURCE_JSON_FIELD_NUMBER: _ClassVar[int]
    VOTING_FIELD_NUMBER: _ClassVar[int]
    access_key: str
    end_time: int
    engine: str
    explained: bool
    input_completed_time: int
    input_fetching_time: int
    input_name: str
    input_size: int
    job: Result.Job
    model_latency: float
    output_uploading_time: int
    queue_time: int
    result: _struct_pb2.Struct
    start_time: int
    update_time: int
    use_legacy_datasource_json: bool
    voting: Voting
    def __init__(self, job: _Optional[_Union[Result.Job, _Mapping]] = ..., input_name: _Optional[str] = ..., start_time: _Optional[int] = ..., update_time: _Optional[int] = ..., end_time: _Optional[int] = ..., explained: bool = ..., engine: _Optional[str] = ..., queue_time: _Optional[int] = ..., input_fetching_time: _Optional[int] = ..., output_uploading_time: _Optional[int] = ..., model_latency: _Optional[float] = ..., input_completed_time: _Optional[int] = ..., access_key: _Optional[str] = ..., input_size: _Optional[int] = ..., use_legacy_datasource_json: bool = ..., result: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ..., voting: _Optional[_Union[Voting, _Mapping]] = ...) -> None: ...

class ResultIdentifier(_message.Message):
    __slots__ = ["input_identifier", "job_identifier"]
    INPUT_IDENTIFIER_FIELD_NUMBER: _ClassVar[int]
    JOB_IDENTIFIER_FIELD_NUMBER: _ClassVar[int]
    input_identifier: str
    job_identifier: _jobs_pb2.JobIdentifier
    def __init__(self, job_identifier: _Optional[_Union[_jobs_pb2.JobIdentifier, _Mapping]] = ..., input_identifier: _Optional[str] = ...) -> None: ...

class ResultOutput(_message.Message):
    __slots__ = ["data"]
    DATA_FIELD_NUMBER: _ClassVar[int]
    data: bytes
    def __init__(self, data: _Optional[bytes] = ...) -> None: ...

class ResultVote(_message.Message):
    __slots__ = ["vote"]
    class Vote(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    DOWN: ResultVote.Vote
    NO_VOTES: ResultVote.Vote
    UP: ResultVote.Vote
    VOTE_FIELD_NUMBER: _ClassVar[int]
    vote: ResultVote.Vote
    def __init__(self, vote: _Optional[_Union[ResultVote.Vote, str]] = ...) -> None: ...

class Results(_message.Message):
    __slots__ = ["account_identifier", "average_model_latency", "completed", "elapsed_time", "explained", "failed", "failures", "finished", "initial_queue_time", "input_size", "job_identifier", "result_summarizing", "results", "starting_result_summarizing", "submitted_at", "submitted_by_key", "team", "total", "total_model_latency", "total_queue_time"]
    class FailuresEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: _any_pb2.Any
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[_any_pb2.Any, _Mapping]] = ...) -> None: ...
    class InputResult(_message.Message):
        __slots__ = ["end_time", "engine", "input_fetching", "model_latency", "output_uploading", "queue_time", "results", "start_time", "status", "update_time", "voting"]
        END_TIME_FIELD_NUMBER: _ClassVar[int]
        ENGINE_FIELD_NUMBER: _ClassVar[int]
        INPUT_FETCHING_FIELD_NUMBER: _ClassVar[int]
        MODEL_LATENCY_FIELD_NUMBER: _ClassVar[int]
        OUTPUT_UPLOADING_FIELD_NUMBER: _ClassVar[int]
        QUEUE_TIME_FIELD_NUMBER: _ClassVar[int]
        RESULTS_FIELD_NUMBER: _ClassVar[int]
        START_TIME_FIELD_NUMBER: _ClassVar[int]
        STATUS_FIELD_NUMBER: _ClassVar[int]
        UPDATE_TIME_FIELD_NUMBER: _ClassVar[int]
        VOTING_FIELD_NUMBER: _ClassVar[int]
        end_time: _timestamp_pb2.Timestamp
        engine: str
        input_fetching: int
        model_latency: float
        output_uploading: int
        queue_time: int
        results: _struct_pb2.Struct
        start_time: _timestamp_pb2.Timestamp
        status: str
        update_time: _timestamp_pb2.Timestamp
        voting: Voting
        def __init__(self, status: _Optional[str] = ..., engine: _Optional[str] = ..., input_fetching: _Optional[int] = ..., output_uploading: _Optional[int] = ..., model_latency: _Optional[float] = ..., queue_time: _Optional[int] = ..., start_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., update_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., end_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., results: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ..., voting: _Optional[_Union[Voting, _Mapping]] = ...) -> None: ...
    class ResultsEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: Results.InputResult
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[Results.InputResult, _Mapping]] = ...) -> None: ...
    ACCOUNT_IDENTIFIER_FIELD_NUMBER: _ClassVar[int]
    AVERAGE_MODEL_LATENCY_FIELD_NUMBER: _ClassVar[int]
    COMPLETED_FIELD_NUMBER: _ClassVar[int]
    ELAPSED_TIME_FIELD_NUMBER: _ClassVar[int]
    EXPLAINED_FIELD_NUMBER: _ClassVar[int]
    FAILED_FIELD_NUMBER: _ClassVar[int]
    FAILURES_FIELD_NUMBER: _ClassVar[int]
    FINISHED_FIELD_NUMBER: _ClassVar[int]
    INITIAL_QUEUE_TIME_FIELD_NUMBER: _ClassVar[int]
    INPUT_SIZE_FIELD_NUMBER: _ClassVar[int]
    JOB_IDENTIFIER_FIELD_NUMBER: _ClassVar[int]
    RESULTS_FIELD_NUMBER: _ClassVar[int]
    RESULT_SUMMARIZING_FIELD_NUMBER: _ClassVar[int]
    STARTING_RESULT_SUMMARIZING_FIELD_NUMBER: _ClassVar[int]
    SUBMITTED_AT_FIELD_NUMBER: _ClassVar[int]
    SUBMITTED_BY_KEY_FIELD_NUMBER: _ClassVar[int]
    TEAM_FIELD_NUMBER: _ClassVar[int]
    TOTAL_FIELD_NUMBER: _ClassVar[int]
    TOTAL_MODEL_LATENCY_FIELD_NUMBER: _ClassVar[int]
    TOTAL_QUEUE_TIME_FIELD_NUMBER: _ClassVar[int]
    account_identifier: str
    average_model_latency: float
    completed: int
    elapsed_time: int
    explained: bool
    failed: int
    failures: _containers.MessageMap[str, _any_pb2.Any]
    finished: bool
    initial_queue_time: int
    input_size: int
    job_identifier: str
    result_summarizing: int
    results: _containers.MessageMap[str, Results.InputResult]
    starting_result_summarizing: _timestamp_pb2.Timestamp
    submitted_at: _timestamp_pb2.Timestamp
    submitted_by_key: str
    team: _accounting_pb2.TeamIdentifier
    total: int
    total_model_latency: float
    total_queue_time: int
    def __init__(self, job_identifier: _Optional[str] = ..., account_identifier: _Optional[str] = ..., team: _Optional[_Union[_accounting_pb2.TeamIdentifier, _Mapping]] = ..., total: _Optional[int] = ..., completed: _Optional[int] = ..., failed: _Optional[int] = ..., finished: bool = ..., submitted_by_key: _Optional[str] = ..., explained: bool = ..., submitted_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., initial_queue_time: _Optional[int] = ..., total_queue_time: _Optional[int] = ..., average_model_latency: _Optional[float] = ..., total_model_latency: _Optional[float] = ..., elapsed_time: _Optional[int] = ..., starting_result_summarizing: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., result_summarizing: _Optional[int] = ..., input_size: _Optional[int] = ..., results: _Optional[_Mapping[str, Results.InputResult]] = ..., failures: _Optional[_Mapping[str, _any_pb2.Any]] = ...) -> None: ...

class Voting(_message.Message):
    __slots__ = ["down", "up"]
    DOWN_FIELD_NUMBER: _ClassVar[int]
    UP_FIELD_NUMBER: _ClassVar[int]
    down: int
    up: int
    def __init__(self, up: _Optional[int] = ..., down: _Optional[int] = ...) -> None: ...
