import uuid
from typing import (
    Protocol,
    Sequence,
    TypeVar,
)


ModelType = TypeVar("ModelType")
ReadSchemaType = TypeVar("ReadSchemaType")
CreateSchemaType = TypeVar("CreateSchemaType")
UpdateSchemaType = TypeVar("UpdateSchemaType")


class BaseRepositoryProtocol(
    Protocol[ReadSchemaType, CreateSchemaType, UpdateSchemaType],
):
    async def get(self, id: uuid.UUID) -> ReadSchemaType: ...

    async def get_or_none(self, id: uuid.UUID) -> ReadSchemaType | None: ...

    async def get_by_ids(self, ids: Sequence[uuid.UUID]) -> list[ReadSchemaType]: ...

    async def get_all(self) -> list[ReadSchemaType]: ...

    async def create(self, create_object: CreateSchemaType) -> ReadSchemaType: ...

    async def bulk_create(
        self,
        create_objects: list[CreateSchemaType],
    ) -> list[ReadSchemaType]: ...

    async def update(self, update_object: UpdateSchemaType) -> ReadSchemaType: ...

    async def bulk_update(self, update_objects: list[UpdateSchemaType]) -> None: ...

    async def upsert(self, create_object: CreateSchemaType) -> ReadSchemaType: ...

    async def delete(self, id: uuid.UUID) -> bool: ...
