from dataclasses import dataclass

from domain.exceptions.base import ApplicationException


@dataclass(eq=False)
class InfrastructureException(ApplicationException):
    @property
    def message(self):
        return "Ошибка на уровне инфраструктуры"
