import logging
import json
from typing import List, Dict


class JSONFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        return json.dumps({"level": record.levelname, "msg": record.getMessage()})


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
