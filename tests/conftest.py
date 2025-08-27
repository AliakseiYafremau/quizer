import pytest
from faker import Faker

from tests.provider import TelegramIdProvider, get_faker


@pytest.fixture
def faker() -> Faker:
    return get_faker(TelegramIdProvider)
