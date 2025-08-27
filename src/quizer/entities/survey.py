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
    author: str
    questions: list[UUID]

    def can_manage(self, user_id: str) -> bool:
        if self.author != user_id:
            raise AccessDeniedError("Cannot delete the survey")
        return True

    def update_name(self, name: str):
        if not isinstance(name, str):
            raise ValueError("Name must be string")
        self.name = name
