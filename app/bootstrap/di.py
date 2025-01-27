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

from infrastructure.cache.config import CacheConfig
from infrastructure.cache.init import init_cache
from infrastructure.database.config import DBConfig
from infrastructure.database.init import init_database
from infrastructure.jwt.base import BaseJWTProcessor
from infrastructure.jwt.config import JWTConfig
from infrastructure.jwt.jwt_processor import PyJWTProcessor
from infrastructure.logger.base import ILogger
from infrastructure.logger.factory import create_logger_dependency
from infrastructure.message_broker.base import BaseMessageBroker
from infrastructure.message_broker.config import MessageBrokerConfig
from infrastructure.message_broker.message_broker_factory import ConnectionFactory
from infrastructure.message_broker.rabbit_message_broker import RabbitMQMessageBroker
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

    # Register database configuration
    db_config: DBConfig = DBConfig()
    container.register(
        DBConfig,
        instance=db_config,
        scope=Scope.singleton,
    )

    # Register database engine
    container.register(
        AsyncEngine,
        factory=partial(init_database, db_config=db_config),
        scope=Scope.singleton,
    )

    # Register JWT configuration
    jwt_config: JWTConfig = JWTConfig()
    container.register(
        JWTConfig,
        instance=jwt_config,
        scope=Scope.singleton,
    )

    # Register JWT processor
    container.register(
        BaseJWTProcessor,
        PyJWTProcessor,
        scope=Scope.singleton,
    )

    # Register cache configuration
    cache_config: CacheConfig = CacheConfig()
    container.register(
        Redis,
        factory=partial(init_cache, cache_config=cache_config),
        scope=Scope.singleton,
    )

    # Register Message Broker
    message_broker_config: MessageBrokerConfig = MessageBrokerConfig(host="rabbitmq")
    container.register(
        MessageBrokerConfig,
        instance=message_broker_config,
        scope=Scope.singleton,
    )

    container.register(ConnectionFactory, scope=Scope.singleton)

    container.register(AbstractConnection, instance=None)
    container.register(AbstractChannel, instance=None)

    container.register(
        BaseMessageBroker,
        RabbitMQMessageBroker,
        scope=Scope.singleton,
    )

    return container
