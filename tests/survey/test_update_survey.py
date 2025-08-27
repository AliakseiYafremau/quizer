from faker import Faker
from uuid import uuid4

from unittest.mock import create_autospec

from factories import make_survey

from quizer.application.dto.survey import UpdateSurveyDTO
from quizer.application.interactors.survey.update_survey import UpdateSurveyInteractor
from quizer.application.interfaces.common.id_provider import IdProvider
from quizer.application.interfaces.repositories.survey import SurveyRepository


async def test_user_update_with_owner(faker: Faker):
    user_id = faker.telegram_id()
    old_name = faker.unique.name()
    new_name = faker.unique.name()
    survey = make_survey(name=old_name, author=user_id)
    survey_dto = UpdateSurveyDTO(uuid4(), new_name)
    survey_repo_mock = create_autospec(SurveyRepository)
    id_provider = create_autospec(IdProvider)
    id_provider.get_current_user_id.return_value = user_id
    survey_repo_mock.get_by_id.return_value = survey
    interactor = UpdateSurveyInteractor(id_provider, survey_repo_mock)

    await interactor(survey_dto)

    survey_repo_mock.update.assert_called_once()
    new_survey = survey_repo_mock.update.call_args.args[0]
    assert new_survey.name == new_name
