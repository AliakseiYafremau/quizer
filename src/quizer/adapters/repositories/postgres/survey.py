import psycopg
from uuid import UUID

from quizer.entities.survey import Survey
from quizer.application.interfaces.repositories.survey import SurveyRepository


class SQLSurveyRepository(SurveyRepository):
    def __init__(self, session: psycopg.AsyncCursor):
        self.session = session

    async def get_by_id(self, id: UUID) -> Survey | None:
        await self.session.execute(
            """
            SELECT
                survey.id,
                survey.name,
                survey.author,
                survey.is_available,
                questions.id
            FROM survey
            LEFT JOIN questions
            ON questions.survey_id = survey.id
            WHERE survey.id = %s
            ORDER BY questions.id
            """,
            (id,),
        )
        rows = await self.session.fetchall()
        if not rows:
            return None

        survey_id, name, author, is_available, _ = rows[0]
        questions = [UUID(row[4]) for row in rows if row[4] is not None]
        return Survey(
            id=UUID(survey_id),
            name=name,
            author=author,
            questions=questions,
            is_available=is_available,
        )

    async def get_by_user_id(self, user_id: str) -> list[Survey]:
        await self.session.execute(
            """
            SELECT
                survey.id,
                survey.name,
                survey.author,
                survey.is_available,
                questions.id
            FROM survey
            LEFT JOIN questions
            ON questions.survey_id = survey.id
            WHERE survey.author = %s
            ORDER BY survey.id, questions.id
            """,
            (user_id,),
        )
        rows = await self.session.fetchall()
        return self._build_surveys(rows)

    async def get_all(self) -> list[Survey]:
        await self.session.execute(
            """
            SELECT
                survey.id,
                survey.name,
                survey.author,
                survey.is_available,
                questions.id
            FROM survey
            LEFT JOIN questions
            ON questions.survey_id = survey.id
            ORDER BY survey.id, questions.id
            """
        )
        rows = await self.session.fetchall()
        return self._build_surveys(rows)

    async def add(self, survey: Survey) -> UUID:
        await self.session.execute(
            """
            INSERT INTO survey (id, name, author, is_available)
            VALUES (%s, %s, %s, %s)
            """,
            (survey.id, survey.name, survey.author, survey.is_available),
        )
        return survey.id

    async def update(self, survey: Survey) -> None:
        await self.session.execute(
            """
            UPDATE survey
            SET name = %s, is_available = %s
            WHERE id = %s
            """,
            (survey.name, survey.is_available, survey.id),
        )

    async def delete(self, id: UUID) -> None:
        await self.session.execute(
            """
            DELETE FROM questions_answers
            WHERE question_id IN (SELECT id FROM questions WHERE survey_id = %s)
               OR answer_id IN (SELECT id FROM answers WHERE survey_id = %s)
            """,
            (id, id),
        )
        await self.session.execute(
            "DELETE FROM questions_options WHERE question_id IN (SELECT id FROM questions WHERE survey_id = %s)",
            (id,),
        )
        await self.session.execute(
            "DELETE FROM answers WHERE survey_id = %s",
            (id,),
        )
        await self.session.execute(
            "DELETE FROM questions WHERE survey_id = %s",
            (id,),
        )
        await self.session.execute("DELETE FROM survey WHERE id = %s", (id,))

    @staticmethod
    def _build_surveys(rows: list[tuple]) -> list[Survey]:
        if not rows:
            return []
        surveys_map: dict[str, dict] = {}
        for survey_id, name, author, is_available, question_id in rows:
            bucket = surveys_map.setdefault(
                survey_id,
                {
                    "name": name,
                    "author": author,
                    "is_available": is_available,
                    "questions": [],
                },
            )
            if question_id is not None:
                bucket["questions"].append(UUID(question_id))
        return [
            Survey(
                id=UUID(survey_id),
                name=data["name"],
                author=data["author"],
                questions=data["questions"],
                is_available=data["is_available"],
            )
            for survey_id, data in surveys_map.items()
        ]
