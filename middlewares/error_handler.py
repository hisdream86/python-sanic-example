import time
import uuid

from sanic import response
from sanic.request import Request
from sanic.exceptions import SanicException, ServerError
from errors import APIError
from utils import logger


async def handle_error(request: Request, error: Exception):
    if isinstance(error, APIError):
        status = error.status
        code = error.code
        error = error.msg

    elif isinstance(error, SanicException):
        if not hasattr(request.ctx, "request_id"):
            request.ctx.request_id = request.headers.get("request-id") or str(uuid.uuid4())
        if not hasattr(request.ctx, "start"):
            request.ctx.start = time.time()
        status = error.status_code
        code = status * 10
        error = str(error)

    else:
        status = ServerError.status_code
        code = APIError.ErrorCode.UNDEFINED.value
        error = str(error)

    if status >= ServerError.status_code:
        logger.error("Error", error, request)

    return response.json({"error": error, "code": code}, status=status)
