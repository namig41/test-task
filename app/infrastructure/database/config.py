from dataclasses import dataclass

from settings.config import settings


@dataclass
class DBConfig:
    DB_USER: str = settings.DATABASE_USER
    DB_PASSWORD: str = settings.DATABASE_PASSWORD
    DB_HOST: str = settings.DATABASE_HOST
    DB_PORT: str = settings.DATABASE_PORT
    DB_NAME: str = settings.DATABASE_NAME
    DB_PRIVDER: str = settings.DATABASE_PROVIDER

    @property
    def database_url(self):
        return f"${self.DB_PRIVDER}://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
