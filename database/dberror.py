from sqlalchemy.exc import IntegrityError
from sqlalchemy.dialects.postgresql.asyncpg import AsyncAdapt_asyncpg_dbapi
from psycopg2.errorcodes import UNIQUE_VIOLATION


def is_unique_violation(error: IntegrityError):
    return (
        type(error) == IntegrityError
        and isinstance(error.orig, AsyncAdapt_asyncpg_dbapi.DatabaseError)
        and error.orig.pgcode == UNIQUE_VIOLATION
    )
