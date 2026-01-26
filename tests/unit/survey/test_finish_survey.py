import pytest
from faker import Faker
from unittest.mock import create_autospec

from tests.factories import make_survey

from quizer.application.exceptions import TargetNotFoundError
from quizer.application.interfaces.common.id_provider import IdProvider
from quizer.application.interfaces.repositories.survey import SurveyRepository
from quizer.application.interactors.survey.finish_survey import SaveSurveyInteractor
from quizer.entities.exceptions import AccessDeniedError


async def test_finish_survey_with_owner(uuid_generator, faker: Faker):
    # Arrange
    survey_id = uuid_generator()
    user_id = faker.telegram_id()
    survey = make_survey(id=survey_id, author=user_id)

    survey_repo_mock = create_autospec(SurveyRepository)
    id_provider_stub = create_autospec(IdProvider)

    survey_repo_mock.get_by_id.return_value = survey
    id_provider_stub.get_current_user_id.return_value = user_id

    interactor = SaveSurveyInteractor(id_provider_stub, survey_repo_mock)

    # Act
    await interactor(survey_id)

    # Assert
    survey_repo_mock.update.assert_called_once()
    updated_survey = survey_repo_mock.update.call_args.args[0]
    assert updated_survey.is_available is True


async def test_finish_survey_with_unknown_survey(uuid_generator):
    # Arrange
    survey_id = uuid_generator()
    survey_repo_mock = create_autospec(SurveyRepository)
    id_provider_stub = create_autospec(IdProvider)

    survey_repo_mock.get_by_id.return_value = None

    interactor = SaveSurveyInteractor(id_provider_stub, survey_repo_mock)

    # Act
    with pytest.raises(TargetNotFoundError):
        await interactor(survey_id)

    # Assert
    survey_repo_mock.update.assert_not_called()


async def test_finish_survey_with_stranger(uuid_generator, faker: Faker):
    # Arrange
    survey_id = uuid_generator()
    author_id = faker.unique.telegram_id()
    user_id = faker.unique.telegram_id()
    survey = make_survey(id=survey_id, author=author_id)

    survey_repo_mock = create_autospec(SurveyRepository)
    id_provider_stub = create_autospec(IdProvider)

    survey_repo_mock.get_by_id.return_value = survey
    id_provider_stub.get_current_user_id.return_value = user_id

    interactor = SaveSurveyInteractor(id_provider_stub, survey_repo_mock)

    # Act
    with pytest.raises(AccessDeniedError):
        await interactor(survey_id)

    # Assert
    survey_repo_mock.update.assert_not_called()
