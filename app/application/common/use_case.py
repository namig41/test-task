from abc import abstractmethod
from typing import (
    Generic,
    TypeVar,
)


InputDTO = TypeVar("InputDTO")
OutputDTO = TypeVar("OutputDTO")


class UseCase(Generic[InputDTO, OutputDTO]):
    @abstractmethod
    async def __call__(self, data: InputDTO) -> OutputDTO: ...
