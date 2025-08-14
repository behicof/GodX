import json
import logging
from datetime import datetime, timezone
from typing import Dict


class JsonFormatter(logging.Formatter):
    """Format logs as JSON with ISO-8601 timestamps."""

    def format(self, record: logging.LogRecord) -> str:
        payload = {
            "ts": datetime.fromtimestamp(record.created, tz=timezone.utc).isoformat(),
            "level": record.levelname,
            "name": record.name,
            "msg": record.getMessage(),
        }
        return json.dumps(payload)


_loggers: Dict[str, logging.Logger] = {}


def get_logger(name: str) -> logging.Logger:
    """Return a configured logger.

    Removes any existing handlers, attaches a single ``StreamHandler`` with
    ``JsonFormatter``, disables propagation and caches the logger instance.
    """
    if name in _loggers:
        return _loggers[name]

    logger = logging.getLogger(name)
    logger.handlers = []
    handler = logging.StreamHandler()
    handler.setFormatter(JsonFormatter())
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    logger.propagate = False
    _loggers[name] = logger
    return logger
