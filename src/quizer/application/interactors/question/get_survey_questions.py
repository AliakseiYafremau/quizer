from uuid import UUID

from quizer.entities.survey import Question
from quizer.application.interfaces.common.id_provider import IdProvider
from quizer.application.interfaces.repositories.question import QuestionRepository
from quizer.application.interfaces.repositories.survey import SurveyRepository
from quizer.application.dto.question import ReadQuestionDTO
from quizer.application.dto.mappers.question import to_question_dto
from quizer.application.exceptions import TargetNotFoundError


class GetSurveyQuestionsInteractor:
    def __init__(
        self,
        question_repo: QuestionRepository,
    ):
        self._question_repo = question_repo

    async def __call__(self, survey_id: UUID) -> list[ReadQuestionDTO]:
        questions = await self._question_repo.get_by_survey_id(survey_id)
        return list(map(to_question_dto, questions))
