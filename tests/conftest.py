import asyncio
import pytest
import json
import functools

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.pool import NullPool
from database import Database
from database.orm import BaseOrm


@pytest.fixture(autouse=True)
def loop_factory():
    return asyncio.get_event_loop


@pytest.fixture()
@pytest.mark.asyncio
async def mock_database(mocker, postgresql):
    mock_conn_url = f"postgresql+asyncpg://{postgresql.info.user}:@{postgresql.info.host}:{postgresql.info.port}/{postgresql.info.dbname}"
    engine = create_async_engine(
        mock_conn_url,
        echo=False,
        json_serializer=functools.partial(json.dumps, ensure_ascii=False),
        poolclass=NullPool,
    )
    mocker.patch("database.Database._create_async_engine", return_value=engine)

    async with engine.begin() as conn:
        Database.init_engine()
        await conn.run_sync(BaseOrm.metadata.create_all)

    yield

    async with engine.begin() as conn:
        await conn.run_sync(BaseOrm.metadata.drop_all)
        await Database.close_engine()
