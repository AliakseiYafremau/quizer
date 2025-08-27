from typing import Protocol
from abc import abstractmethod

from uuid import UUID


class UUIDGenerator(Protocol):
    @abstractmethod
    def __call__(self) -> UUID:
        raise NotImplementedError
