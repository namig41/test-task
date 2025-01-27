from dataclasses import dataclass

from settings.config import settings


@dataclass(frozen=True)
class MessageBrokerConfig:
    host: str = settings.MESSAGE_BROKER_HOST
    port: int = settings.MESSAGE_BROKER_PORT
    login: str = settings.MESSAGE_BROKER_USER
    password: str = settings.MESSAGE_BROKER_PASSWORD

    @property
    def get_url(self) -> str:
        return f"amqp://{self.login}:{self.password}@{self.host}:{self.port}/"
