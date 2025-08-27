from typing import Protocol
from abc import abstractmethod

from quizer.entities.survey import Survey


class SurveyRepository(Protocol):
    @abstractmethod
    async def get_all(
        self,
    ) -> list[Survey]:
        raise NotImplementedError
