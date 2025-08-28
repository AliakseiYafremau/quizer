from uuid import UUID

from quizer.application.interfaces.common.id_provider import IdProvider
from quizer.application.interfaces.repositories.survey import SurveyRepository
from quizer.application.factories.survey import SurveyFactory


class CreateSurveryInteractor:
    def __init__(
        self,
        id_provider: IdProvider,
        survey_repo: SurveyRepository,
        survey_factory: SurveyFactory,
    ):
        self._id_provider = id_provider
        self._survey_repo = survey_repo
        self._survey_factory = survey_factory

    async def __call__(self, survey_name: str) -> UUID:
        user_id = self._id_provider.get_current_user_id()
        survey = self._survey_factory.create_survey(name=survey_name, author=user_id)
        return await self._survey_repo.add(survey)
