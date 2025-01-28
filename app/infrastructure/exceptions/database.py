from dataclasses import dataclass

from infrastructure.exceptions.base import InfrastructureException


@dataclass(eq=False)
class DatabaseConnectionFailedException(InfrastructureException):
    @property
    def message(self):
        return "Не удалось установить соединение с базой данных"


@dataclass(eq=False)
class DatabaseInitialFailedException(InfrastructureException):
    @property
    def message(self):
        return "Ошибка инициализации базы данных"
