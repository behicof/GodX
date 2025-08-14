from core.data.logger import get_logger
from core.data.logger import get_logger as get_logger_again


def test_get_logger_singleton():
    logger1 = get_logger()
    logger2 = get_logger_again()
    assert logger1 is logger2
    assert len(logger1.handlers) == 1
