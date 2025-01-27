from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import dataclass

from infrastructure.jwt.access_token import (
    JWTPayloadDict,
    JWTToken,
)
from infrastructure.jwt.config import JWTConfig


@dataclass
class BaseJWTProcessor(ABC):
    jwt_config: JWTConfig

    @abstractmethod
    def encode(self, payload: JWTPayloadDict) -> JWTToken: ...

    @abstractmethod
    def decode(self, token: JWTToken) -> JWTPayloadDict: ...
