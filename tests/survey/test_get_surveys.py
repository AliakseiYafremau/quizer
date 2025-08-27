from unittest.mock import create_autospec

from factories import make_survey

from quizer.application.interfaces.repositories.survey import SurveyRepository
from quizer.application.dto.mappers.survey import to_survey_dto
from quizer.application.interactors.survey.get_all_surveys import (
    GetAllSurveysInteractor,
)


async def test_recieving_all_surveys():
    surveys = [make_survey() for _ in range(3)]
    surveys_dto = list(map(to_survey_dto, surveys))
    survey_repo_stub = create_autospec(SurveyRepository)
    survey_repo_stub.get_all.return_value = surveys
    interactor = GetAllSurveysInteractor(survey_repo_stub)

    result = await interactor()

    assert result == surveys_dto
