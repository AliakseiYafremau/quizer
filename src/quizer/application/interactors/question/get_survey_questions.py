from uuid import UUID

from quizer.application.interfaces.repositories.question import QuestionRepository
from quizer.application.dto.question import ReadQuestionDTO
from quizer.application.dto.mappers.question import to_question_dto


class GetSurveyQuestionsInteractor:
    """Get all questions for a given survey.
    
    Returns a list of ReadQuestionDTO objects representing the questions
    associated with the specified survey ID."""
    def __init__(
        self,
        question_repo: QuestionRepository,
    ):
        self._question_repo = question_repo

    async def __call__(self, survey_id: UUID) -> list[ReadQuestionDTO]:
        questions = await self._question_repo.get_by_survey_id(survey_id)
        return list(map(to_question_dto, questions))
