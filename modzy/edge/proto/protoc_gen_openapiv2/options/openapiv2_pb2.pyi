from google.protobuf import struct_pb2 as _struct_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor
HTTP: Scheme
HTTPS: Scheme
UNKNOWN: Scheme
WS: Scheme
WSS: Scheme

class Contact(_message.Message):
    __slots__ = ["email", "name", "url"]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    URL_FIELD_NUMBER: _ClassVar[int]
    email: str
    name: str
    url: str
    def __init__(self, name: _Optional[str] = ..., url: _Optional[str] = ..., email: _Optional[str] = ...) -> None: ...

class ExternalDocumentation(_message.Message):
    __slots__ = ["description", "url"]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    URL_FIELD_NUMBER: _ClassVar[int]
    description: str
    url: str
    def __init__(self, description: _Optional[str] = ..., url: _Optional[str] = ...) -> None: ...

class Header(_message.Message):
    __slots__ = ["default", "description", "format", "pattern", "type"]
    DEFAULT_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    FORMAT_FIELD_NUMBER: _ClassVar[int]
    PATTERN_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    default: str
    description: str
    format: str
    pattern: str
    type: str
    def __init__(self, description: _Optional[str] = ..., type: _Optional[str] = ..., format: _Optional[str] = ..., default: _Optional[str] = ..., pattern: _Optional[str] = ...) -> None: ...

class HeaderParameter(_message.Message):
    __slots__ = ["description", "format", "name", "required", "type"]
    class Type(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    BOOLEAN: HeaderParameter.Type
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    FORMAT_FIELD_NUMBER: _ClassVar[int]
    INTEGER: HeaderParameter.Type
    NAME_FIELD_NUMBER: _ClassVar[int]
    NUMBER: HeaderParameter.Type
    REQUIRED_FIELD_NUMBER: _ClassVar[int]
    STRING: HeaderParameter.Type
    TYPE_FIELD_NUMBER: _ClassVar[int]
    UNKNOWN: HeaderParameter.Type
    description: str
    format: str
    name: str
    required: bool
    type: HeaderParameter.Type
    def __init__(self, name: _Optional[str] = ..., description: _Optional[str] = ..., type: _Optional[_Union[HeaderParameter.Type, str]] = ..., format: _Optional[str] = ..., required: bool = ...) -> None: ...

class Info(_message.Message):
    __slots__ = ["contact", "description", "extensions", "license", "terms_of_service", "title", "version"]
    class ExtensionsEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: _struct_pb2.Value
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[_struct_pb2.Value, _Mapping]] = ...) -> None: ...
    CONTACT_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    EXTENSIONS_FIELD_NUMBER: _ClassVar[int]
    LICENSE_FIELD_NUMBER: _ClassVar[int]
    TERMS_OF_SERVICE_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    contact: Contact
    description: str
    extensions: _containers.MessageMap[str, _struct_pb2.Value]
    license: License
    terms_of_service: str
    title: str
    version: str
    def __init__(self, title: _Optional[str] = ..., description: _Optional[str] = ..., terms_of_service: _Optional[str] = ..., contact: _Optional[_Union[Contact, _Mapping]] = ..., license: _Optional[_Union[License, _Mapping]] = ..., version: _Optional[str] = ..., extensions: _Optional[_Mapping[str, _struct_pb2.Value]] = ...) -> None: ...

