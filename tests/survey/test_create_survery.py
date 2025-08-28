from uuid import uuid4
from faker import Faker

from unittest.mock import create_autospec

from quizer.application.interactors.survey.create_survey import CreateSurveryInteractor
from quizer.application.interfaces.common.id_provider import IdProvider
from quizer.application.interfaces.repositories.survey import SurveyRepository
from quizer.application.factories.survey import SurveyFactory
from quizer.entities.survey import Survey


async def test_survery_creation(survey_factory, faker: Faker):
    # Arrange
    user_id = faker.telegram_id()
    survey_name = faker.sentence()

    id_provider_stub = create_autospec(IdProvider)
    survey_repo_mock = create_autospec(SurveyRepository)

    id_provider_stub.get_current_user_id.return_value = user_id

    interactor = CreateSurveryInteractor(
        id_provider_stub, survey_repo_mock, survey_factory
    )

    # Act
    await interactor(survey_name)

    # Assert
    survey_repo_mock.add.assert_called_once()
    new_survey: Survey = survey_repo_mock.add.call_args.args[0]
    assert new_survey.name == survey_name
    assert new_survey.author == user_id
