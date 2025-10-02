import psycopg

from quizer.entities.survey import Question
from quizer.application.interfaces.repositories.question import QuestionRepository
from quizer.application.factories.survey import QuestionFactory


class SQLQuestionRepository(QuestionRepository):
    def __init__(self, session: psycopg.AsyncCursor):
        self.session = session

    async def get_by_id(self, question_id) -> Question | None:
        await self.session.execute(
            "SELECT name FROM questions WHERE id = &s", (question_id,)
        )
        question_name = self.session.fetchone()
        if question_name is None:
            return None
        await self.session.execute(
            "SELECT value FROM question_options WHERE question_id = &s", (question_id,)
        )
        options = await self.session.fetchall()
        return QuestionFactory().create_question(
            id=question_id, name=question_name, options=options
        )