class JSONSchema(_message.Message):
    __slots__ = ["array", "default", "description", "enum", "example", "exclusive_maximum", "exclusive_minimum", "extensions", "field_configuration", "format", "max_items", "max_length", "max_properties", "maximum", "min_items", "min_length", "min_properties", "minimum", "multiple_of", "pattern", "read_only", "ref", "required", "title", "type", "unique_items"]
    class JSONSchemaSimpleTypes(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    class ExtensionsEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: _struct_pb2.Value
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[_struct_pb2.Value, _Mapping]] = ...) -> None: ...
    class FieldConfiguration(_message.Message):
        __slots__ = ["path_param_name"]
        PATH_PARAM_NAME_FIELD_NUMBER: _ClassVar[int]
        path_param_name: str
        def __init__(self, path_param_name: _Optional[str] = ...) -> None: ...
    ARRAY: JSONSchema.JSONSchemaSimpleTypes
    ARRAY_FIELD_NUMBER: _ClassVar[int]
    BOOLEAN: JSONSchema.JSONSchemaSimpleTypes
    DEFAULT_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    ENUM_FIELD_NUMBER: _ClassVar[int]
    EXAMPLE_FIELD_NUMBER: _ClassVar[int]
    EXCLUSIVE_MAXIMUM_FIELD_NUMBER: _ClassVar[int]
    EXCLUSIVE_MINIMUM_FIELD_NUMBER: _ClassVar[int]
    EXTENSIONS_FIELD_NUMBER: _ClassVar[int]
    FIELD_CONFIGURATION_FIELD_NUMBER: _ClassVar[int]
    FORMAT_FIELD_NUMBER: _ClassVar[int]
    INTEGER: JSONSchema.JSONSchemaSimpleTypes
    MAXIMUM_FIELD_NUMBER: _ClassVar[int]
    MAX_ITEMS_FIELD_NUMBER: _ClassVar[int]
    MAX_LENGTH_FIELD_NUMBER: _ClassVar[int]
    MAX_PROPERTIES_FIELD_NUMBER: _ClassVar[int]
    MINIMUM_FIELD_NUMBER: _ClassVar[int]
    MIN_ITEMS_FIELD_NUMBER: _ClassVar[int]
    MIN_LENGTH_FIELD_NUMBER: _ClassVar[int]
    MIN_PROPERTIES_FIELD_NUMBER: _ClassVar[int]
    MULTIPLE_OF_FIELD_NUMBER: _ClassVar[int]
    NULL: JSONSchema.JSONSchemaSimpleTypes
    NUMBER: JSONSchema.JSONSchemaSimpleTypes
    OBJECT: JSONSchema.JSONSchemaSimpleTypes
    PATTERN_FIELD_NUMBER: _ClassVar[int]
    READ_ONLY_FIELD_NUMBER: _ClassVar[int]
    REF_FIELD_NUMBER: _ClassVar[int]
    REQUIRED_FIELD_NUMBER: _ClassVar[int]
    STRING: JSONSchema.JSONSchemaSimpleTypes
    TITLE_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    UNIQUE_ITEMS_FIELD_NUMBER: _ClassVar[int]
    UNKNOWN: JSONSchema.JSONSchemaSimpleTypes
    array: _containers.RepeatedScalarFieldContainer[str]
    default: str
    description: str
    enum: _containers.RepeatedScalarFieldContainer[str]
    example: str
    exclusive_maximum: bool
    exclusive_minimum: bool
    extensions: _containers.MessageMap[str, _struct_pb2.Value]
    field_configuration: JSONSchema.FieldConfiguration
    format: str
    max_items: int
    max_length: int
    max_properties: int
    maximum: float
    min_items: int
    min_length: int
    min_properties: int
    minimum: float
    multiple_of: float
    pattern: str
    read_only: bool
    ref: str
    required: _containers.RepeatedScalarFieldContainer[str]
    title: str
    type: _containers.RepeatedScalarFieldContainer[JSONSchema.JSONSchemaSimpleTypes]
    unique_items: bool
    def __init__(self, ref: _Optional[str] = ..., title: _Optional[str] = ..., description: _Optional[str] = ..., default: _Optional[str] = ..., read_only: bool = ..., example: _Optional[str] = ..., multiple_of: _Optional[float] = ..., maximum: _Optional[float] = ..., exclusive_maximum: bool = ..., minimum: _Optional[float] = ..., exclusive_minimum: bool = ..., max_length: _Optional[int] = ..., min_length: _Optional[int] = ..., pattern: _Optional[str] = ..., max_items: _Optional[int] = ..., min_items: _Optional[int] = ..., unique_items: bool = ..., max_properties: _Optional[int] = ..., min_properties: _Optional[int] = ..., required: _Optional[_Iterable[str]] = ..., array: _Optional[_Iterable[str]] = ..., type: _Optional[_Iterable[_Union[JSONSchema.JSONSchemaSimpleTypes, str]]] = ..., format: _Optional[str] = ..., enum: _Optional[_Iterable[str]] = ..., field_configuration: _Optional[_Union[JSONSchema.FieldConfiguration, _Mapping]] = ..., extensions: _Optional[_Mapping[str, _struct_pb2.Value]] = ...) -> None: ...

