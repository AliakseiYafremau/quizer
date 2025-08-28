from typing import Protocol
from abc import abstractmethod

from uuid import UUID

from quizer.entities.survey import Question


class QuestionRepository(Protocol):
    @abstractmethod
    async def get_by_id(self, question_id: UUID) -> Question | None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_survey_id(self, survey_id: UUID) -> list[Question]:
        raise NotImplementedError
