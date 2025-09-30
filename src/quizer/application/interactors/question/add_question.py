from uuid import UUID

from quizer.application.interfaces.common.id_provider import IdProvider
from quizer.application.interfaces.repositories.question import QuestionRepository
from quizer.application.interfaces.repositories.user import UserRepository
from quizer.application.interfaces.repositories.survey import SurveyRepository
from quizer.application.factories.survey import QuestionFactory
from quizer.application.dto.question import CreateQuestionDTO
from quizer.application.exceptions import TargetNotFoundError


class AddSurveyQuestionInteractor:
    def __init__(
        self,
        id_provider: IdProvider,
        question_repo: QuestionRepository,
        survey_repo: SurveyRepository,
        user_repo: UserRepository,
        question_factory: QuestionFactory,
    ):
        self._id_provider = id_provider
        self._question_repo = question_repo
        self._survey_repo = survey_repo
        self._user_repo = user_repo
        self._question_factory = question_factory

    async def __call__(self, question_data: CreateQuestionDTO) -> UUID:
        user_id = self._id_provider.get_current_user_id()
        user_surveys = await self._survey_repo.get_by_user_id(user_id)
        if question_data.survey_id not in user_surveys:
            raise TargetNotFoundError("Survey was not found")

        new_question = self._question_factory.create_question(
            name=question_data.name, options=question_data.options
        )
        return await self._question_repo.add(new_question)
