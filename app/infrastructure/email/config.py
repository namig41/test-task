from dataclasses import dataclass

from settings.config import settings


@dataclass
class SMTPConfig:
    username: str = settings.SMTP_USERNAME
    password: str = settings.SMTP_PASSWORD
    port: int = settings.SMTP_PORT
    host: str = settings.SMTP_HOST
    use_tls: bool = True
