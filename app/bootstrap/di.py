from functools import (
    lru_cache,
    partial,
)

from aio_pika.abc import (
    AbstractChannel,
    AbstractConnection,
)
from punq import (
    Container,
    Scope,
)
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio.engine import AsyncEngine

from infrastructure.logger.base import ILogger
from infrastructure.logger.factory import create_logger_dependency
from settings.config import (
    Settings,
    settings,
)


@lru_cache(1)
def init_container() -> Container:
    return _init_container()


# Initialize the dependency injection container
def _init_container() -> Container:
    container: Container = Container()

    # Register global settings
    container.register(
        Settings,
        instance=settings,
        scope=Scope.singleton,
    )

    # Register logger
    container.register(
        ILogger,
        factory=create_logger_dependency,
        scope=Scope.singleton,
    )

    return container
