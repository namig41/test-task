import logging
import sys
from functools import lru_cache
from typing import TextIO

from infrastructure.logger.base import ILogger


def logger_factory(name: str, level: int, stream: TextIO) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(level)

    handler = logging.StreamHandler(stream=stream)

    formatter = logging.Formatter(
        fmt="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    handler.setFormatter(formatter)

    if handler not in logger.handlers:
        logger.addHandler(handler)

    return logger


@lru_cache(1)
def create_logger_dependency() -> ILogger:
    common_logger: logging.Logger = logger_factory(
        name="common",
        level=logging.INFO,
        stream=sys.stdout,
    )
    error_logger: logging.Logger = logger_factory(
        name="error",
        level=logging.ERROR,
        stream=sys.stderr,
    )
    return logging.Logger(logger=common_logger, error_logger=error_logger)
