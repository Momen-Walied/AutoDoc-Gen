from __future__ import annotations

import logging
import sys
import typing as Any

import structlog
from structlog.stdlib import BoundLogger

from src.config import get_settings

def _configure_structlog(log_level: str, app_name: str) -> None:
    """Configure structlog processors and stdlib integration.

    In development we render console-friendly logs; in production/staging we
    render JSON. The same processors always run first to keep the log model
    consistent.
    """
    shared_processors: list[Any] = [
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
    ]

    settings = get_settings()
    if settings.app_env == "development":
        renderer: Any = structlog.dev.ConsoleRenderer()
    else:
        renderer = structlog.processors.JSONRenderer()

    structlog.configure(
        processors=[*shared_processors, renderer],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

    # Sync stdlib logging level with structlog so third-party libraries that
    # use the stdlib logger also respect the configured level.
    level = logging.getLevelName(log_level.upper())
    if not isinstance(level, int):
        level = logging.INFO
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=level,
    )

_configure_structlog(
    log_level=get_settings().log_level,
    app_name=get_settings().app_name,
)


def get_logger(name: str, **binds: Any) -> BoundLogger:
    """Return a structured logger bound to the given name and context.

    Args:
        name: The logger name, usually ``__name__``.
        **binds: Additional context fields such as ``task_id`` or
            ``workflow_id`` to attach to every emitted log entry.

    Returns:
        A ``structlog`` bound logger ready for structured logging.
    """
    logger: BoundLogger = structlog.get_logger(name)
    if binds:
        logger = logger.bind(**binds)

    return logger
