from functools import lru_cache

from punq import (
    Container,
    Scope,
)

from infrastructure.logger.base import ILogger
from infrastructure.logger.factory import create_logger_dependency
from infrastructure.repositories.github.api.scrapper import GithubRepositoryScrapper
from infrastructure.repositories.github.database.base import BaseGitHubRepository
from infrastructure.repositories.github.database.clickhouse import GitHubClickHouseRepository
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

    # TODO: Реализовать регистрацию скраппера с автоматической разрешение зависимостей
    container.register(
        GithubRepositoryScrapper,
        lambda: GithubRepositoryScrapper(
            access_token=settings.GITHUB_ACCESS_TOKEN,
            logger=container.resolve(ILogger),
        ),
        scope=Scope.transient,
    )

    # Register GitHubRepository
    container.register(
        BaseGitHubRepository,
        GitHubClickHouseRepository,
        scope=Scope.singleton,
    )
    return container
