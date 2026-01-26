from unittest.mock import create_autospec

from tests.factories import make_user, make_survey

from quizer.application.interfaces.common.id_provider import IdProvider
from quizer.application.interfaces.repositories.survey import SurveyRepository
from quizer.application.interactors.user.get_user_surveys import (
    GetUserSurveysInteractor,
)
from quizer.application.dto.mappers.survey import to_survey_dto


async def test_user_surveys_recieving():
    # Arrange
    user = make_user()
    surveys = [make_survey(author=user.id) for _ in range(3)]
    surveys_dto = list(map(to_survey_dto, surveys))
    id_provider = create_autospec(IdProvider)
    survey_repo_mock = create_autospec(SurveyRepository)

    survey_repo_mock.get_by_user_id.return_value = surveys

    interactor = GetUserSurveysInteractor(id_provider, survey_repo_mock)

    # Act
    result = await interactor()

    # Assert
    assert result == surveys_dto
