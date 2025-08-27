from uuid import UUID
from quizer.application.interfaces.repositories.survey import SurveyRepository
from quizer.application.interfaces.common.id_provider import IdProvider


class DeleteSurveyInteractor:
    def __init__(self, survey_repo: SurveyRepository, id_provider: IdProvider):
        self._survey_repo = survey_repo
        self._id_provider = id_provider

    async def __call__(self, survey_id: UUID) -> None:
        user_id = self._id_provider.get_current_user_id()
        survey = await self._survey_repo.get_by_id(survey_id)
        survey.can_delete(user_id)
        await self._survey_repo.delete(survey_id)
