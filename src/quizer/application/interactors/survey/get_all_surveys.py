from quizer.application.dto.mappers.survey import to_survey_dto
from quizer.application.interfaces.repositories.survey import SurveyRepository
from quizer.application.dto.survey import ReadSurveyDTO


class GetAllSurveysInteractor:
    def __init__(self, survey_repo: SurveyRepository):
        self._survey_repo = survey_repo

    async def __call__(self) -> list[ReadSurveyDTO]:
        return list(map(to_survey_dto, await self._survey_repo.get_all()))
