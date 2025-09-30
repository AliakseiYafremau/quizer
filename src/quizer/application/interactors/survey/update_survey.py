from quizer.application.dto.survey import UpdateSurveyDTO
from quizer.application.interfaces.repositories.survey import SurveyRepository
from quizer.application.interfaces.common.id_provider import IdProvider
from quizer.application.exceptions import TargetNotFoundError


class UpdateSurveyInteractor:
    def __init__(self, id_provider: IdProvider, survey_repo: SurveyRepository):
        self._id_provider = id_provider
        self._survey_repo = survey_repo

    async def __call__(self, survey_data: UpdateSurveyDTO) -> None:
        user_id = self._id_provider.get_current_user_id()
        survey = await self._survey_repo.get_by_id(survey_data.id)
        if survey is None:
            raise TargetNotFoundError("Survey was not found")

        survey.can_manage(user_id)
        survey.update_name(survey_data.new_name)

        await self._survey_repo.update(survey)
