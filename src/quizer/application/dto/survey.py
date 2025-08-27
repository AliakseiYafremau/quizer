from uuid import UUID
from dataclasses import dataclass


@dataclass
class ReadSurveyDTO:
    id: UUID
    name: str
    author: UUID
