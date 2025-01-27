import json
from dataclasses import (
    asdict,
    dataclass,
)
from datetime import (
    datetime,
    timedelta,
    timezone,
)
from typing import (
    Any,
    TypeAlias,
)

from domain.entities.base import BaseEntity
from infrastructure.exceptions.jwt_token import JWTExpiredException


JWTPayloadDict: TypeAlias = dict[str, Any]
JWTToken: TypeAlias = str


@dataclass
class JWTPayload:
    user_id: int
    login: str

    def to_raw(self) -> str:
        return json.dumps(asdict(self))

    @classmethod
    def from_dict(cls, payload_dict: JWTPayloadDict) -> "JWTPayload":
        return cls(**payload_dict)

    @classmethod
    def from_raw(cls, raw_payload: str) -> "JWTPayload":
        return cls.from_dict(json.loads(raw_payload))

    def __str__(self):
        return self.to_raw()


@dataclass
class AccessToken(BaseEntity):
    payload: JWTPayload
    expires_in: datetime

    def validate(self) -> None:
        if datetime.now(timezone.utc) > self.expires_in:
            raise JWTExpiredException()

    @classmethod
    def create_with_expiration(
        cls,
        payload: JWTPayload,
        minutes: int = 5,
    ) -> "AccessToken":
        return cls(
            payload=payload,
            expires_in=datetime.now(timezone.utc) + timedelta(minutes=minutes),
        )

    @classmethod
    def from_payload_dict(
        cls,
        payload_dict: JWTPayloadDict,
        minutes: int = 5,
    ) -> "AccessToken":
        payload: JWTPayload = JWTPayload.from_dict(payload_dict)
        return cls.create_with_expiration(payload=payload, minutes=minutes)
