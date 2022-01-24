from sqlalchemy import Column, TIMESTAMP
from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy.sql import func


@as_declarative()
class BaseOrm:
    __abstrace__ = True

    created_at = Column("created_at", TIMESTAMP(timezone=False), nullable=False, server_default=func.now())
    updated_at = Column("updated_at", TIMESTAMP(timezone=False), nullable=False, server_default=func.now())

    __mapper_args__ = {"eager_defaults": True}
