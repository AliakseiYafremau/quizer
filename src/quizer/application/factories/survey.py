from typing import Protocol
from abc import abstractmethod

from uuid import UUID

from quizer.application.interfaces.common.uuid_generator import UUIDGenerator
from quizer.entities.survey import Survey, Answer


class SurveyFactory:
    def __init__(self, uuid_generator: UUIDGenerator):
        self._uuid_generator = uuid_generator

    def create_survey(self, name: str, author: str) -> Survey:
        return Survey(
            id=self._uuid_generator(),
            name=name,
            author=author,
            questions=[],
        )


class AnswerFactory:
    def __init__(self, uuid_generator: UUIDGenerator):
        self._uuid_generator = uuid_generator

    def create_answer(self, user_id: str, question_id: UUID, option: int) -> Answer:
        return Answer(
            id=self._uuid_generator(), user=user_id, question=question_id, option=option
        )
