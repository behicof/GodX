import logging
import json


class JSONFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        return json.dumps({"level": record.levelname, "msg": record.getMessage()})


_LOGGER: logging.Logger | None = None


def get_logger() -> logging.Logger:
    """Return module-level logger configured once."""

    global _LOGGER
    if _LOGGER is None:
        logger = logging.getLogger("omni")
        if not logger.handlers:
            handler = logging.StreamHandler()
            handler.setFormatter(JSONFormatter())
            logger.addHandler(handler)
        logger.setLevel(logging.INFO)
        _LOGGER = logger
    return _LOGGER


# Backwards-compatible logger object
logger = get_logger()
