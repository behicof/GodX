import json
import logging
from datetime import datetime, timezone


class JsonFormatter(logging.Formatter):
    """Emit logs in JSON with ISO-8601 timestamp."""

    def format(self, record: logging.LogRecord) -> str:
        log_record = {
            "ts": datetime.fromtimestamp(record.created, tz=timezone.utc).isoformat(),
            "level": record.levelname,
            "msg": record.getMessage(),
        }
        return json.dumps(log_record)


_loggers: dict[str, logging.Logger] = {}


def get_logger(name: str) -> logging.Logger:
    """Return a cached logger emitting structured JSON."""
    logger = _loggers.get(name)
    if logger is not None:
        return logger

    logger = logging.getLogger(name)
    logger.handlers.clear()
    handler = logging.StreamHandler()
    handler.setFormatter(JsonFormatter())
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    logger.propagate = False

    _loggers[name] = logger
    return logger
