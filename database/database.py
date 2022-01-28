from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from config import config
from utils.strenum import StrEnum


class IsolationLevel(StrEnum):
    READ_COMMITTED = "READ COMMITTED"
    REPEATABLE_READ = "REPEATABLE READ"
    SERIALIZABLE = "SERIALIZABLE"


class Database:
    __engine: AsyncSession = None

    @staticmethod
    def get_conn_url() -> str:
        return (
            f"postgresql://{config.PG_USER}:{config.PG_PASSWORD}@{config.PG_HOST}:{config.PG_PORT}/{config.PG_DATABASE}"
        )

    @staticmethod
    def get_async_conn_url() -> str:
        return f"postgresql+asyncpg:://{config.PG_USER}:{config.PG_PASSWORD}@{config.PG_HOST}:{config.PG_PORT}/{config.PG_DATABASE}"

    @classmethod
    def _create_async_engine(cls) -> None:
        return create_async_engine(
            config.PG_ASYNC_CONN_URL,
            echo=config.PG_DEBUG,
            pool_size=config.PG_POOL_SIZE,
            max_overflow=config.PG_POOL_MAX_OVERFLOW,
            pool_pre_ping=True,
        )

    @classmethod
    def init_engine(cls) -> None:
        cls.__engine = cls._create_async_engine()

    @classmethod
    async def close_engine(cls) -> None:
        if cls.__engine:
            await cls.__engine.dispose()

    @classmethod
    def async_session(
        cls, expire_on_commit: bool = False, isolation_level: IsolationLevel = IsolationLevel.READ_COMMITTED
    ) -> AsyncSession:
        engine = cls.__engine.execution_options(isolation_level=isolation_level)
        return sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=expire_on_commit)()
