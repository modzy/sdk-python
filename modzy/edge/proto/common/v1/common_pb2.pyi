from google.api import field_behavior_pb2 as _field_behavior_pb2
from modzy.edge.proto.protoc_gen_openapiv2.options import annotations_pb2 as _annotations_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ListOptions(_message.Message):
    __slots__ = ["filters", "page", "sort"]
    class FiltersEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    class SortEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    FILTERS_FIELD_NUMBER: _ClassVar[int]
    PAGE_FIELD_NUMBER: _ClassVar[int]
    SORT_FIELD_NUMBER: _ClassVar[int]
    filters: _containers.ScalarMap[str, str]
    page: Pagination
    sort: _containers.ScalarMap[str, str]
    def __init__(self, filters: _Optional[_Mapping[str, str]] = ..., sort: _Optional[_Mapping[str, str]] = ..., page: _Optional[_Union[Pagination, _Mapping]] = ...) -> None: ...

class ModelAutoscalingConfig(_message.Message):
    __slots__ = ["maximum", "minimum", "model", "model_library_id"]
    MAXIMUM_FIELD_NUMBER: _ClassVar[int]
    MINIMUM_FIELD_NUMBER: _ClassVar[int]
    MODEL_FIELD_NUMBER: _ClassVar[int]
    MODEL_LIBRARY_ID_FIELD_NUMBER: _ClassVar[int]
    maximum: int
    minimum: int
    model: ModelIdentifier
    model_library_id: str
    def __init__(self, model: _Optional[_Union[ModelIdentifier, _Mapping]] = ..., minimum: _Optional[int] = ..., maximum: _Optional[int] = ..., model_library_id: _Optional[str] = ...) -> None: ...

class ModelIdentifier(_message.Message):
    __slots__ = ["identifier", "name", "version"]
    IDENTIFIER_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    identifier: str
    name: str
    version: str
    def __init__(self, identifier: _Optional[str] = ..., version: _Optional[str] = ..., name: _Optional[str] = ...) -> None: ...

class ModelLibrary(_message.Message):
    __slots__ = ["ca_certificate", "identifier", "name", "registry", "url"]
    CA_CERTIFICATE_FIELD_NUMBER: _ClassVar[int]
    IDENTIFIER_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    REGISTRY_FIELD_NUMBER: _ClassVar[int]
    URL_FIELD_NUMBER: _ClassVar[int]
    ca_certificate: str
    identifier: str
    name: str
    registry: Registry
    url: str
    def __init__(self, identifier: _Optional[str] = ..., url: _Optional[str] = ..., name: _Optional[str] = ..., ca_certificate: _Optional[str] = ..., registry: _Optional[_Union[Registry, _Mapping]] = ...) -> None: ...

class Page(_message.Message):
    __slots__ = ["number", "page_count", "size", "total_elements"]
    NUMBER_FIELD_NUMBER: _ClassVar[int]
    PAGE_COUNT_FIELD_NUMBER: _ClassVar[int]
    SIZE_FIELD_NUMBER: _ClassVar[int]
    TOTAL_ELEMENTS_FIELD_NUMBER: _ClassVar[int]
    number: int
    page_count: int
    size: int
    total_elements: int
    def __init__(self, number: _Optional[int] = ..., size: _Optional[int] = ..., page_count: _Optional[int] = ..., total_elements: _Optional[int] = ...) -> None: ...

class Pagination(_message.Message):
    __slots__ = ["number", "size"]
    NUMBER_FIELD_NUMBER: _ClassVar[int]
    SIZE_FIELD_NUMBER: _ClassVar[int]
    number: int
    size: int
    def __init__(self, number: _Optional[int] = ..., size: _Optional[int] = ...) -> None: ...

class Registry(_message.Message):
    __slots__ = ["credentials", "host", "port", "skip_tls_verify"]
    CREDENTIALS_FIELD_NUMBER: _ClassVar[int]
    HOST_FIELD_NUMBER: _ClassVar[int]
    PORT_FIELD_NUMBER: _ClassVar[int]
    SKIP_TLS_VERIFY_FIELD_NUMBER: _ClassVar[int]
    credentials: str
    host: str
    port: int
    skip_tls_verify: bool
    def __init__(self, host: _Optional[str] = ..., port: _Optional[int] = ..., credentials: _Optional[str] = ..., skip_tls_verify: bool = ...) -> None: ...
