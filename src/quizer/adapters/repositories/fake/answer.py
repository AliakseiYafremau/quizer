from uuid import uuid4, UUID

from quizer.entities.survey import Answer
from quizer.application.interfaces.repositories.answer import AnswerRepository


class FakeAnswerRepository(AnswerRepository):
    async def get_by_user_and_survey_id(
        self, user_id: str, survey_id: UUID
    ) -> Answer | None:
        return None

    async def get_by_survey_id(self, survey_id: UUID) -> list[Answer]:
        return []

    async def add(self, answer: Answer) -> UUID:
        return uuid4()

    async def update(self, answer: Answer) -> UUID:
        return uuid4()
