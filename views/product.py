from sanic import response
from sanic.request import Request
from sanic.views import HTTPMethodView
from sanic_openapi import openapi

from middlewares import APIResponse
from models import Product
from controllers import ProductController
from api_models.product import ProductResponse, ProductListResponse
from api_models.base import ErrorResponse
from utils.model_to_schema import model_to_schema


class ProductsView(HTTPMethodView):
    @openapi.summary("Create a product")
    @openapi.body({"application/json": model_to_schema(Product)})
    @openapi.response(200, {"application/json": model_to_schema(ProductResponse)})
    @openapi.response("OTHERS", {"application/json": model_to_schema(ErrorResponse)})
    async def post(self, request: Request) -> response.HTTPResponse:
        data = request.json or {}
        product = await ProductController().create_product(**data)
        return APIResponse(product.dict())

    @openapi.summary("List products")
    @openapi.response(200, {"application/json": model_to_schema(ProductListResponse)})
    @openapi.response("OTHERS", {"application/json": model_to_schema(ErrorResponse)})
    async def get(self, request: Request) -> response.HTTPResponse:
        products = await ProductController().list_products()
        return APIResponse(data=[product.dict() for product in products])


class ProductView(HTTPMethodView):
    @openapi.summary("Get a product")
    @openapi.response(200, {"application/json": model_to_schema(ProductResponse)})
    @openapi.response("OTHERS", {"application/json": model_to_schema(ErrorResponse)})
    async def get(self, request: Request, product_name: str) -> response.HTTPResponse:
        product = await ProductController().get_product(product_name)
        return APIResponse(product.dict())

    @openapi.summary("Update a product")
    @openapi.body({"application/json": model_to_schema(Product)})
    @openapi.response(200, {"application/json": model_to_schema(ProductResponse)})
    @openapi.response("OTHERS", {"application/json": model_to_schema(ErrorResponse)})
    async def put(self, request: Request, product_name: str) -> response.HTTPResponse:
        data = request.json or {}
        data = dict(filter(lambda item: item[0] != "name", data.items()))
        product = await ProductController().update_product(name=product_name, **data)
        return APIResponse(product.dict())

    @openapi.summary("Delete a product")
    @openapi.response(200, {"application/json": model_to_schema(ProductResponse)})
    @openapi.response("OTHERS", {"application/json": model_to_schema(ErrorResponse)})
    async def delete(self, request: Request, product_name: str) -> response.HTTPResponse:
        await ProductController().delete_product(name=product_name)
        return APIResponse()
