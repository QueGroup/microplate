from typing import Final

import structlog
from structlog import BoundLogger

from .setup import configure_logging

custom_logger: Final[BoundLogger] = structlog.stdlib.get_logger("custom_logger")  # type: ignore

__all__ = (
    "custom_logger",
    "configure_logging",
)
