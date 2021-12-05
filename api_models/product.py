from typing import List
from models import Product
from .base import BaseResponse


class ProductResponse(BaseResponse):
    data: Product


class ProductListResponse(BaseResponse):
    data: List[Product]
