from dataclasses import dataclass

from infrastructure.exceptions.base import InfraException


@dataclass(eq=False)
class DatabaseConnectionFailedException(InfraException):
    @property
    def message(self):
        return "Не удалось установить соединение с базой данных"


@dataclass(eq=False)
class DatabaseInitialFailedException(InfraException):
    @property
    def message(self):
        return "Ошибка инициализации базы данных"


@dataclass(eq=False)
class RepositoryNotFoundException(InfraException):
    @property
    def message(self):
        return "Репозиторий не найден"
