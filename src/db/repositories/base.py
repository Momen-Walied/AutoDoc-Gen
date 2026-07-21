"""Base repository contract and shared utilities."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TypeVar

from sqlalchemy.ext.asyncio import AsyncSession

T = TypeVar("T")

class BaseRepository[T](ABC):

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    @property
    def session(self) -> AsyncSession:
        """Return the current async database session."""
        return self._session
    
    @abstractmethod
    async def create(self, entity: T) -> T:
        """Persist a new entity and return it."""
        ...
