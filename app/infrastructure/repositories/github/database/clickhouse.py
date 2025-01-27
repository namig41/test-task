from typing import Any
from aiochclient import ChClient
from domain.entities.github import Repository, RepositoryAuthorCommitsNum
from infrastructure.database.clickhouse.github.sqls import (
    GET_REPOSITORY_WITH_DETAILS,
    INSERT_REPOSITORY,
)
from infrastructure.repositories.github.database.base import BaseGitHubRepository
from infrastructure.repositories.github.database.converters import (
    convert_repository_record_to_author_stats_entity,
    convert_repository_record_to_entity,
)


class GitHubClickHouseRepository(BaseGitHubRepository):
    def __init__(self, client: ChClient):
        self._client = client

    async def get_repository_by_name(self, name: str, owner: str) -> Repository:
        if rows := await self._client.fetch(
            GET_REPOSITORY_WITH_DETAILS, {"name": name, "owner": owner}
        ):
            raise

        authors_commits: list[RepositoryAuthorCommitsNum] = convert_repository_record_to_author_stats_entity(rows)

        first_row: dict[str, Any] = rows[0]
        repository: Repository = convert_repository_record_to_entity(first_row)
        repository.authors_commits_num_today = authors_commits
        return repository

    async def save_repository(self, repository: Repository) -> None:
        await self._client.execute(
            INSERT_REPOSITORY,
            {
                "name": repository.name,
                "owner": repository.owner,
                "stars": repository.stars,
                "watchers": repository.watchers,
                "forks": repository.forks,
                "language": repository.language,
            },
        )

    async def close(self) -> None:
        await self._client.close()
