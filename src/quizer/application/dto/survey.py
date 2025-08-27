from uuid import UUID
from dataclasses import dataclass


@dataclass
class ReadSurveyDTO:
    id: UUID
    name: str
    author: str


@dataclass
class UpdateSurveyDTO:
    id: UUID
    new_name: str
