from typing import Protocol
from abc import abstractmethod

from uuid import UUID

from quizer.entities.survey import Survey


class SurveyRepository(Protocol):
    @abstractmethod
    async def get_by_id(
        self,
        id: UUID,
    ) -> Survey | None:
        raise NotImplementedError

    @abstractmethod
    async def get_all(
        self,
    ) -> list[Survey]:
        raise NotImplementedError

    @abstractmethod
    async def add(
        self,
        survey: Survey,
    ) -> UUID:
        raise NotImplementedError

    @abstractmethod
    async def update(
        self,
        survey: Survey,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def delete(
        self,
        id: UUID,
    ) -> None:
        raise NotImplementedError
