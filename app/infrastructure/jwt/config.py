from dataclasses import dataclass
from typing import Literal

from settings.config import settings


Algorithm = Literal[
    "HS256",
    "HS384",
    "HS512",
    "RS256",
    "RS384",
    "RS512",
]


@dataclass(frozen=True)
class JWTConfig:
    key: str = settings.JWT_SECRET_KEY
    algorithm: Algorithm = settings.JWT_ALGORITHM
