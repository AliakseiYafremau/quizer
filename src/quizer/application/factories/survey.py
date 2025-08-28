from typing import Protocol
from abc import abstractmethod

from quizer.application.interfaces.common.uuid_generator import UUIDGenerator
from quizer.entities.survey import Survey


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
