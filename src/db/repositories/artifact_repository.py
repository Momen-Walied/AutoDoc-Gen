"""Artifact repository implementation."""

from __future__ import annotations

from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models import Artifact
from src.db.repositories.base import BaseRepository
from src.db.schemas import ArtifactSchema


class ArtifactRepository(BaseRepository[ArtifactSchema]):
    """Repository for artifact metadata persistence."""

    def __init__(self, session: AsyncSession) -> None:
        """Initialize the repository with a database session."""
        super().__init__(session)

    async def create(self, artifact: ArtifactSchema) -> ArtifactSchema:
        """Persist artifact metadata.

        Args:
            artifact: Artifact metadata to persist.

        Returns:
            The persisted artifact metadata as a typed schema.
        """
        orm_artifact = Artifact(
            id=artifact.id,
            task_id=artifact.task_id,
            artifact_type=artifact.artifact_type,
            s3_key=artifact.s3_key,
            s3_bucket=artifact.s3_bucket,
            content_type=artifact.content_type,
            is_final=artifact.is_final,
            metadata_=artifact.metadata,
        )
        self._session.add(orm_artifact)
        await self._session.flush()
        await self._session.refresh(orm_artifact)
        return ArtifactSchema.model_validate(orm_artifact)

    async def get(self, artifact_id: str) -> ArtifactSchema | None:
        """Retrieve an artifact by ID.

        Args:
            artifact_id: Unique artifact identifier.

        Returns:
            The artifact metadata if found, otherwise ``None``.
        """
        result = await self._session.execute(select(Artifact).where(Artifact.id == artifact_id))
        orm_artifact = result.scalar_one_or_none()
        if orm_artifact is None:
            return None
        return ArtifactSchema.model_validate(orm_artifact)

    async def list_by_task(self, task_id: str) -> list[ArtifactSchema]:
        """List all artifacts for a given task.

        Args:
            task_id: Unique task identifier.

        Returns:
            A list of artifact metadata records.
        """
        result = await self._session.execute(
            select(Artifact).where(Artifact.task_id == task_id),
        )
        return [ArtifactSchema.model_validate(a) for a in result.scalars().all()]

    async def mark_final(
        self,
        artifact_id: str,
        metadata_updates: dict[str, Any] | None = None,
    ) -> ArtifactSchema | None:
        """Mark an artifact as final and optionally update metadata.

        Args:
            artifact_id: Unique artifact identifier.
            metadata_updates: Optional metadata fields to merge.

        Returns:
            The updated artifact metadata if found, otherwise ``None``.
        """
        orm_artifact = await self._session.get(Artifact, artifact_id)
        if orm_artifact is None:
            return None

        orm_artifact.is_final = True
        if metadata_updates:
            orm_artifact.metadata_.update(metadata_updates)

        await self._session.flush()
        await self._session.refresh(orm_artifact)
        return ArtifactSchema.model_validate(orm_artifact)
