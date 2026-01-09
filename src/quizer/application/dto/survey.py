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
    new_name: str | None = None


@dataclass
class SurveyReportDTO:
    name: str
    author: str
    survey: UUID
    selections: tuple[
        tuple[str, tuple[tuple[UUID, int], ...]], ...
    ]  # User: [Question: Answer]
