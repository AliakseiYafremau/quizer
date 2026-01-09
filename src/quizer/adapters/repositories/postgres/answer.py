import psycopg
from uuid import UUID

from quizer.entities.survey import Answer
from quizer.application.interfaces.repositories.answer import AnswerRepository
from quizer.application.factories.survey import AnswerFactory


class SQLAnswerRepository(AnswerRepository):
    def __init__(self, session: psycopg.AsyncCursor, answer_factory: AnswerFactory):
        self.session = session
        self.answer_factory = answer_factory
    
    async def add(self, answer: Answer) -> UUID:
        await self.session.execute(
            """INSERT INTO answers (id, user_id, survey_id) VALUES (%s, %s, %s)""",
            (answer.id, answer.user, answer.survey),
        )
        if answer.selections:
            await self.session.executemany(
                """
                INSERT INTO questions_answers (answer_id, question_id, option_index)
                VALUES (%s, %s, %s)
                """,
                [
                    (answer.id, question_id, option_index)
                    for question_id, option_index in answer.selections
                ],
            )
        return answer.id
