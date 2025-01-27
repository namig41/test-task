from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PYTHONPATH: str

    SERVICE_API_HOST: str
    SERVICE_API_PORT: int
    SERVICE_API_CORS: list[str]

    DATABASE_USER: str
    DATABASE_PASSWORD: str
    DATABASE_NAME: str
    DATABASE_HOST: str
    DATABASE_PORT: int
    DATABASE_PROVIDER: str

    PGADMIN_EMAIL: str
    PGADMIN_PASSWORD: str

    DATABASE_CLICKHOUSE_USER: str
    DATABASE_CLICKHOUSE_PASSWORD: str
    DATABASE_CLICKHOUSE_NAME: str
    DATABASE_CLICKHOUSE_HOST: str
    DATABASE_CLICKHOUSE_PORT: int
    DATABASE_CLICKHOUSE_HTTP: int

    GITHUB_ACCESS_TOKEN: str


settings: Settings = Settings()