class License(_message.Message):
    __slots__ = ["name", "url"]
    NAME_FIELD_NUMBER: _ClassVar[int]
    URL_FIELD_NUMBER: _ClassVar[int]
    name: str
    url: str
    def __init__(self, name: _Optional[str] = ..., url: _Optional[str] = ...) -> None: ...

class Operation(_message.Message):
    __slots__ = ["consumes", "deprecated", "description", "extensions", "external_docs", "operation_id", "parameters", "produces", "responses", "schemes", "security", "summary", "tags"]
    class ExtensionsEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: _struct_pb2.Value
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[_struct_pb2.Value, _Mapping]] = ...) -> None: ...
    class ResponsesEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: Response
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[Response, _Mapping]] = ...) -> None: ...
    CONSUMES_FIELD_NUMBER: _ClassVar[int]
    DEPRECATED_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    EXTENSIONS_FIELD_NUMBER: _ClassVar[int]
    EXTERNAL_DOCS_FIELD_NUMBER: _ClassVar[int]
    OPERATION_ID_FIELD_NUMBER: _ClassVar[int]
    PARAMETERS_FIELD_NUMBER: _ClassVar[int]
    PRODUCES_FIELD_NUMBER: _ClassVar[int]
    RESPONSES_FIELD_NUMBER: _ClassVar[int]
    SCHEMES_FIELD_NUMBER: _ClassVar[int]
    SECURITY_FIELD_NUMBER: _ClassVar[int]
    SUMMARY_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    consumes: _containers.RepeatedScalarFieldContainer[str]
    deprecated: bool
    description: str
    extensions: _containers.MessageMap[str, _struct_pb2.Value]
    external_docs: ExternalDocumentation
    operation_id: str
    parameters: Parameters
    produces: _containers.RepeatedScalarFieldContainer[str]
    responses: _containers.MessageMap[str, Response]
    schemes: _containers.RepeatedScalarFieldContainer[Scheme]
    security: _containers.RepeatedCompositeFieldContainer[SecurityRequirement]
    summary: str
    tags: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, tags: _Optional[_Iterable[str]] = ..., summary: _Optional[str] = ..., description: _Optional[str] = ..., external_docs: _Optional[_Union[ExternalDocumentation, _Mapping]] = ..., operation_id: _Optional[str] = ..., consumes: _Optional[_Iterable[str]] = ..., produces: _Optional[_Iterable[str]] = ..., responses: _Optional[_Mapping[str, Response]] = ..., schemes: _Optional[_Iterable[_Union[Scheme, str]]] = ..., deprecated: bool = ..., security: _Optional[_Iterable[_Union[SecurityRequirement, _Mapping]]] = ..., extensions: _Optional[_Mapping[str, _struct_pb2.Value]] = ..., parameters: _Optional[_Union[Parameters, _Mapping]] = ...) -> None: ...

class Parameters(_message.Message):
    __slots__ = ["headers"]
    HEADERS_FIELD_NUMBER: _ClassVar[int]
    headers: _containers.RepeatedCompositeFieldContainer[HeaderParameter]
    def __init__(self, headers: _Optional[_Iterable[_Union[HeaderParameter, _Mapping]]] = ...) -> None: ...

class Response(_message.Message):
    __slots__ = ["description", "examples", "extensions", "headers", "schema"]
    class ExamplesEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    class ExtensionsEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: _struct_pb2.Value
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[_struct_pb2.Value, _Mapping]] = ...) -> None: ...
    class HeadersEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: Header
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[Header, _Mapping]] = ...) -> None: ...
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    EXAMPLES_FIELD_NUMBER: _ClassVar[int]
    EXTENSIONS_FIELD_NUMBER: _ClassVar[int]
    HEADERS_FIELD_NUMBER: _ClassVar[int]
    SCHEMA_FIELD_NUMBER: _ClassVar[int]
    description: str
    examples: _containers.ScalarMap[str, str]
    extensions: _containers.MessageMap[str, _struct_pb2.Value]
    headers: _containers.MessageMap[str, Header]
    schema: Schema
    def __init__(self, description: _Optional[str] = ..., schema: _Optional[_Union[Schema, _Mapping]] = ..., headers: _Optional[_Mapping[str, Header]] = ..., examples: _Optional[_Mapping[str, str]] = ..., extensions: _Optional[_Mapping[str, _struct_pb2.Value]] = ...) -> None: ...

