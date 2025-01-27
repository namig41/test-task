from typing import Annotated

from fastapi import Depends

import asyncpg

from settings.config import settings


async def get_pg_connection() -> asyncpg.Connection:
    pool: asyncpg.Pool = await asyncpg.create_pool(
        user=settings.DATABASE_USER,
        password=settings.DATABASE_PASSWORD,
        database=settings.DATABASE_NAME,
        host=settings.DATABASE_HOST,
        port=settings.DATABASE_PORT,
        min_size=1,
        max_size=10,
    )

    connection: asyncpg.Connection = await pool.acquire()
    return connection


async def get_db_version(
    conn: Annotated[asyncpg.Connection, Depends(get_pg_connection)],
):
    return await conn.fetchval("SELECT version()")
