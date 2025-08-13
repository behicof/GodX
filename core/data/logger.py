"""Structured logging utilities with a structlog fallback."""

from typing import Dict, List
import logging
import json

try:  # pragma: no cover - structlog is optional in tests
    import structlog

    structlog.configure(
        processors=[
            structlog.processors.add_log_level,
            structlog.processors.JSONRenderer(),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
    )
    logger = structlog.get_logger("omni")
except Exception:  # noqa: BLE001
    class JSONFormatter(logging.Formatter):
        def format(self, record: logging.LogRecord) -> str:  # noqa: D401
            """Render log records as compact JSON."""

            return json.dumps(
                {"level": record.levelname, "msg": record.getMessage()}
            )

    handler = logging.StreamHandler()
    handler.setFormatter(JSONFormatter())
    logger = logging.getLogger("omni")
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)


def run_logger(symbols: List[str], exchanges_cfg: Dict[str, dict]) -> None:
    """Dummy logger runner that logs start events for symbols."""
    for sym in symbols:
        logger.info(f"logging {sym} with exchanges={list(exchanges_cfg.keys())}")


if __name__ == "__main__":
    run_logger([], {})
