import psycopg
from uuid import UUID

from quizer.entities.survey import Answer
from quizer.application.interfaces.repositories.answer import AnswerRepository
from quizer.application.factories.survey import AnswerFactory


class SQLAnswerRepository(AnswerRepository):
    def __init__(self, session: psycopg.AsyncCursor, answer_factory: AnswerFactory):
        self.session = session
        self.answer_factory = answer_factory

    async def get_by_user_and_survey_id(
        self, user_id: str, survey_id: UUID
    ) -> Answer | None:
        await self.session.execute(
            """
            SELECT
                answers.id,
                answers.user_id,
                answers.survey_id,
                questions_answers.question_id,
                questions_answers.option_index
            FROM answers
            LEFT JOIN questions_answers
            ON questions_answers.answer_id = answers.id
            WHERE answers.user_id = %s AND answers.survey_id = %s
            ORDER BY questions_answers.id
            """,
            (user_id, survey_id),
        )
        rows = await self.session.fetchall()
        if not rows:
            return None

        answer_id = rows[0][0]
        selections = [
            (UUID(row[3]), row[4]) for row in rows if row[3] is not None
        ]
        return self.answer_factory.create_answer(
            user_id=rows[0][1],
            survey_id=rows[0][2],
            selections=tuple(selections),
            id=UUID(answer_id),
        )

    async def get_by_survey_id(self, survey_id: UUID) -> list[Answer]:
        await self.session.execute(
            """
            SELECT
                answers.id,
                answers.user_id,
                answers.survey_id,
                questions_answers.question_id,
                questions_answers.option_index
            FROM answers
            LEFT JOIN questions_answers
            ON questions_answers.answer_id = answers.id
            WHERE answers.survey_id = %s
            ORDER BY answers.id, questions_answers.id
            """,
            (survey_id,),
        )
        rows = await self.session.fetchall()
        if not rows:
            return []

        answers_map: dict[str, dict] = {}
        for answer_id, user_id, survey_id, question_id, option_index in rows:
            bucket = answers_map.setdefault(
                answer_id,
                {
                    "user": user_id,
                    "survey": survey_id,
                    "selections": [],
                },
            )
            if question_id is not None:
                bucket["selections"].append((UUID(question_id), option_index))

        return [
            self.answer_factory.create_answer(
                user_id=data["user"],
                survey_id=UUID(data["survey"]),
                selections=tuple(data["selections"]),
                id=UUID(answer_id),
            )
            for answer_id, data in answers_map.items()
        ]
    
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

    async def update(self, answer: Answer) -> UUID:
        await self.session.execute(
            """
            UPDATE answers
            SET user_id = %s, survey_id = %s
            WHERE id = %s
            """,
            (answer.user, answer.survey, answer.id),
        )
        await self.session.execute(
            "DELETE FROM questions_answers WHERE answer_id = %s",
            (answer.id,),
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
