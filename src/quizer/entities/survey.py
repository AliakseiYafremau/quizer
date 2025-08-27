from uuid import UUID
from dataclasses import dataclass

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

    