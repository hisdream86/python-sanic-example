from sqlalchemy import Column, String, Integer
from sqlalchemy.dialects.postgresql import UUID
from database.orm.base import BaseOrm


class ProductOrm(BaseOrm):
    __tablename__ = "products"

    product_id = Column("product_id", UUID(as_uuid=True), primary_key=True)
    name = Column("name", String, nullable=False)
    description = Column("description", String, nullable=True)
    price = Column("price", Integer, nullable=False)
