import asyncio
from typing import (
    Any,
    Final,
)

import aiohttp
from aiochclient import ChClient
from app.infrastructure.repositories.github.base import BaseGitHubRepository
from tools import iterators

from domain.entities.github import (
    Repository,
    RepositoryAuthorCommitsNum,
)
from infrastructure.exceptions.base import InfrastructureException
from infrastructure.exceptions.repository import (
    RepositoryNotFoundException,
    RepositoryTimeOutException,
)
from infrastructure.logger.base import ILogger
from infrastructure.repositories.github.database.converters import (
    convert_repository_data_to_author_stats_entity,
    convert_repository_data_to_entity,
    convert_repository_entity_to_author_stats_data,
    convert_repository_entity_to_data,
    convert_repositoy_entity_to_position_data,
)
from infrastructure.repositories.github.database.sqls import (
    GET_REPOSITORY_WITH_DETAILS,
    INSERT_AUTHORS_COMMITS,
    INSERT_POSITION,
    INSERT_REPOSITORY,
)
from settings.config import settings


class GitHubClickHouseRepository(BaseGitHubRepository):
    def __init__(self, logger: ILogger, batch_size: int = 10):
        self.logger = logger
        self._batch_size = batch_size

    async def _make_request(
        self,
        query: str,
        params: dict[str, Any] | None = None,
    ) -> Any:
        # TODO: Необходимо иньектировать параметры через структуру DBConfig с использованием di-контейнера
        async with aiohttp.ClientSession() as session:
            client: ChClient = ChClient(
                session=session,
                url=f"http://{settings.DATABASE_CLICKHOUSE_HOST}:{settings.DATABASE_CLICKHOUSE_HTTP}/",
                user=settings.DATABASE_CLICKHOUSE_USER,
                password=settings.DATABASE_CLICKHOUSE_PASSWORD,
                # database=settings.DATABASE_CLICKHOUSE_NAME,
                compress_response=True,
            )
            try:
                self.logger.info(f"Отправка запроса: {query} с параметрами {params}")

                if query.strip().lower().startswith("select"):
                    result = await client.fetch(query)
                    self.logger.info(f"Получен результат SELECT-запроса: {result}")
                    return result
                elif not query.strip().lower().startswith("insert"):
                    await client.execute(query)
                    self.logger.info(f"Успешное выполнение запроса: {query}")
                    return {"status": "success"}
                else:
                    result = await client.execute(query=query, params=params)
                    self.logger.info(f"Успешное выполнение INSERT-запроса: {query}")
                    return result
            except aiohttp.ClientError as e:
                self.logger.error(f"Ошибка клиента при выполнении запроса: {e}")
                raise InfrastructureException()
            except asyncio.TimeoutError as e:
                self.logger.error(
                    f"Запрос к базе данных превысил лимит времени (тайм-аут): {e}",
                )
                raise RepositoryTimeOutException()
            except Exception as e:
                self.logger.error(f"Неизвестная ошибка при выполнении запроса: {e}")
                raise
            finally:
                await client.close()

    async def get_repository_by_name(self, name: str, owner: str) -> Repository:
        self.logger.info(f"Получение репозитория {name} от {owner}")
        try:
            rows = await self._make_request(
                GET_REPOSITORY_WITH_DETAILS.format(name=name, owner=owner),
            )

            if not rows:
                self.logger.error(
                    f"Репозиторий с именем {name} и владельцем {owner} не найден",
                )
                raise RepositoryNotFoundException()

            authors_commits: list[RepositoryAuthorCommitsNum] = (
                convert_repository_data_to_author_stats_entity(rows)
            )
            first_row = rows[0]
            repository: Repository = convert_repository_data_to_entity(first_row)
            repository.authors_commits_num_today = authors_commits
            self.logger.info(f"Репозиторий {name} от {owner} успешно найден")
            return repository
        except RepositoryNotFoundException:
            self.logger.error(f"Репозиторий {name} от {owner} не найден в базе данных")
            raise
        except Exception as e:
            self.logger.error(
                f"Ошибка при получении репозитория {name} от {owner}: {e}",
            )
            raise InfrastructureException()

    # NOTE Медленная вставка. Используется только для тестов
    async def save_repository(self, repository: Repository) -> None:
        self.logger.info(
            f"Сохранение репозитория {repository.name} от {repository.owner}",
        )
        try:
            repository_data: dict[str, Any] = convert_repository_entity_to_data(
                repository,
            )

            postion_data: dict[str, Any] = convert_repositoy_entity_to_position_data(
                repository,
            )

            author_stats_data: list[dict[str, Any]] = (
                convert_repository_entity_to_author_stats_data(repository)
            )

            await asyncio.gather(
                self._make_request(INSERT_REPOSITORY, repository_data),
                self._make_request(INSERT_POSITION, postion_data),
                *[
                    self._make_request(INSERT_AUTHORS_COMMITS, author_stat)
                    for author_stat in author_stats_data
                ],
            )

            self.logger.info(
                f"Репозиторий {repository.name} от {repository.owner} успешно сохранён",
            )
        except Exception as e:
            self.logger.error(
                f"Ошибка при сохранении репозитория {repository.name} от {repository.owner}: {e}",
            )
            raise InfrastructureException()

    async def save_repositories(self, repositories: list[Repository]) -> None:
        if not repositories:
            self.logger.debug("Нет репозиториев для сохранения")
            return

        # TODO: Вынести в константу
        insert_repositories_query: Final[
            str
        ] = """
            INSERT INTO test.repositories
            (name, owner, stars, watchers, forks, language, updated)
            VALUES
        """

        insert_positions_query: Final[
            str
        ] = """
            INSERT INTO test.repositories_positions (date, repo, position)
            VALUES
        """

        insert_authors_commits_query: Final[
            str
        ] = """
            INSERT INTO test.repositories_authors_commits (date, repo, author, commits_num)
            VALUES
        """

        batch_repositories_data: list[str] = []
        batch_positions_data: list[str] = []
        batch_authors_commits_data: list[str] = []

        self.logger.info(f"Начинаем сохранение {len(repositories)} репозиториев")

        for batch_repositories in iterators.batch_generator(
            repositories, self._batch_size,
        ):
            for repo in batch_repositories:
                batch_repositories_data.append(
                    f"('{repo.name}', '{repo.owner}', {repo.stars}, "
                    f"{repo.watchers}, {repo.forks}, '{repo.language}', now())",
                )

                batch_positions_data.append(
                    f"(now(), '{repo.name}', {repo.position})",
                )

                for commits_today in repo.authors_commits_num_today:
                    batch_authors_commits_data.append(
                        f"(now(), '{repo.name}', '{commits_today.author}', {commits_today.commits_num})",
                    )

                values_clause: str = ",".join(batch_repositories_data)
                repository_query: str = f"{insert_repositories_query} {values_clause}"

                values_clause: str = ",".join(batch_positions_data)
                position_query: str = f"{insert_positions_query} {values_clause}"

                values_clause: str = ",".join(batch_authors_commits_data)
                author_commits_query: str = (
                    f"{insert_authors_commits_query} {values_clause}"
                )

            try:
                await asyncio.gather(
                    self._make_request(repository_query),
                    self._make_request(position_query),
                    self._make_request(author_commits_query),
                )
                self.logger.info(
                    f"Пакет из {len(batch_repositories_data)} репозиториев успешно сохранён",
                )
            except Exception as e:
                self.logger.error(f"Ошибка при сохранении пакета репозиториев: {e}")
                raise InfrastructureException()

            batch_repositories_data.clear()
            batch_positions_data.clear()
            batch_authors_commits_data.clear()

        self.logger.info("Завершено сохранение репозиториев")
