
from __future__ import annotations

import datetime
from typing import Any

from sqlalchemy import JSON, DateTime, String, Text

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

def _utc_now() -> datetime.datetime:
    """Return the current UTC time."""
    return datetime.datetime.now(datetime.UTC)

class Base(DeclarativeBase):
    pass

class Task(Base):

    __tablename__ = "tasks"

    id : Mapped[int] = mapped_column(String(64), primary_key=True)
    repo_url : Mapped[str] = mapped_column(String(512), nullable=False)
    branch: Mapped[str] = mapped_column(String(255), default="main")
    status: Mapped[str] = mapped_column(String(64), default="PENDING")
    target_audience: Mapped[str | None] = mapped_column(String(255), nullable=True)
    model_tier: Mapped[str | None] = mapped_column(String(64), nullable=True)
    cost_usd: Mapped[float] = mapped_column(default=0.0)
    metadata_: Mapped[dict[str, Any]] = mapped_column(
        "metadata",
        JSON,
        default={},
        nullable=False,
    )
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        default=_utc_now,
        nullable=False,
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        default=_utc_now,
        onupdate=_utc_now,
        nullable=False,
    )

class Artifact(Base):
    """Generated artifact metadata model.

    Artifact content is stored in S3; this table only keeps metadata and S3
    object keys.
    """

    __tablename__ = "artifacts"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    task_id: Mapped[str] = mapped_column(String(64), nullable=False)
    artifact_type: Mapped[str] = mapped_column(String(64), nullable=False)
    s3_key: Mapped[str] = mapped_column(String(512), nullable=False)
    s3_bucket: Mapped[str] = mapped_column(String(255), nullable=False)
    content_type: Mapped[str] = mapped_column(String(128), default="text/markdown")
    is_final: Mapped[bool] = mapped_column(default=False)
    metadata_: Mapped[dict[str, Any]] = mapped_column(
        "metadata",
        JSON,
        default={},
        nullable=False,
    )
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        default=_utc_now,
        nullable=False,
    )

class Approval(Base):
    """Human-in-the-Loop approval record model."""

    __tablename__ = "approvals"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    task_id: Mapped[str] = mapped_column(String(64), nullable=False, unique=True)
    approved: Mapped[bool] = mapped_column(nullable=False)
    feedback: Mapped[str | None] = mapped_column(Text, nullable=True)
    reviewer_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        default=_utc_now,
        nullable=False,
    )
