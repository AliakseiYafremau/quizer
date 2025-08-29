from quizer.entities.survey import Question
from quizer.application.interfaces.repositories.question import QuestionRepository


class FakeQuestionRepository(QuestionRepository):
    async def get_by_id(self, question_id):
        return Question(
            id=question_id,
            name="name",
            options=[],
        )

    async def get_by_survey_id(self, survey_id):
        return []
