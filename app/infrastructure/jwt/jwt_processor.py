from dataclasses import dataclass

import jwt

from infrastructure.exceptions.jwt_token import (
    JWTDecodeException,
    JWTExpiredException,
)
from infrastructure.jwt.base import (
    BaseJWTProcessor,
    JWTPayloadDict,
    JWTToken,
)
from infrastructure.jwt.config import JWTConfig


@dataclass
class PyJWTProcessor(BaseJWTProcessor):
    jwt_config: JWTConfig

    def encode(self, payload: JWTPayloadDict) -> JWTToken:
        return jwt.encode(payload, self.jwt_config.key, self.jwt_config.algorithm)

    def decode(self, token: JWTToken) -> JWTPayloadDict:
        try:
            return jwt.decode(
                token,
                self.jwt_config.key,
                algorithms=[self.jwt_config.algorithm],
            )
        except jwt.ExpiredSignatureError:
            raise JWTExpiredException()
        except jwt.DecodeError:
            raise JWTDecodeException()
