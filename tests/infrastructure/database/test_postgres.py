from asyncpg import Connection
import pytest
from infrastructure.database.postgres.init import get_db_version, get_pg_connection

@pytest.mark.asyncio
async def test_postgres_connection():
    connection: Connection = await get_pg_connection()
    result = await connection.fetch('SELECT 1')
    result_dict = [dict(record) for record in result]
    assert result_dict == [{'?column?': 1}]
    await connection.close()
    
    
@pytest.mark.asyncio
async def test_postgres_version():
    connection: Connection = await get_pg_connection()
    result = await get_db_version(conn=connection)
    assert isinstance(result, str)
    assert result.startswith("PostgreSQL")
