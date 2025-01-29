from faker import Faker
from punq import Container

from bootstrap.di import _init_container
from domain.entities.github import (
    Repository,
    RepositoryAuthorCommitsNum,
)


def init_dummy_container() -> Container:
    container: Container = _init_container()
    return container


def get_random_repository(faker: Faker) -> Repository:
    return Repository(
        name=faker.name(),
        owner=faker.name(),
        position=faker.pyint(0, 100),
        watchers=faker.pyint(),
        stars=faker.pyint(),
        forks=faker.pyint(),
        language=faker.language_name(),
    )


def get_random_author_commits(author: str, faker: Faker) -> list[RepositoryAuthorCommitsNum]:
    return [
        RepositoryAuthorCommitsNum(author=author, commits_num=faker.pyint())
        for _ in range(faker.pyint(max_value=50))
    ]