class Schema(_message.Message):
    __slots__ = ["discriminator", "example", "external_docs", "json_schema", "read_only"]
    DISCRIMINATOR_FIELD_NUMBER: _ClassVar[int]
    EXAMPLE_FIELD_NUMBER: _ClassVar[int]
    EXTERNAL_DOCS_FIELD_NUMBER: _ClassVar[int]
    JSON_SCHEMA_FIELD_NUMBER: _ClassVar[int]
    READ_ONLY_FIELD_NUMBER: _ClassVar[int]
    discriminator: str
    example: str
    external_docs: ExternalDocumentation
    json_schema: JSONSchema
    read_only: bool
    def __init__(self, json_schema: _Optional[_Union[JSONSchema, _Mapping]] = ..., discriminator: _Optional[str] = ..., read_only: bool = ..., external_docs: _Optional[_Union[ExternalDocumentation, _Mapping]] = ..., example: _Optional[str] = ...) -> None: ...

class Scopes(_message.Message):
    __slots__ = ["scope"]
    class ScopeEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    SCOPE_FIELD_NUMBER: _ClassVar[int]
    scope: _containers.ScalarMap[str, str]
    def __init__(self, scope: _Optional[_Mapping[str, str]] = ...) -> None: ...

class SecurityDefinitions(_message.Message):
    __slots__ = ["security"]
    class SecurityEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: SecurityScheme
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[SecurityScheme, _Mapping]] = ...) -> None: ...
    SECURITY_FIELD_NUMBER: _ClassVar[int]
    security: _containers.MessageMap[str, SecurityScheme]
    def __init__(self, security: _Optional[_Mapping[str, SecurityScheme]] = ...) -> None: ...

class SecurityRequirement(_message.Message):
    __slots__ = ["security_requirement"]
    class SecurityRequirementEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: SecurityRequirement.SecurityRequirementValue
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[SecurityRequirement.SecurityRequirementValue, _Mapping]] = ...) -> None: ...
    class SecurityRequirementValue(_message.Message):
        __slots__ = ["scope"]
        SCOPE_FIELD_NUMBER: _ClassVar[int]
        scope: _containers.RepeatedScalarFieldContainer[str]
        def __init__(self, scope: _Optional[_Iterable[str]] = ...) -> None: ...
    SECURITY_REQUIREMENT_FIELD_NUMBER: _ClassVar[int]
    security_requirement: _containers.MessageMap[str, SecurityRequirement.SecurityRequirementValue]
    def __init__(self, security_requirement: _Optional[_Mapping[str, SecurityRequirement.SecurityRequirementValue]] = ...) -> None: ...

