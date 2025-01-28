from typing import Any

import aiohttp
from aiochclient import ChClient

from domain.entities.github import (
    Repository,
    RepositoryAuthorCommitsNum,
)
from infrastructure.exceptions.database import RepositoryNotFoundException
from infrastructure.repositories.github.database.base import BaseGitHubRepository
from infrastructure.repositories.github.database.converters import (
    convert_repository_record_to_author_stats_entity,
    convert_repository_record_to_entity,
)
from infrastructure.repositories.github.database.sqls import CREATE_REPOSITORIES_TABLES_SQL_QUERIES
from settings.config import settings


class GitHubClickHouseRepository(BaseGitHubRepository):
    def __init__(self, batch_size: int = 10):
        self._batch_size = batch_size

    async def _make_request(
        self, query: str, params: dict[str, Any] | None = None,
    ) -> Any:
        # TODO: Необходимо иньектировать параметры через структуру DBConfig с использованием di-контейнера
        async with aiohttp.ClientSession() as session:
            client: ChClient = ChClient(
                session=session,
                url=f"http://{settings.DATABASE_CLICKHOUSE_HOST}:{settings.DATABASE_CLICKHOUSE_HTTP}/",
                user=settings.DATABASE_CLICKHOUSE_USER,
                password=settings.DATABASE_CLICKHOUSE_PASSWORD,
                database=settings.DATABASE_CLICKHOUSE_NAME,
                compress_response=True,
            )
            print(query)
            try:
                if query.strip().lower().startswith("select"):
                    result = await client.fetch(query)
                    return result
                elif not query.strip().lower().startswith("insert"):
                    await client.execute(query)
                    return {"status": "success"}
                else:
                    result = await client.fetch(query, params or {})
                    return result
            finally:
                await client.close()

    async def create_tables(self) -> None:
        for query in CREATE_REPOSITORIES_TABLES_SQL_QUERIES:
            await self._make_request(query)

    async def get_repository_by_name(self, name: str, owner: str) -> Repository:
        rows = await self._make_request(
            f"SELECT * FROM test.repositories WHERE name = '{name}' AND owner = '{owner}'",
        )

        if not rows:
            raise RepositoryNotFoundException()

        authors_commits: list[RepositoryAuthorCommitsNum] = (
            convert_repository_record_to_author_stats_entity(rows)
        )
        first_row = rows[0]
        repository: Repository = convert_repository_record_to_entity(first_row)
        repository.authors_commits_num_today = authors_commits
        return repository

    async def save_repository(self, repository: Repository) -> None:
        await self._make_request(
            f"INSERT INTO test.repositories (name, owner, stars, watchers, forks, language, updated) "
            f"VALUES ('{repository.name}', '{repository.owner}', {repository.stars}, {repository.watchers}, {repository.forks}, '{repository.language}', now())",
        )

    async def save_repositories(self, repositories: list[Repository]) -> None:
        if not repositories:
            return

        insert_query = """
            INSERT INTO test.repositories
            (name, owner, stars, watchers, forks, language, updated)
            VALUES
        """

        batch_data = []

        for idx, repo in enumerate(repositories):
            batch_data.append(
                f"('{repo.name}', '{repo.owner}', {repo.stars}, "
                f"{repo.watchers}, {repo.forks}, '{repo.language}', now())",
            )

            if (idx + 1) % self._batch_size == 0 or (idx + 1) == len(repositories):
                values_clause = ",".join(batch_data)
                query = f"{insert_query} {values_clause}"

                await self._make_request(query)
                batch_data.clear()
