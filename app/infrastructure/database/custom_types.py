from typing import (
    Any,
    TypeVar,
)

from sqlalchemy import (
    Dialect,
    String,
)
from sqlalchemy.types import TypeDecorator


CUSTOM_TYPE = TypeVar("CUSTOM_TYPE")


class CustomerTypes(TypeDecorator):
    impl = String

    def process_bind_param(self, value: Any | None, dialect: Dialect) -> Any | None:
        if value is not None:
            return value.value
        return None

    def process_result_value(self, value: Any | None, dialect: Dialect) -> Any | None:
        if value is not None:
            return CUSTOM_TYPE(value)
        return None

    def copy(self, **kwargs: Any) -> "CUSTOM_TYPE":
        return self.__class__()
