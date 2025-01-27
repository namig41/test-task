from dataclasses import dataclass

from settings.config import settings


@dataclass
class CacheConfig:
    host: str = settings.CACHE_HOST
    port: int = settings.CACHE_PORT

    def get_url(self, schema: str) -> str:
        return f"{schema}://{self.host}:{self.port}"
