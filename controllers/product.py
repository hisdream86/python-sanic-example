from models import Product
from errors import BadRequest, NotFound
from typing import Dict, List

_PRODUCT_DB: Dict[str, Product] = {}


class ProductController:
    async def create_product(self, name: str = None, price: int = None, description: str = None, **kwargs) -> Product:
        product = Product(name=name, price=price, description=description)
        if _PRODUCT_DB.get(product.name):
            raise BadRequest(f"Product {product.name} is already registered")
        _PRODUCT_DB[name] = product
        return _PRODUCT_DB[name]

    async def list_products(self) -> List[Product]:
        return [product for product in _PRODUCT_DB.values()]

    async def get_product(self, name: str) -> Product:
        product = _PRODUCT_DB.get(name)
        if not product:
            raise NotFound()
        return product

    async def update_product(self, name: str, price: int = None, description: str = None, **kwargs) -> Product:
        product = self.get_product(name)

        if price is not None:
            product.price = price

        if description is not None:
            product.description = description

        return product

    async def delete_product(self, name: str) -> None:
        if _PRODUCT_DB.get(name):
            del _PRODUCT_DB[name]
        else:
            raise NotFound()
