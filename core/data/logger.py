"""JSON logger configuration for the project.

This module exposes a module-level ``logger`` configured to emit structured
JSON messages containing the log level, message and an ISO 8601 timestamp. Use
it by importing ``logger`` and calling standard logging methods::

    from core.data.logger import logger
    logger.info("trade executed")

The logger writes to standard output via a single ``StreamHandler`` and avoids
adding duplicate handlers on import.
"""

from __future__ import annotations

import json
import logging
from datetime import datetime, timezone


class JSONFormatter(logging.Formatter):
    """Format log records as JSON with level, message and timestamp."""

    def format(self, record: logging.LogRecord) -> str:
        payload = {
            "level": record.levelname,
            "msg": record.getMessage(),
            "time": datetime.fromtimestamp(record.created, tz=timezone.utc).isoformat(),
        }
        return json.dumps(payload)


logger = logging.getLogger("omni")
if not any(isinstance(h, logging.StreamHandler) for h in logger.handlers):
    handler = logging.StreamHandler()
    handler.setFormatter(JSONFormatter())
    logger.addHandler(handler)
logger.setLevel(logging.INFO)

