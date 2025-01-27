from abc import (
    ABC,
    abstractmethod,
)

from domain.entities.github import Repository


class BaseGitHubRepository(ABC):
    @abstractmethod
    async def get_repository_by_name(self, name: str, owner: str) -> Repository: ...

    @abstractmethod
    async def save_repository(self, repository: Repository) -> None: ...

    @abstractmethod
    async def close(self) -> None: ...
