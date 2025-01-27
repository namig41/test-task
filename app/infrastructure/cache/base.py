from abc import (
    ABC,
    abstractmethod,
)
from typing import (
    Generic,
    Optional,
    TypeVar,
)


KeyValue = TypeVar("KeyValue")
Value = TypeVar("Value")


class ICacheService(ABC, Generic[KeyValue, Value]):

    @abstractmethod
    async def get_value(self, key_value: KeyValue) -> Optional[Value]:
        """Получить значение по ключу."""
        ...

    @abstractmethod
    async def set_value(self, key_value: KeyValue, value: Value) -> None:
        """Сохранить значение по ключу."""
        ...
