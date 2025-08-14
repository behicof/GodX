from libs.logging_utils import get_logger

logger = get_logger("omni")


def write_event(event: str) -> None:
    """Write a structured event using the shared logger."""
    logger.info(event)
