from typing import Protocol
from abc import abstractmethod

from uuid import UUID

from quizer.entities.survey import Answer


class AnswerRepository(Protocol):
    @abstractmethod
    async def get_by_user_and_question_id(
        self, user_id: str, question_id: UUID
    ) -> Answer | None:
        raise NotImplementedError

    @abstractmethod
    async def add(self, answer: Answer) -> UUID:
        raise NotImplementedError

    @abstractmethod
    async def update(self, answer: Answer) -> UUID:
        raise NotImplementedError
