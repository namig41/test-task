from dataclasses import dataclass

from infrastructure.exceptions.base import InfrastructureException


@dataclass(eq=False)
class RepositoryNotFoundException(InfrastructureException):
    @property
    def message(self):
        return "Репозиторий не найден"


@dataclass(eq=False)
class RepositoryTimeOutException(InfrastructureException):
    @property
    def message(self):
        return "Запрос превысил лимит времени (тайм-аут)"


@dataclass(eq=False)
class RepositoryCommonException(InfrastructureException):
    @property
    def message(self):
        return "Ошибка при работе репозитория"
