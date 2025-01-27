from abc import abstractmethod
from typing import Protocol


class ILogger(Protocol):

    @abstractmethod
    def info(self, message: str) -> None: ...

    @abstractmethod
    def error(self, message: str) -> None: ...

    @abstractmethod
    def debug(self, message: str) -> None: ...
