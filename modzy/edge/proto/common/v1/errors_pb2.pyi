from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class Error(_message.Message):
    __slots__ = ["message", "report_error_url", "status", "status_code"]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    REPORT_ERROR_URL_FIELD_NUMBER: _ClassVar[int]
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    message: str
    report_error_url: str
    status: str
    status_code: int
    def __init__(self, message: _Optional[str] = ..., report_error_url: _Optional[str] = ..., status: _Optional[str] = ..., status_code: _Optional[int] = ...) -> None: ...
