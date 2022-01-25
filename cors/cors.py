from collections import defaultdict
from typing import Callable, Dict, FrozenSet, Iterable
from sanic import Sanic
from sanic.request import Request
from sanic.response import empty, HTTPResponse
from sanic.router import Route

from config import config


def _compile_routes_needing_options(routes: Dict[str, Route]) -> Dict[str, FrozenSet]:
    needs_options = defaultdict(list)
    for route in routes:
        for method in route.methods:
            if "OPTIONS" not in route.methods:
                uri = route.uri[:-1] if route.uri.endswith("/") else route.uri
                needs_options[uri].extend([method])
    return {uri: frozenset(methods) for uri, methods in dict(needs_options).items()}


def _options_wrapper(handler: Callable, methods: Iterable[str]):
    def wrapped_handler(request: Request, *args, **kwargs):
        nonlocal methods
        return handler(request, methods)

    return wrapped_handler


async def _options_handler(request: Request, methods: Iterable[str]) -> HTTPResponse:
    response = empty()

    allow_methods = list(set(methods))

    if "OPTIONS" not in allow_methods:
        allow_methods.append("OPTIONS")

    if (origin := request.headers.get("origin")) in config.ALLOWED_ORIGINS:
        response.headers.extend(
            {
                "Access-Control-Allow-Methods": ",".join(allow_methods),
                "Access-Control-Allow-Origin": origin,
                "Access-Control-Allow-Credentials": "true",
                "Access-Control-Allow-Headers": "Accept, Accept-Encoding, Content-Type, DNT, Origin, User-Agent, X-Csrftoken, X-Requested-With, Cache, Authorization",
            }
        )

    return response


def setup_options(app: Sanic, _):
    app.router.reset()
    needs_options = _compile_routes_needing_options(app.router.routes)
    for uri, methods in needs_options.items():
        app.add_route(_options_wrapper(_options_handler, methods), uri, methods=["OPTIONS"])
    app.router.finalize()


def cors(request: Request, response: HTTPResponse):
    if request.method == "OPTIONS":
        return

    if (origin := request.headers.get("origin")) in config.ALLOWED_ORIGINS:
        headers = {
            "Access-Control-Allow-Origin": origin,
            "Access-Control-Allow-Credentials": "true",
        }
        response.headers.extend(headers)
