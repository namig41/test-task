from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import dataclass

from infrastructure.message_broker.base import BaseMessageBroker
from infrastructure.message_broker.message import Message


@dataclass
class BaseProducer(ABC):
    message_broker: BaseMessageBroker

    @abstractmethod
    async def publish(self, message: Message) -> None: ...
