import logging
import json

class JSONFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        return json.dumps({"level": record.levelname, "msg": record.getMessage()})

handler = logging.StreamHandler()
handler.setFormatter(JSONFormatter())
logger = logging.getLogger("omni")
logger.addHandler(handler)
logger.setLevel(logging.INFO)
