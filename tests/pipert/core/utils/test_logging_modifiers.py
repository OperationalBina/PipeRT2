import sys
import logging
from src.pipert2.utils.logging_module_modifiers import add_pipe_log_level, \
    PIPE_INFRASTRUCTURE_LOG_LEVEL_NAME, PIPE_INFRASTRUCTURE_LOG_LEVEL


def test_plog_works_when_using_his_level(caplog):
    LOGGING_TEXT = "wow Mayo Meleh"
    add_pipe_log_level()
    logger = logging.getLogger()
    logger.addHandler(logging.StreamHandler(sys.stdout))
    logger.setLevel(PIPE_INFRASTRUCTURE_LOG_LEVEL)
    logger.plog(LOGGING_TEXT)

    assert f"{PIPE_INFRASTRUCTURE_LOG_LEVEL_NAME}" in caplog.text and LOGGING_TEXT in caplog.text


def test_plog_works_when_not_using_his_level(caplog):
    LOGGING_TEXT = "wow Mayo Meleh"
    add_pipe_log_level()
    logger = logging.getLogger()
    logger.addHandler(logging.StreamHandler(sys.stdout))
    logger.plog(LOGGING_TEXT)

    assert f"{PIPE_INFRASTRUCTURE_LOG_LEVEL_NAME}" not in caplog.text and LOGGING_TEXT not in caplog.text