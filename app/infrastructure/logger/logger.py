import logging

from infrastructure.logger.base import ILogger


class Logger(ILogger):

    logger: logging.Logger
    error_logger: logging.Logger

    def info(self, message: str) -> None:
        self.logger.info(message)

    def error(self, message: str) -> None:
        self.error_logger.error(message)

    def debug(self, message: str) -> None:
        self.logger.debug(message)
