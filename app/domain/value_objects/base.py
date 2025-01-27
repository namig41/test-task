from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import dataclass
from typing import (
    Generic,
    TypeVar,
)


_T = TypeVar("_T")


@dataclass(frozen=True)
class BaseValueObject(ABC, Generic[_T]):

    value: _T

    def __post_init__(self):
        self.validate()

    @abstractmethod
    def validate(self) -> None: ...

    def to_raw(self) -> _T:
        return self.value

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return self.value == other
        return self.value == other.value

    def __str__(self) -> str:
        return str(self.value)
