from sanic.request import Request
from sanic.response import HTTPResponse

from configs import config


def cors(request: Request, response: HTTPResponse):
    if request.method == "OPTIONS":
        return

    if (origin := request.headers.get("origin")) in config.ALLOWED_ORIGINS:
        headers = {
            "Access-Control-Allow-Origin": origin,
            "Access-Control-Allow-Credentials": "true",
        }
        response.headers.extend(headers)
