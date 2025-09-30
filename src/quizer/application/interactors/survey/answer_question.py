from quizer.application.interfaces.common.id_provider import IdProvider
from quizer.application.interfaces.repositories.question import QuestionRepository
from quizer.application.interfaces.repositories.answer import AnswerRepository
from quizer.application.dto.answer import AnswerDTO
from quizer.application.factories.survey import AnswerFactory


class AnswerQuestionInteractor:
    def __init__(
        self,
        id_provider: IdProvider,
        question_repo: QuestionRepository,
        answer_repo: AnswerRepository,
        answer_factory: AnswerFactory,
    ):
        self._id_provider = id_provider
        self._question_repo = question_repo
        self._answer_repo = answer_repo
        self._answer_factory = answer_factory

    async def __call__(self, answer_data: AnswerDTO) -> None:
        user_id = self._id_provider.get_current_user_id()
        answer = await self._answer_repo.get_by_user_and_survey_id(
            user_id, answer_data.survey
        )

        new_answer = self._answer_factory.create_answer(
            user_id, answer_data.survey, answer_data.selections
        )

        if answer is None:
            await self._answer_repo.add(new_answer)
        else:
            await self._answer_repo.update(new_answer)
