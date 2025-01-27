from random import SystemRandom

import pytest
import pytest_asyncio
from faker import Faker
from punq import Container
from sqlalchemy.ext.asyncio.engine import AsyncEngine

from infrastructure.database.utils import (
    create_database,
    drop_database,
    start_entity_mappers,
)
from tests.fixtures import init_dummy_container


@pytest.fixture(scope="session")
def container() -> Container:
    return init_dummy_container()


@pytest.fixture(scope="session")
def faker() -> Faker:
    faker_instance: Faker = Faker()
    return faker_instance


@pytest_asyncio.fixture(scope="session", autouse=True)
async def setup_before_all_tests(container: Container, faker: Faker) -> None:
    random_seed: int = SystemRandom().randint(0, 9999)
    faker.seed_instance(random_seed)

    engine: AsyncEngine = container.resolve(AsyncEngine)
    await drop_database(engine)
    await create_database(engine)
    start_entity_mappers()
