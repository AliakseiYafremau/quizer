import pytest
from faker import Faker

from provider import TelegramIdProvider, get_faker


@pytest.fixture
def faker() -> Faker:
    return get_faker(TelegramIdProvider)
