from typing import Protocol
from abc import abstractmethod

from quizer.entities.user import User


class UserRepository(Protocol):
    @abstractmethod
    async def add(
        self,
        user: User,
    ) -> str:
        raise NotImplementedError
