import asyncio
from typing import Any

from aiohttp import ClientSession

from domain.entities.github import (
    Repository,
    RepositoryAuthorCommitsNum,
)
from infrastructure.repositories.github.api.constatns import GITHUB_API_BASE_URL
from infrastructure.repositories.github.api.converters import (
    convert_commit_data_to_author_stats,
    convert_repository_data_to_model,
)


class GithubRepositoryScrapper:
    def __init__(self, access_token: str, mcr: int = 10, rps: float = 1.0):
        self._session = ClientSession(
            headers={
                "Accept": "application/vnd.github.v3+json",
                "Authorization": f"Bearer {access_token}",
            },
        )

        self.mcr = mcr
        self.rps = rps
        self._semaphore = asyncio.Semaphore(mcr)

    async def _make_request(
        self,
        endpoint: str,
        method: str = "GET",
        params: dict[str, Any] | None = None,
    ) -> Any:
        async with self._semaphore:
            await asyncio.sleep(self.rps)
            async with self._session.request(
                method,
                f"{GITHUB_API_BASE_URL}/{endpoint}",
                params=params,
            ) as response:
                return await response.json()

    async def _get_top_repositories(self, limit: int = 100) -> list[dict[str, Any]]:
        """GitHub REST API: https://docs.github.com/en/rest/search/search?apiVersion=2022-11-28#search-repositories"""
        data = await self._make_request(
            endpoint="search/repositories",
            params={
                "q": "stars:>1",
                "sort": "stars",
                "order": "desc",
                "per_page": limit,
            },
        )
        return data["items"]

    async def _get_repository_commits(
        self,
        owner: str,
        repo: str,
    ) -> list[dict[str, Any]]:
        """
        GitHub REST API: https://docs.github.com/en/rest/commits/commits?apiVersion=2022-11-28#list-commits
        """
        data = await self._make_request(
            endpoint=f"repos/{owner}/{repo}/commits",
        )
        return data

    async def get_repositories(self) -> list[Repository]:
        top_repos: list[dict[str, Any]] = await self._get_top_repositories(limit=100)
        repositories: list[Repository] = []

        for repo_data in top_repos:
            repository: Repository = convert_repository_data_to_model(
                repo_data,
                top_repos.index(repo_data) + 1,
            )
            commits: list[dict[str, Any]] = await self._get_repository_commits(
                owner=repository.owner,
                repo=repository.name,
            )
            authors_commits_num_today: list[RepositoryAuthorCommitsNum] = (
                convert_commit_data_to_author_stats(commits)
            )
            repository.authors_commits_num_today = authors_commits_num_today
            repositories.append(repository)

        return repositories

    async def close(self):
        await self._session.close()
