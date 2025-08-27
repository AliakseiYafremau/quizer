import pytest
from faker import Faker

from unittest.mock import create_autospec
from uuid import uuid4

from tests.factories import make_survey

from quizer.application.interfaces.common.id_provider import IdProvider
from quizer.application.interfaces.repositories.survey import SurveyRepository
from quizer.entities.exceptions import AccessDeniedError
from quizer.application.interactors.survey.delete_survey import DeleteSurveyInteractor


async def test_survery_deletion_with_owner(faker: Faker):
    survey_id = uuid4()
    user_id = faker.telegram_id()
    survey_repo_mock = create_autospec(SurveyRepository)
    id_provider_stub = create_autospec(IdProvider)
    survey = make_survey(id=survey_id, author=user_id)
    survey_repo_mock.get_by_id.return_value = survey
    id_provider_stub.get_current_user_id.return_value = user_id
    interactor = DeleteSurveyInteractor(survey_repo_mock, id_provider_stub)

    await interactor(survey_id)

    survey_repo_mock.delete.assert_called_once_with(survey_id)


async def test_survery_deletion_with_stranger(faker: Faker):
    survey_id = uuid4()
    user_id = faker.unique.telegram_id()
    author_id = faker.unique.telegram_id()
    survey_repo_mock = create_autospec(SurveyRepository)
    id_provider_stub = create_autospec(IdProvider)
    survey = make_survey(id=survey_id, author=author_id)
    survey_repo_mock.get_by_id.return_value = survey
    id_provider_stub.get_current_user_id.return_value = user_id
    interactor = DeleteSurveyInteractor(survey_repo_mock, id_provider_stub)

    with pytest.raises(AccessDeniedError):
        await interactor(survey_id)

    survey_repo_mock.delete.assert_not_called()
