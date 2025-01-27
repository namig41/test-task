from functools import lru_cache

from infrastructure.jwt.base import BaseJWTProcessor
from infrastructure.jwt.config import JWTConfig
from infrastructure.jwt.jwt_processor import PyJWTProcessor
from settings.config import settings


@lru_cache(1)
def py_jwt_processor_factory() -> BaseJWTProcessor:
    jwt_config: JWTConfig = JWTConfig(
        settings.JWT_SECRET_KEY,
        settings.JWT_ALGORITHM,
    )

    return PyJWTProcessor(jwt_config)
