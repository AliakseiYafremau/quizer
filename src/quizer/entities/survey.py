from uuid import UUID
from dataclasses import dataclass

from quizer.entities.exceptions import AccessDeniedError, DuplicateNameError


@dataclass
class Answer:
    """Answer entity

    Each answer has a unique id and belongs to a specific survey. An answer is associated with a user who provided it.

    Example:
        User(id='user_1'),
        Survey(
            id=SURVEY_ID
        ),
        Question(
            id=FIRST_QUESTION_ID,
            survey=SURVEY_ID,
            options=['option_1', 'option_2']
        ),
        Question(
            id=SECOND_QUESTION_ID,
            survey=SURVEY_ID,
            options=['option_3', 'option_4']
        ),

        Answer(
            ...
            user='user_1',
            selecitons=(
                (FIRST_QUESTION_ID, 0),  # user_1 selects 'option_1'
                (SECOND_QUESTION_ID, 1),  # user_1 selects 'option_4'
            )
    """
    id: UUID
    user: str
    survey: UUID
    selections: tuple[tuple[UUID, int], ...]  # (Question, Option)


@dataclass
class Question:
    """Question entity
    
    Each question has a unique id, a name. A question belongs to a survey and can have multiple options of answer."""
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
    """Survey entity
    
    Each survey has a unique id, a name. An author is the user who created the survey.
    A survey contains multiple questions. A survey can be marked as available only if
    all its questions have unique names and all questions are prepared."""
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
