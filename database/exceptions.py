from sqlalchemy.exc import IntegrityError
from sqlalchemy.dialects.postgresql.asyncpg import AsyncAdapt_asyncpg_dbapi
from psycopg2.errorcodes import UNIQUE_VIOLATION


class DatabaseError(IntegrityError):
    def is_unique_violation(self):
        return isinstance(self.orig, AsyncAdapt_asyncpg_dbapi.DatabaseError) and self.orig.pgcode == UNIQUE_VIOLATION
