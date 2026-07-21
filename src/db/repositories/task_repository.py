
from __future__ import annotations

from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models import Task
from src.db.repositories.base import BaseRepository
from src.db.schemas import TaskSchema


class TaskRepository(BaseRepository[TaskSchema]):

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)

    async def create(self, task: TaskSchema) -> TaskSchema:

        orm_task = Task(
            id = task.id,
            repo_url = task.repo_url,
            branch=task.branch,
            status=task.status,
            target_audience=task.target_audience,
            model_tier=task.model_tier,
            cost_usd=task.cost_usd,
            metadata_=task.metadata,

        )

        self._session.add(orm_task)

        await self._session.flush()  # Ensure the task is persisted to the database
        await self._session.refresh(orm_task)  # Refresh the ORM object to get updated fields
        return TaskSchema.model_validate(orm_task)
    
    async def get(self, task_id: str) -> TaskSchema | None:

        result = await self._session.execute(select(Task).where(Task.id == task_id))
        orm_task = result.scalar_one_or_none()
        if orm_task is None:
            return None
        return TaskSchema.model_validate(orm_task)
    
    async def update_status(
        self,
        task_id: str,
        status: str,
        metadata_updates: dict[str, Any] | None = None,
    ) -> TaskSchema | None:
        
        task = await self.get(task_id)
        if task is None:
            return None
        
        orm_task = await self._session.get(Task, task_id)
        if orm_task is None:
            return None
        
        orm_task.status = status
        if metadata_updates:
            orm_task.metadata_.update(metadata_updates)
        
        await self._session.flush()
        await self._session.refresh(orm_task)
        return TaskSchema.model_validate(orm_task)

    async def update_cost(self, task_id: str, cost_usd: float) -> TaskSchema | None:

        
        orm_task = await self._session.get(Task, task_id)
        if orm_task is None:
            return None
        
        orm_task.cost_usd = cost_usd
        
        await self._session.flush()
        await self._session.refresh(orm_task)
        return TaskSchema.model_validate(orm_task)
