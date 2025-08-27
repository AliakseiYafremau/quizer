from typing import Protocol
from abc import abstractmethod

from quizer.entities.survey import Survey


class SurveyFactory(Protocol):
    @abstractmethod
    def create_survey(self, name: str, author: str) -> Survey:
        raise NotImplementedError
