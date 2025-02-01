from dataclasses import dataclass

from app.domain.entities.base import BaseEntity


@dataclass
class RepositoryAuthorCommitsNum(BaseEntity):
    author: str
    commits_num: int

    def validate(self) -> None: ...


@dataclass
class Repository(BaseEntity):
    name: str
    owner: str
    position: int
    stars: int
    watchers: int
    forks: int
    language: str
    authors_commits_num_today: list[RepositoryAuthorCommitsNum] | None = None

    def validate(self) -> None: ...
