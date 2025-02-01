from dataclasses import dataclass

from aiochclient import ChClient
import aiohttp
from app.infrastructure.database.config import DBConfig
from infrastructure.database.factory import BaseConnectionFactory

@dataclass
class ConnectionFactory(BaseConnectionFactory):
    config: DBConfig

    async def get_connection(self) -> ChClient:
        async with aiohttp.ClientSession() as session:
            client: ChClient = ChClient(
                session=session,
                url=f"http://{self.config.DATABASE_HOST}:{self.config.DATABASE_HTTP}/",
                user=self.config.DATABASE_USER,
                password=self.config.DATABASE_PASSWORD,
                compress_response=True,
            )
            
            return client