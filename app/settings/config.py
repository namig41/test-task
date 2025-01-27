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


settings: Settings = Settings()
