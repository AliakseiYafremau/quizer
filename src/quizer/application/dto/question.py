from uuid import UUID
from dataclasses import dataclass


@dataclass
class ReadQuestionDTO:
    id: UUID
    name: str
    options: list[str]
