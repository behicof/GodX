import logging
from logging import getLogger as get_logger

def test_logging_singleton_identity_and_handler():
    logger1 = get_logger("x")
    logger1.handlers.clear()
    handler = logging.StreamHandler()
    logger1.addHandler(handler)
    logger2 = get_logger("x")
    assert logger1 is logger2
    assert len(logger2.handlers) == 1
