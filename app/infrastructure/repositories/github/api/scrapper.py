import asyncio
from typing import Any

from aiohttp import (
    ClientError,
    ClientSession,
    ClientTimeout,
)

from domain.entities.github import (
    Repository,
    RepositoryAuthorCommitsNum,
)
from infrastructure.exceptions.base import InfrastructureException
from infrastructure.exceptions.repository import RepositoryTimeOutException
from infrastructure.logger.base import ILogger
from infrastructure.repositories.github.api.constatns import GITHUB_API_BASE_URL
from infrastructure.repositories.github.api.converters import (
    convert_commit_data_to_author_stats,
    convert_repository_data_to_model,
)


class GithubRepositoryScrapper:
    def __init__(
        self, access_token: str, logger: ILogger, mcr: int = 10, rps: float = 1.0,
    ):
        self._session = ClientSession(
            headers={
                "Accept": "application/vnd.github.v3+json",
                "Authorization": f"Bearer {access_token}",
            },
            timeout=ClientTimeout(total=10),
        )
        self.logger = logger
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
            try:
                await asyncio.sleep(self.rps)
                self.logger.info(
                    f"Отправка {method} запроса на {endpoint} с параметрами {params}",
                )

                async with self._session.request(
                    method,
                    f"{GITHUB_API_BASE_URL}/{endpoint}",
                    params=params,
                ) as response:
                    response.raise_for_status()
                    data = await response.json()
                    self.logger.info(f"Получен ответ: {data}")
                    return data
            except ClientError as e:
                self.logger.error(f"Ошибка клиента при запросе к {endpoint}: {e}")
                raise InfrastructureException()
            except asyncio.TimeoutError as e:
                self.logger.error(
                    f"Запрос к {endpoint} превысил лимит времени (тайм-аут): {e}",
                )
                raise RepositoryTimeOutException()
            except Exception as e:
                self.logger.error(f"Неизвестная ошибка при запросе к {endpoint}: {e}")
                raise InfrastructureException()

    async def _get_top_repositories(self, limit: int = 100) -> list[dict[str, Any]]:
        """GitHub REST API: https://docs.github.com/en/rest/search/search?apiVersion=2022-11-28#search-repositories"""
        try:
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
        except KeyError as e:
            self.logger.error(f"Не удалось извлечь 'items' из ответа: {e}")
            raise InfrastructureException()

    async def _get_repository_commits(
        self,
        owner: str,
        repo: str,
    ) -> list[dict[str, Any]]:
        """
        GitHub REST API: https://docs.github.com/en/rest/commits/commits?apiVersion=2022-11-28#list-commits
        """
        try:
            data = await self._make_request(
                endpoint=f"repos/{owner}/{repo}/commits",
            )
            return data
        except KeyError as e:
            self.logger.error(
                f"Не удалось извлечь коммиты из ответа для {owner}/{repo}: {e}",
            )
            raise InfrastructureException()

    async def get_repositories(self) -> list[Repository]:
        self.logger.info("Начинаем получать топовые репозитории")
        top_repos: list[dict[str, Any]] = await self._get_top_repositories(limit=5)
        repositories: list[Repository] = []

        for repo_data in top_repos:
            try:
                repository: Repository = convert_repository_data_to_model(
                    repo_data,
                    top_repos.index(repo_data) + 1,
                )
                self.logger.info(
                    f"Обрабатываем репозиторий {repository.name} от {repository.owner}",
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
            except Exception as e:
                self.logger.error(
                    f"Ошибка при обработке репозитория {repo_data['name']}: {e}",
                )
                continue

        self.logger.info("Завершена обработка репозиториев")
        return repositories

    async def close(self):
        self.logger.info("Закрываем сессию")
        await self._session.close()
