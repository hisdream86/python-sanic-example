from sanic.views import HTTPMethodView
from sanic.request import Request
from sanic.response import empty

from middlewares.response import log_response_body


class PingView(HTTPMethodView):
    decorator = [log_response_body(False)]

    async def post(self, request: Request):
        return empty(status=200)

    async def get(self, request: Request):
        return empty(status=200)
