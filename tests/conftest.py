from random import SystemRandom
from typing import (
    Any,
    AsyncGenerator,
)

import pytest
import pytest_asyncio
from faker import Faker
from punq import Container

from infrastructure.repositories.github.database.base import BaseGitHubRepository
from tests.fixtures import init_dummy_container


@pytest.fixture(scope="session")
def container() -> Container:
    return init_dummy_container()


@pytest.fixture(scope="session")
def faker() -> Faker:
    faker_instance: Faker = Faker()
    return faker_instance


@pytest_asyncio.fixture(scope="session", autouse=True)
async def setup_before_all_tests(container: Container, faker: Faker) -> AsyncGenerator[Any, Any, Any]:
    random_seed: int = SystemRandom().randint(0, 9999)
    faker.seed_instance(random_seed)

    repository: BaseGitHubRepository = container.resolve(BaseGitHubRepository)
    await repository.create_db(database_name="test")
    await repository.create_tables()

    yield

    await repository.drop_tables()
