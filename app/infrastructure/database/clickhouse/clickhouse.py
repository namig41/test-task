import asyncio
from dataclasses import dataclass

from app.infrastructure.database.base import BaseDataBase
from app.infrastructure.database.clickhouse.sqls import (
    CREATE_REPOSITORIES_DATABASE,
    CREATE_REPOSITORIES_TABLES_SQL_QUERIES,
    DROP_REPOSITORIES_DROP_TABLES,
)
from app.infrastructure.exceptions.base import InfrastructureException
from app.infrastructure.logger.base import ILogger


@dataclass
class ClickHouseDataBase(BaseDataBase):
    logger: ILogger

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

    async def drop_tables(self) -> None:
        try:
            await asyncio.gather(
                *[self._make_request(query) for query in DROP_REPOSITORIES_DROP_TABLES],
            )
            self.logger.info("Таблицы успешно очищены")
        except Exception as e:
            self.logger.error(f"Ошибка при очистке таблицы: {e}")
            raise

    async def create_db(self, database_name: str) -> None:
        try:
            await self._make_request(
                CREATE_REPOSITORIES_DATABASE.format(db_name=database_name),
            )
        except InfrastructureException:
            raise
