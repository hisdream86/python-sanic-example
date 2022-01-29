from sqlalchemy import select, func
from sqlalchemy.exc import IntegrityError
from models import Product, PagedProductList
from errors import BadRequest
from database import Database, dberror
from database.orm import ProductOrm
from errors import NotFound


class ProductController:
    async def create_product(self, name: str = None, price: int = None, description: str = None, **kwargs) -> Product:
        async with Database().async_session() as session:
            product = ProductOrm(name=name, price=price, description=description)
            try:
                async with session.begin():
                    session.add(product)
            except IntegrityError as e:
                if dberror.is_unique_violation(e):
                    raise BadRequest(f"Product '{name}' already exist")

            await session.refresh(product)

            return Product(**product.__dict__)

    async def list_products(self, page: int = 0, page_size: int = 10) -> PagedProductList:
        async with Database().async_session() as session:
            async with session.begin():
                products = (
                    (
                        await session.execute(
                            select(ProductOrm).order_by(ProductOrm.created_at).limit(page_size).offset(page)
                        )
                    )
                    .scalars()
                    .all()
                )
                total_counts = (await session.execute(select(func.count(ProductOrm.product_id)))).scalar()
                total_pages = (total_counts // page_size) + 1

            return PagedProductList(
                items=[Product(**product.__dict__) for product in products],
                page=page,
                total_pages=total_pages,
            )

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
