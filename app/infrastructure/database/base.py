from abc import (
    ABC,
    abstractmethod,
)


class BaseDataBase(ABC):

    @abstractmethod
    async def create_tables(self) -> None: ...

    @abstractmethod
    async def create_db(self, database_name: str) -> None: ...

    @abstractmethod
    async def drop_tables(self) -> None: ...
