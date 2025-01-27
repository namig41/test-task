from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from infrastructure.database.config import DBConfig
from infrastructure.exceptions.database import DatabaseRunFailedException


def init_database(db_config: DBConfig) -> AsyncEngine:
    engine: AsyncEngine = create_async_engine(
        db_config.database_url,
    )
    try:
        engine.connect()
    except SQLAlchemyError:
        raise DatabaseRunFailedException()
    return engine


class Base(DeclarativeBase):
    pass
