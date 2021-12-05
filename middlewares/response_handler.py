import json

from sanic.compat import Header
from sanic.request import Request
from sanic.response import HTTPResponse
from typing import Dict, Optional, Union
from utils import logger

__DISABLE_BODY_LOG_ROUTES = [
    "swagger",
]


async def handle_response(request: Request, response: HTTPResponse):
    # For ignore non-http requests
    if hasattr(request.ctx, "ping"):
        return

    write_body = True
    for route in __DISABLE_BODY_LOG_ROUTES:
        if request.route and request.route.path.startswith(route):
            write_body = False
            break

    logger.response(request, response, write_body)


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
