import asyncio
from typing import Any

import aiohttp
from aiochclient import ChClient

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
from infrastructure.repositories.github.database.base import BaseGitHubRepository
from infrastructure.repositories.github.database.converters import (
    convert_repository_data_to_author_stats_entity,
    convert_repository_data_to_entity,
    convert_repository_entity_to_author_stats_data,
    convert_repository_entity_to_data,
    convert_repositoy_entity_to_position_data,
)
from infrastructure.repositories.github.database.sqls import (
    CREATE_REPOSITORIES_TABLES_SQL_QUERIES,
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
                database=settings.DATABASE_CLICKHOUSE_NAME,
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
                raise InfrastructureException()
            finally:
                await client.close()

    async def create_tables(self) -> None:
        self.logger.info("Создание таблиц в базе данных ClickHouse")
        for query in CREATE_REPOSITORIES_TABLES_SQL_QUERIES:
            try:
                await self._make_request(query)
                self.logger.info(f"Таблица создана с запросом: {query}")
            except Exception as e:
                self.logger.error(
                    f"Ошибка при создании таблицы с запросом: {query}, ошибка: {e}",
                )
                raise

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

    async def save_repository(self, repository: Repository) -> None:
        self.logger.info(
            f"Сохранение репозитория {repository.name} от {repository.owner}",
        )
        try:
            repository_data: dict[str, Any] = convert_repository_entity_to_data(
                repository,
            )
            await self._make_request(INSERT_REPOSITORY, repository_data)

            postion_data: dict[str, Any] = convert_repositoy_entity_to_position_data(
                repository,
            )
            await self._make_request(INSERT_POSITION, postion_data)

            author_stats_data: list[dict[str, Any]] = (
                convert_repository_entity_to_author_stats_data(repository)
            )
            for author_stat in author_stats_data:
                await self._make_request(INSERT_AUTHORS_COMMITS, author_stat)

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
            self.logger.warning("Нет репозиториев для сохранения")
            return

        insert_query = """
            INSERT INTO test.repositories
            (name, owner, stars, watchers, forks, language, updated)
            VALUES
        """

        batch_data = []
        self.logger.info(f"Начинаем сохранение {len(repositories)} репозиториев")

        for idx, repo in enumerate(repositories):
            batch_data.append(
                f"('{repo.name}', '{repo.owner}', {repo.stars}, "
                f"{repo.watchers}, {repo.forks}, '{repo.language}', now())",
            )

            if (idx + 1) % self._batch_size == 0 or (idx + 1) == len(repositories):
                values_clause = ",".join(batch_data)
                query = f"{insert_query} {values_clause}"

                try:
                    await self._make_request(query)
                    self.logger.info(
                        f"Пакет из {len(batch_data)} репозиториев успешно сохранён",
                    )
                except Exception as e:
                    self.logger.error(f"Ошибка при сохранении пакета репозиториев: {e}")
                    raise
                batch_data.clear()

        self.logger.info("Завершено сохранение репозиториев")
