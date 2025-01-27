from dataclasses import dataclass

from infrastructure.exceptions.base import InfraException


@dataclass(eq=False)
class JWTDecodeException(InfraException):
    @property
    def message(self):
        return "Ошибка декодирования токена"


@dataclass(eq=False)
class JWTExpiredException(InfraException):
    @property
    def message(self):
        return "Истек срок действия токена"
