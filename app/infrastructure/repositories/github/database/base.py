from abc import (
    ABC,
    abstractmethod,
)

from domain.entities.github import Repository


# TODO: От абстрактного класса должны наследоваться GithubScrapper и ClickHouseRepository
class BaseGitHubRepository(ABC):

    # TODO: Нужно вынсети логику создания бд и таблиц в отдельные функции database
    @abstractmethod
    async def create_tables(self) -> None: ...

    @abstractmethod
    async def get_repository_by_name(self, name: str, owner: str) -> Repository: ...

    @abstractmethod
    async def save_repository(self, repository: Repository) -> None: ...
