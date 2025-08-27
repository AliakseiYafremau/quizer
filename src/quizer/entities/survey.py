from uuid import UUID
from dataclasses import dataclass

from quizer.entities.exceptions import AccessDeniedError


@dataclass
class Question:
    id: UUID
    name: str
    options: list[str]


@dataclass
class Survey:
    id: UUID
    name: str
    author: UUID
    questions: list[UUID]

    def can_delete(self, user_id: str) -> bool:
        if self.author != user_id:
            raise AccessDeniedError("Cannot delete the survey")
        return True
