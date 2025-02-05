from pydantic import BaseModel

from domain.entities.github import Repository


class RepositoryResponseSchema(BaseModel):
    name: str
    owner: str
    position: int
    stars: int
    watchers: int
    forks: int
    language: str

    @classmethod
    def from_entity(cls, repository: Repository) -> "RepositoryResponseSchema":
        return cls(
            name=repository.name,
            owner=repository.owner,
            position=repository.position,
            stars=repository.stars,
            watchers=repository.watchers,
            forks=repository.forks,
            language=repository.language,
        )