class SecurityScheme(_message.Message):
    __slots__ = ["authorization_url", "description", "extensions", "flow", "name", "scopes", "token_url", "type"]
    class Flow(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    class In(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    class Type(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    class ExtensionsEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: _struct_pb2.Value
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[_struct_pb2.Value, _Mapping]] = ...) -> None: ...
    AUTHORIZATION_URL_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    EXTENSIONS_FIELD_NUMBER: _ClassVar[int]
    FLOW_ACCESS_CODE: SecurityScheme.Flow
    FLOW_APPLICATION: SecurityScheme.Flow
    FLOW_FIELD_NUMBER: _ClassVar[int]
    FLOW_IMPLICIT: SecurityScheme.Flow
    FLOW_INVALID: SecurityScheme.Flow
    FLOW_PASSWORD: SecurityScheme.Flow
    IN_FIELD_NUMBER: _ClassVar[int]
    IN_HEADER: SecurityScheme.In
    IN_INVALID: SecurityScheme.In
    IN_QUERY: SecurityScheme.In
    NAME_FIELD_NUMBER: _ClassVar[int]
    SCOPES_FIELD_NUMBER: _ClassVar[int]
    TOKEN_URL_FIELD_NUMBER: _ClassVar[int]
    TYPE_API_KEY: SecurityScheme.Type
    TYPE_BASIC: SecurityScheme.Type
    TYPE_FIELD_NUMBER: _ClassVar[int]
    TYPE_INVALID: SecurityScheme.Type
    TYPE_OAUTH2: SecurityScheme.Type
    authorization_url: str
    description: str
    extensions: _containers.MessageMap[str, _struct_pb2.Value]
    flow: SecurityScheme.Flow
    name: str
    scopes: Scopes
    token_url: str
    type: SecurityScheme.Type
    def __init__(self, type: _Optional[_Union[SecurityScheme.Type, str]] = ..., description: _Optional[str] = ..., name: _Optional[str] = ..., flow: _Optional[_Union[SecurityScheme.Flow, str]] = ..., authorization_url: _Optional[str] = ..., token_url: _Optional[str] = ..., scopes: _Optional[_Union[Scopes, _Mapping]] = ..., extensions: _Optional[_Mapping[str, _struct_pb2.Value]] = ..., **kwargs) -> None: ...

class Swagger(_message.Message):
    __slots__ = ["base_path", "consumes", "extensions", "external_docs", "host", "info", "produces", "responses", "schemes", "security", "security_definitions", "swagger", "tags"]
    class ExtensionsEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: _struct_pb2.Value
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[_struct_pb2.Value, _Mapping]] = ...) -> None: ...
    class ResponsesEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: Response
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[Response, _Mapping]] = ...) -> None: ...
    BASE_PATH_FIELD_NUMBER: _ClassVar[int]
    CONSUMES_FIELD_NUMBER: _ClassVar[int]
    EXTENSIONS_FIELD_NUMBER: _ClassVar[int]
    EXTERNAL_DOCS_FIELD_NUMBER: _ClassVar[int]
    HOST_FIELD_NUMBER: _ClassVar[int]
    INFO_FIELD_NUMBER: _ClassVar[int]
    PRODUCES_FIELD_NUMBER: _ClassVar[int]
    RESPONSES_FIELD_NUMBER: _ClassVar[int]
    SCHEMES_FIELD_NUMBER: _ClassVar[int]
    SECURITY_DEFINITIONS_FIELD_NUMBER: _ClassVar[int]
    SECURITY_FIELD_NUMBER: _ClassVar[int]
    SWAGGER_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    base_path: str
    consumes: _containers.RepeatedScalarFieldContainer[str]
    extensions: _containers.MessageMap[str, _struct_pb2.Value]
    external_docs: ExternalDocumentation
    host: str
    info: Info
    produces: _containers.RepeatedScalarFieldContainer[str]
    responses: _containers.MessageMap[str, Response]
    schemes: _containers.RepeatedScalarFieldContainer[Scheme]
    security: _containers.RepeatedCompositeFieldContainer[SecurityRequirement]
    security_definitions: SecurityDefinitions
    swagger: str
    tags: _containers.RepeatedCompositeFieldContainer[Tag]
    def __init__(self, swagger: _Optional[str] = ..., info: _Optional[_Union[Info, _Mapping]] = ..., host: _Optional[str] = ..., base_path: _Optional[str] = ..., schemes: _Optional[_Iterable[_Union[Scheme, str]]] = ..., consumes: _Optional[_Iterable[str]] = ..., produces: _Optional[_Iterable[str]] = ..., responses: _Optional[_Mapping[str, Response]] = ..., security_definitions: _Optional[_Union[SecurityDefinitions, _Mapping]] = ..., security: _Optional[_Iterable[_Union[SecurityRequirement, _Mapping]]] = ..., tags: _Optional[_Iterable[_Union[Tag, _Mapping]]] = ..., external_docs: _Optional[_Union[ExternalDocumentation, _Mapping]] = ..., extensions: _Optional[_Mapping[str, _struct_pb2.Value]] = ...) -> None: ...

class Tag(_message.Message):
    __slots__ = ["description", "extensions", "external_docs", "name"]
    class ExtensionsEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: _struct_pb2.Value
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[_struct_pb2.Value, _Mapping]] = ...) -> None: ...
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    EXTENSIONS_FIELD_NUMBER: _ClassVar[int]
    EXTERNAL_DOCS_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    description: str
    extensions: _containers.MessageMap[str, _struct_pb2.Value]
    external_docs: ExternalDocumentation
    name: str
    def __init__(self, name: _Optional[str] = ..., description: _Optional[str] = ..., external_docs: _Optional[_Union[ExternalDocumentation, _Mapping]] = ..., extensions: _Optional[_Mapping[str, _struct_pb2.Value]] = ...) -> None: ...

class Scheme(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
