from quizer.application.interfaces.common.id_provider import IdProvider
from quizer.application.interfaces.repositories.survey import SurveyRepository
from quizer.application.dto.survey import ReadSurveyDTO
from quizer.application.dto.mappers.survey import to_survey_dto


class GetUserSurveysInteractor:
    def __init__(self, id_provider: IdProvider, surver_repo: SurveyRepository):
        self._id_provider = id_provider
        self._surver_repo = surver_repo

    async def __call__(self) -> list[ReadSurveyDTO]:
        user_id = self._id_provider.get_current_user_id()
        surveys = await self._surver_repo.get_by_user_id(user_id)
        return list(map(to_survey_dto, surveys))
