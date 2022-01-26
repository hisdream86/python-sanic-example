import os

from sanic import Sanic
from sanic_openapi import openapi3_blueprint
from uvloop import Loop
from clients import HTTPBaseClient
from cors import cors, setup_options
from config import config
from middlewares import default_request_middleware, default_response_middleware, handle_error
from views import ping, product

_SANIC_MIDDLEWARE_REQUEST = "request"
_SANIC_MIDDLEWARE_RESPONSE = "response"
_SANIC_LISTENER_BEFORE_SERVER_START = "before_server_start"
_SANIC_LISTENER_BEFORE_SERVER_STOP = "before_server_stop"


class App(Sanic):
    def __init__(self):
        super().__init__(config.APP_NAME, log_config=config.LOG_CONFIG)

        self.blueprint(openapi3_blueprint)
        self.config.API_TITLE = config.APP_NAME
        self.config.API_VERSION = config.APP_VERSION
        self.config.API_DESCRIPTION = "Hello World"

        self.setup_listeners()
        self.setup_middlewares()
        self.setup_routes()

    def setup_listeners(self):
        self.register_listener(_listener_init, _SANIC_LISTENER_BEFORE_SERVER_START)
        self.register_listener(_listener_finish, _SANIC_LISTENER_BEFORE_SERVER_STOP)
        if not os.getenv("PYTEST_CURRENT_TEST"):
            self.register_listener(setup_options, _SANIC_LISTENER_BEFORE_SERVER_START)

    def setup_middlewares(self):
        self.register_middleware(default_request_middleware, _SANIC_MIDDLEWARE_REQUEST)
        self.register_middleware(default_response_middleware, _SANIC_MIDDLEWARE_RESPONSE)
        self.register_middleware(cors, _SANIC_MIDDLEWARE_RESPONSE)
        self.error_handler.add(Exception, handle_error)

    def setup_routes(self):
        self.add_route(ping.PingView.as_view(), "/")
        self.add_route(product.ProductsView.as_view(), "/api/v1/products")
        self.add_route(product.ProductView.as_view(), "/api/v1/products/<product_name>")


async def _listener_init(app: Sanic, loop: Loop) -> None:
    HTTPBaseClient.create_session()


async def _listener_finish(app: Sanic, loop: Loop) -> None:
    await HTTPBaseClient.close_session()
