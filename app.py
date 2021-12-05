import os

from sanic import Sanic
from sanic_openapi import openapi3_blueprint

from configs import config
from listeners import init, finish, setup_options
from middlewares import handle_request, handle_response, handle_error, cors

from views import product

SANIC_MIDDLEWARE_REQUEST = "request"
SANIC_MIDDLEWARE_RESPONSE = "response"
SANIC_LISTENER_BEFORE_SERVER_START = "before_server_start"
SANIC_LISTENER_AFTER_SERVER_START = "after_server_start"
SANIC_LISTENER_BEFORE_SERVER_STOP = "before_server_stop"
SANIC_LISTENER_AFTER_SERVER_STOP = "after_server_stop"

_API_DESCRIPTION = """
Write your application description here
"""


def create_app():
    app = Sanic(config.APP_NAME, log_config=config.LOGGING_CONFIG)

    # Set open api configuration
    app.blueprint(openapi3_blueprint)
    app.config.API_TITLE = config.APP_NAME
    app.config.API_VERSION = config.APP_VERSION
    app.config.API_DESCRIPTION = _API_DESCRIPTION

    # Register listeners
    app.register_listener(init, SANIC_LISTENER_BEFORE_SERVER_START)
    app.register_listener(finish, SANIC_LISTENER_AFTER_SERVER_STOP)

    # Register middlewares
    app.register_middleware(cors, SANIC_MIDDLEWARE_RESPONSE)
    app.register_middleware(handle_request, SANIC_MIDDLEWARE_REQUEST)
    app.register_middleware(handle_response, SANIC_MIDDLEWARE_RESPONSE)

    # Add error handlers
    app.error_handler.add(Exception, handle_error)

    # Add routes
    app.add_route(product.ProductsView.as_view(), "/api/v1/products")
    app.add_route(product.ProductView.as_view(), "/api/v1/products/<product_name>")

    # Set options methods for configuring CORS
    if not os.getenv("PYTEST_CURRENT_TEST"):
        app.register_listener(setup_options, SANIC_LISTENER_BEFORE_SERVER_START)

    return app
