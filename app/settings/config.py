from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PYTHONPATH: str

    SERVICE_API_HOST: str
    SERVICE_API_PORT: int
    SERVICE_API_CORS: list[str]

    DATABASE_USER: str
    DATABASE_PASSWORD: str
    DATABASE_NAME: str
    DATABASE_TEST_NAME: str
    DATABASE_HOST: str
    DATABASE_PORT: int
    DATABASE_PROVIDER: str

    PGADMIN_EMAIL: str
    PGADMIN_PASSWORD: str

    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str

    CACHE_HOST: str
    CACHE_PORT: int

    MESSAGE_BROKER_HOST: str
    MESSAGE_BROKER_PORT: int
    MESSAGE_BROKER_UI_PORT: int
    MESSAGE_BROKER_USER: str
    MESSAGE_BROKER_PASSWORD: str

    SMTP_HOST: str
    SMTP_PORT: int
    SMTP_USERNAME: str
    SMTP_PASSWORD: str


settings: Settings = Settings()
