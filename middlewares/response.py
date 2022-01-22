import json

from functools import wraps
from sanic.compat import Header
from sanic.request import Request
from sanic.response import HTTPResponse
from typing import Dict, Optional, Union
from utils import logger


def log_response_body(enabled: bool = True):
    def decorator(f):
        @wraps(f)
        async def decorated(request: Request, *args, **kwargs):
            request.ctx.log_response_body = enabled
            return f(request, *args, **kwargs)

        return decorated

    return decorator


async def default_response_middleware(request: Request, response: HTTPResponse):
    logger.response(request, response, hasattr(request.ctx, "log_response_body") and request.ctx.log_response_body)


class APIResponse(HTTPResponse):
    def __init__(self, data: dict = None, headers: Optional[Union[Header, Dict[str, str]]] = None):
        response = {
            "code": 2001,
            **({"data": data} if data is not None else {}),
        }

        super().__init__(
            body=json.dumps(response, default=str, ensure_ascii=False),
            status=200,
            headers=headers,
            content_type="application/json;charset=utf-8",
        )


class PagedAPIResponse(HTTPResponse):
    def __init__(
        self,
        data: dict = None,
        pagination: Dict[str, int] = None,
        headers: Optional[Union[Header, Dict[str, str]]] = None,
    ):
        response = {
            "code": 2001,
            "pagination": pagination,
            **({"data": data} if data is not None else {}),
        }

        super().__init__(
            body=json.dumps(
                response,
                default=str,
            ),
            status=200,
            headers=headers,
            content_type="application/json",
        )
