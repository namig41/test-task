from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import dataclass
from typing import TypeVar

from app.infrastructure.database.config import DBConfig


ConnectionType = TypeVar("ConnectionType")


@dataclass
class BaseConnectionFactory(ABC):
    config: DBConfig

    @abstractmethod
    async def get_connection(self) -> ConnectionType: ...
