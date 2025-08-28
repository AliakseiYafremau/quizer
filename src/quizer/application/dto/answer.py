from uuid import UUID
from dataclasses import dataclass


@dataclass
class AnswerDTO:
    survey: UUID
    selections: dict[UUID, int]
