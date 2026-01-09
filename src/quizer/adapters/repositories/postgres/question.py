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
                questions.survey_id,
                questions_options.value,
                questions_options.position
            FROM questions
            LEFT JOIN questions_options
            ON questions_options.question_id = questions.id
            WHERE id = %s
            ORDER BY questions_options.position
            """,
            (question_id,),
        )
        rows = await self.session.fetchall()

        if not rows:
            return None

        name = rows[0][0]
        survey_id = rows[0][1]
        options = [row[2] for row in rows if row[2] is not None]

        return self.question_factory.create_question(
            id=question_id, name=name, survey=survey_id, options=options
        )

    async def get_by_survey_id(self, survey_id: UUID) -> list[Question]:
        await self.session.execute(
            """
            SELECT
                questions.id,
                questions.name,
                questions.survey_id,
                questions_options.value,
                questions_options.position
            FROM questions
            LEFT JOIN questions_options
            ON questions.id = questions_options.question_id
            WHERE questions.survey_id = %s
            ORDER BY questions.id, questions_options.position
            """,
            (survey_id,),
        )
        rows = await self.session.fetchall()
        if not rows:
            return []

        questions_map: dict[str, dict] = {}
        for id, name, survey_id, option, position in rows:
            bucket = questions_map.setdefault(
                id,
                {
                    "name": name,
                    "survey": survey_id,
                    "options": [],
                },
            )
            if option is not None:
                bucket["options"].append((position, option))

        return [
            self.question_factory.create_question(
                id=UUID(id),
                name=data["name"],
                survey=UUID(data["survey"]),
                options=[option for _, option in sorted(data["options"])],
            )
            for id, data in questions_map.items()
        ]

    async def add(self, question: Question):
        await self.session.execute(
            """INSERT INTO questions (id, name, survey_id) VALUES (%s, %s, %s)""",
            (question.id, question.name, question.survey),
        )
        if question.options:
            await self.session.executemany(
                """
                INSERT INTO questions_options (value, question_id, position)
                VALUES (%s, %s, %s)
                """,
                [
                    (option, question.id, position)
                    for position, option in enumerate(question.options)
                ],
            )
        return question.id
