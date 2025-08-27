import pytest
from faker import Faker

from provider import TelegramIdProvider


@pytest.fixture
def faker() -> Faker:
    faker = Faker()
    faker.add_provider(TelegramIdProvider)
    return faker
