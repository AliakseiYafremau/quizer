from quizer.application.dto.question import UpdateQuestionDTO
from quizer.application.interfaces.common.id_provider import IdProvider
from quizer.application.interfaces.repositories.question import QuestionRepository
from quizer.application.interfaces.repositories.survey import SurveyRepository
from quizer.application.exceptions import TargetNotFoundError


class UpdateQuestionInteractor:
    def __init__(
        self,
        id_provider: IdProvider,
        question_repo: QuestionRepository,
        survey_repo: SurveyRepository,
    ):
        self._id_provider = id_provider
        self._question_repo = question_repo
        self._survey_repo = survey_repo

    async def __call__(self, question_data: UpdateQuestionDTO) -> None:
        user_id = self._id_provider.get_current_user_id()

        question = await self._question_repo.get_by_id(question_data.id)
        if question is None:
            raise TargetNotFoundError("Question was not found")

        survey = await self._survey_repo.get_by_id(question.survey)
        if survey is None:
            raise TargetNotFoundError("Survey was not found")

        survey.can_manage(user_id)
        if question_data.new_name is not None:
            question.update_name(question_data.new_name)
        if question_data.options is not None:
            question.replace_options(question_data.options)

        await self._question_repo.update(question)
