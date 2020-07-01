# -*- coding: utf-8 -*-
"""Package specific exceptions."""


class Error(Exception):
    """Base class for all Modzy exceptions.

    Attributes:
        message (str): Human readable error description.
    """

    def __init__(self, message):
        """Creates an `Error` instance.

        Args:
            message (str): Human readable error description.
        """
        super().__init__(message)
        self.message = str(message)


class ApiError(Error):
    """Base class for errors related to communication with the API.

    Attributes:
        message (str): Human readable error description.
        url (str): The API URL.
        reason (Optional[Exception]): The source exception. May be None.
    """

    def __init__(self, message, url, reason=None):
        """Creates an `ApiError` instance.

        Args:
            message (str): Human readable error description.
            url (str): The API URL.
            reason (Optional[Exception]): The source exception. Defaults to None.
        """
        super().__init__(message)
        self.url = url
        self.reason = reason


class NetworkError(ApiError):
    """Error connecting to the API over the network."""


class ResponseError(ApiError):
    """Base class for HTTP error responses.

    Attributes:
        message (str): Human readable error description.
        url (str): The API URL.
        response (requests.Response): The requests `Response` object.
    """

    def __init__(self, message, url, response):
        """Creates a `ResponseError` instance.

        Args:
            message (str): Human readable error description.
            url (str): The API URL.
            response (requests.Response): The requests `Response` object.
        """
        super().__init__(message, url)
        self.response = response


class ClientError(ResponseError):  # 4xx
    """Base class for all HTTP 4xx Client Errors."""


class BadRequestError(ClientError):  # 400
    """HTTP 400 Bad Request Error.

    Raised if the client sends something that the API cannot or will not handle.
    """


class UnauthorizedError(ClientError):  # 401
    """HTTP 401 Unauthorized Error.

    Raised if the access key is not authorized to access the API.
    """


class ForbiddenError(ClientError):  # 403
    """HTTP 403 Forbidden Error.

    Raised if the access key doesn't have the permission for the requested action
    but was authenticated.
    """


class NotFoundError(ClientError):  # 404
    """HTTP 404 Not Found Error.

    Raised if a resource does not exist.
    """


class MethodNotAllowedError(ClientError):  # 405
    """HTTP 405 Method Not Allowed Error.

    Raised if the client used a method the API does not handle. For
    example `POST` if the resource is view only.
    """


class NotAcceptableError(ClientError):  # 406
    """HTTP 406 Not Acceptable Error.

    Raised if the API can't return any content conforming to the
    `Accept` headers of the client.
    """


class ConflictError(ClientError):  # 409
    """HTTP 409 Conflict Error.

    Raised to signal that a request cannot be completed because it conflicts
    with the current API state.
    """


class RequestEntityTooLargeError(ClientError):  # 413
    """HTTP 413 Request Entity Too Large Error.

    Raised if the data submitted exceeded the limit.
    """


class UnprocessableEntityError(ClientError):  # 422
    """HTTP 422 Unprocessable Entity Error.

    Raised if the API was able to understand the request but was unable
    to process the request.
    """


class ServerError(ResponseError):  # 5xx
    """Base class for all HTTP 5xx Client Errors."""


class InternalServerError(ServerError):  # 500
    """HTTP 500 Internal Server Error."""


_response_error_classes = {
    400: BadRequestError,
    401: UnauthorizedError,
    403: ForbiddenError,
    404: NotFoundError,
    405: MethodNotAllowedError,
    406: NotAcceptableError,
    409: ConflictError,
    413: RequestEntityTooLargeError,
    422: UnprocessableEntityError,
    500: InternalServerError,
}


def _create_response_error(message, url, response):
    code = response.status_code
    error_class = _response_error_classes.get(code)
    if error_class:
        return error_class(message, url, response)
    if 400 <= code < 500:
        return ClientError(message, url, response)
    if 500 <= code < 600:
        return ServerError(message, url, response)
    return ResponseError(message, url, response)  # ?


class ResultsError(Error):  # name?
    """Model run failed for a given input source."""


class Timeout(Error):
    """A blocking function timed out."""
