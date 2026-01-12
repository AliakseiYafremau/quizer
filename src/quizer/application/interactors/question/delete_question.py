from uuid import UUID

from quizer.application.interfaces.common.id_provider import IdProvider
from quizer.application.interfaces.repositories.question import QuestionRepository
from quizer.application.interfaces.repositories.survey import SurveyRepository
from quizer.application.exceptions import TargetNotFoundError


class DeleteQuestionInteractor:
    def __init__(
        self,
        id_provider: IdProvider,
        question_repo: QuestionRepository,
        survey_repo: SurveyRepository,
    ):
        self._id_provider = id_provider
        self._question_repo = question_repo
        self._survey_repo = survey_repo

    async def __call__(self, question_id: UUID) -> None:
        user_id = self._id_provider.get_current_user_id()

        question = await self._question_repo.get_by_id(question_id)
        if question is None:
            raise TargetNotFoundError("Question was not found")

        survey = await self._survey_repo.get_by_id(question.survey)
        if survey is None:
            raise TargetNotFoundError("Survey was not found")

        survey.can_manage(user_id)

        await self._question_repo.delete(question_id)
