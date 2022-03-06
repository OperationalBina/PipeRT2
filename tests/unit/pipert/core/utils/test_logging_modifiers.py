import sys
import pytest
import logging
from pipert2.utils.logging_module_modifiers import add_pipe_log_level, \
    PIPE_INFRASTRUCTURE_LOG_LEVEL_NAME, PIPE_INFRASTRUCTURE_LOG_LEVEL


@pytest.fixture()
def pipe_logger():
    add_pipe_log_level()
    logger = logging.getLogger()
    logger.addHandler(logging.StreamHandler(sys.stdout))
    logger.setLevel(logging.WARNING)
    return logger


def test_plog_when_using_his_level_expecting_the_log_showing(caplog, pipe_logger):
    LOGGING_TEXT = "wow Mayo Meleh"
    pipe_logger.setLevel(PIPE_INFRASTRUCTURE_LOG_LEVEL)
    pipe_logger.plog(LOGGING_TEXT)

    assert f"{PIPE_INFRASTRUCTURE_LOG_LEVEL_NAME}" in caplog.text and LOGGING_TEXT in caplog.text


def test_plog_log_when_level_is_higher_expecting_the_log_not_showing(caplog, pipe_logger):
    LOGGING_TEXT = "wow Mayo Meleh"
    pipe_logger.setLevel(logging.WARNING)
    pipe_logger.plog(LOGGING_TEXT)

    assert f"{PIPE_INFRASTRUCTURE_LOG_LEVEL_NAME}" not in caplog.text and LOGGING_TEXT not in caplog.text
