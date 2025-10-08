import psycopg
from uuid import UUID

from quizer.entities.survey import Question
from quizer.application.interfaces.repositories.question import QuestionRepository
from quizer.application.factories.survey import QuestionFactory


class SQLQuestionRepository(QuestionRepository):
    def __init__(self, session: psycopg.AsyncCursor, question_factory: QuestionFactory):
        self.session = session
        self.question_factory = question_factory

    async def get_by_id(self, question_id) -> Question | None:
        await self.session.execute(
            """
            SELECT
                questions.name,
                questions_options.value
            FROM questions
            LEFT JOIN questions_options
            ON questions_options.question_id = &s
            WHERE id = &s
            """,
            (question_id, question_id),
        )
        rows = await self.session.fetchall()

        if not rows:
            return None

        if rows[0][1] is None:
            return self.question_factory.create_question(
                id=question_id, name=rows[0][0], options=[]
            )
        return self.question_factory.create_question(
            id=question_id, name=rows[0][0], options=[row[1] for row in rows]
        )

    async def get_by_survey_id(self, survey_id: UUID) -> list[Question]:
        await self.session.execute(
            """
            SELECT
                questions.id,
                questions.name,
                questions_options.value
            FROM questions
            LEFT JOIN questions_options
            ON question.id = questions_options.question_id
            WHERE questions.survey_id = &s
            """,
            (survey_id,),
        )
        rows = await self.session.fetchall()
        if not rows:
            return []
        questions_map = {}
        for id, name, option in rows:
            if option is None and id not in questions_map:
                questions_map[id] = {
                    "name": name,
                    "options": [],
                }
            elif option is not None and id not in questions_map:
                questions_map[id] = {
                    "name": name,
                    "options": [option],
                }
            elif option is not None and id in questions_map:
                questions_map[id]["options"].append(option)
        return [
            self.question_factory.create_question(
                id=id_key,
                name=questions_map[id_key]["name"],
                options=questions_map[id_key]["options"],
            )
            for id_key in questions_map.keys()
        ]

    async def add(self, question: Question):
        await self.session.execute(
            """INSERT INTO users (id, name) VALUES (&s, &s, &s)""",
            (question.id, question.name),
        )
        for option in question.options:
            await self.session.execute(
                """INSERT INTO questions_options (value, question_id) VALUES (&s, &s)""",
                (option, question.id),
            )
