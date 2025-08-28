import pytest
from faker import Faker
from uuid import uuid4

from tests.provider import TelegramIdProvider, get_faker

from quizer.application.factories.survey import SurveyFactory, AnswerFactory
from quizer.application.interfaces.common.uuid_generator import UUIDGenerator


@pytest.fixture
def faker() -> Faker:
    return get_faker(TelegramIdProvider)


@pytest.fixture(scope="session")
def uuid_generator() -> UUIDGenerator:
    return uuid4


@pytest.fixture(scope="session")
def survey_factory(uuid_generator: UUIDGenerator) -> SurveyFactory:
    return SurveyFactory(uuid_generator)


@pytest.fixture(scope="session")
def answer_factory(uuid_generator: UUIDGenerator) -> AnswerFactory:
    return AnswerFactory(uuid_generator)
