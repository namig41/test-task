from sqlalchemy.ext.asyncio import AsyncEngine

from infrastructure.database.models import metadata


def start_entity_mappers() -> None: ...


async def create_database(engine: AsyncEngine) -> None:
    async with engine.begin() as connection:
        await connection.run_sync(metadata.create_all)


async def drop_database(engine: AsyncEngine) -> None:
    async with engine.begin() as connection:
        await connection.run_sync(metadata.drop_all)
