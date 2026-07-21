"""Base adapter contract for external systems."""

from __future__ import annotations

from abc import ABC


class BaseAdapter(ABC):
    """Abstract base class for external system adapters."""

    def __init__(self) -> None:
        """Initialize the adapter."""
        pass
