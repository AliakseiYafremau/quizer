from uuid import UUID
from dataclasses import dataclass

from quizer.entities.exceptions import AccessDeniedError, DuplicateNameError


@dataclass
class Answer:
    id: UUID
    user: str
    survey: UUID
    selections: tuple[tuple[UUID, int], ...]  # (Question, Option)


@dataclass
class Question:
    id: UUID
    name: str
    survey: UUID
    options: list[str]

    def __post_init__(self):
        for option in self.options:
            if self.options.count(option) > 1:
                raise DuplicateNameError

    def add_option(self, option: str):
        if option in self.options:
            raise DuplicateNameError
        self.options.append(option)


@dataclass
class Survey:
    id: UUID
    name: str
    author: str
    questions: list[UUID]
    is_available: bool

    def make_available(self):
        for question in self.questions:
            if self.questions.count(question) > 1:
                raise DuplicateNameError
        self.is_available = True

    def can_manage(self, user_id: str) -> bool:
        if self.author != user_id:
            raise AccessDeniedError("Cannot delete the survey")
        return True

    def update_name(self, name: str):
        if not isinstance(name, str):
            raise ValueError("Name must be string")
        self.name = name
