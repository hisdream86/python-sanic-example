import sanic.exceptions

from enum import Enum


class APIError(sanic.exceptions.SanicException):
    class ErrorCode(Enum):
        UNDEFINED = 5000

    def __init__(
        self, msg="Server error", status=sanic.exceptions.ServerError.status_code, code=ErrorCode.UNDEFINED.value
    ):
        super().__init__(msg)
        self.status = status
        self.code = code
        self.msg = msg


class BadRequest(APIError):
    class ErrorCode(Enum):
        BAD_REQUEST = 4000
        INVALID_VALUE = 4001

    def __init__(self, msg="Invalid request", code=ErrorCode.BAD_REQUEST.value):
        super().__init__(msg, sanic.exceptions.InvalidUsage.status_code, code)


class NotFound(APIError):
    class ErrorCode(Enum):
        NOT_FOUND = 4040
        OBJECT_NOT_FOUND = 4041

    def __init__(self, msg="Resource does not exist", code=ErrorCode.NOT_FOUND.value):
        super().__init__(msg, sanic.exceptions.NotFound.status_code, code)


class InternalServerError(APIError):
    class ErrorCode(Enum):
        SERVER_ERROR = 5000

    def __init__(self, msg="Internal Server Error", code=ErrorCode.SERVER_ERROR.value):
        super().__init__(msg, sanic.exceptions.ServerError.status_code, code)
