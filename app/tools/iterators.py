from typing import (
    Generator,
    Iterable,
    TypeVar,
)


T = TypeVar("T")

# NOTE: В python3.12 можно использовать синтаксис batch_generator[T](...)


def batch_generator(
    iterable: Iterable[T], batch_size: int,
) -> Generator[list[T], None, None]:
    """
    Генератор для возврата элементов батчами из итерируемого объекта.
    """
    batch: list[T] = []

    for item in iterable:
        batch.append(item)
        if len(batch) == batch_size:
            yield batch
            batch = []

    if batch:
        yield batch
