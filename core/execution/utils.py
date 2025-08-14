from contextlib import contextmanager
from core.data.logger import logger


@contextmanager
def suppress_exc():
    """Suppress and log exceptions during cleanup."""
    try:
        yield
    except Exception:
        logger.exception("rollback failure")
