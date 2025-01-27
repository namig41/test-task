from dataclasses import dataclass


@dataclass
class DBConfig:
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_PRIVDER: str

    @property
    def database_url(self):
        return f"${self.DB_PRIVDER}://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
