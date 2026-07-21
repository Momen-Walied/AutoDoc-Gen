from __future__ import annotations

import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

class TaskSchema(BaseModel):
    """Typed representation of a Task record."""

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    id: str
    repo_url: str
    branch: str = "main"
    status: str = "PENDING"
    target_audience: str | None = None
    model_tier: str | None = None
    cost_usd: float = 0.0
    metadata: dict[str, Any] = Field(
        default_factory=dict,
        alias="metadata_",
    )
    created_at: datetime.datetime | None = None
    updated_at: datetime.datetime | None = None


class ArtifactSchema(BaseModel):
    """Typed representation of an Artifact record."""

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    id: str
    task_id: str
    artifact_type: str
    s3_key: str
    s3_bucket: str
    content_type: str = "text/markdown"
    is_final: bool = False
    metadata: dict[str, Any] = Field(
        default_factory=dict,
        alias="metadata_",
    )
    created_at: datetime.datetime | None = None


class ApprovalSchema(BaseModel):
    """Typed representation of an Approval record."""

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    id: str
    task_id: str
    approved: bool
    feedback: str | None = None
    reviewer_id: str | None = None
    created_at: datetime.datetime | None = None
