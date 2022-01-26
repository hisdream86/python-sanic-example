from sqlalchemy import select
from models import Product
from database import Database
from database.orm import ProductOrm
from errors import NotFound
from typing import Dict, List

_PRODUCT_DB: Dict[str, Product] = {}


class ProductController:
    async def create_product(self, name: str = None, price: int = None, description: str = None, **kwargs) -> Product:
        async with Database().async_session() as session:
            product = ProductOrm(name=name, price=price, description=description)
            async with session.begin():
                session.add(product)

            await session.refresh(product)

            return Product(**product.__dict__)

    async def list_products(self) -> List[Product]:
        async with Database().async_session() as session:
            stmt = select(ProductOrm).order_by(ProductOrm.created_at)
            products = (await session.execute(stmt)).scalars().all()
            return [Product(**product.__dict__) for product in products]

    async def get_product(self, name: str) -> Product:
        async with Database().async_session() as session:
            product = (
                await session.execute(select(ProductOrm).filter_by(name=name).order_by(ProductOrm.created_at))
            ).scalar()

            return Product(**product.__dict__)

    async def update_product(self, name: str, price: int = None, description: str = None, **kwargs) -> Product:
        async with Database().async_session() as session:
            async with session.begin():
                stmt = select(ProductOrm).where(ProductOrm.name == name)
                product = (await session.execute(stmt)).scalar()

                if not product:
                    raise NotFound(f"Product '{name}' does not exist")

                product.price = price if price is not None else product.price
                product.description = description if description is not None else product.description
                session.add(product)

            await session.refresh(product)

            return Product(**product.__dict__)

    async def delete_product(self, name: str) -> None:
        async with Database().async_session() as session:
            async with session.begin():
                stmt = select(ProductOrm).where(ProductOrm.name == name)
                product = (await session.execute(stmt)).scalar()

                if not product:
                    raise NotFound(f"Product '{name}' does not exist")

                await session.delete(product)
