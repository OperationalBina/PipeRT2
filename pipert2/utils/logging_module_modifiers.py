import os
import sys
import logging
from dotenv import load_dotenv

from pipert2.utils.consts.socket_names import LOG_NAME
from pipert2.utils.socketio_logger.socket_logger import SocketLogger
from pipert2.utils.socketio_logger.socket_handler import SocketHandler


PIPE_INFRASTRUCTURE_LOG_LEVEL = 5
PIPE_INFRASTRUCTURE_LOG_LEVEL_NAME = "PIPE_INFRASTRUCTURE"


load_dotenv()


def add_pipe_log_level():
    """Add a new log level to the logging module named PIPE_INFRASTRUCTURE.
    You can use this level by using the plog method in the Logger.
    The level of PIPE_INFRASTRUCTURE is smaller than DEBUG level (10).


    Example usage:
        >>> import sys
        >>> add_pipe_log_level()
        >>> logger = logging.getLogger()
        >>> logger.addHandler(logging.StreamHandler(sys.stdout))
        >>> logger.setLevel(PIPE_INFRASTRUCTURE_LOG_LEVEL)
        >>> logger.plog("wow")

    """

    logging.addLevelName(PIPE_INFRASTRUCTURE_LOG_LEVEL, PIPE_INFRASTRUCTURE_LOG_LEVEL_NAME)

    def plog(self, message, *args, **kws):
        if self.isEnabledFor(PIPE_INFRASTRUCTURE_LOG_LEVEL):
            self._log(PIPE_INFRASTRUCTURE_LOG_LEVEL, message, args, **kws)

    logging.Logger.plog = plog


def get_default_print_logger(logger_name):
    logger = logging.getLogger(logger_name)
    console_handler = (logging.StreamHandler(sys.stdout))
    console_handler.setFormatter(logging.Formatter("%(asctime)s — %(name)s — %(levelname)s — %(message)s",
                                                   datefmt="%d-%m-%y %H:%M:%S"))
    logger.addHandler(console_handler)
    logger.setLevel(logging.INFO)
    return logger


def get_socket_logger(logger_name, level):
    logging.setLoggerClass(SocketLogger)

    logger: SocketLogger = logging.getLogger(logger_name)

    logger.set_url(os.getenv("SOCKET_LOGGER_URL"))
    logger.set_log_event_name(LOG_NAME)
    logger.propagate = False
    logger.setLevel(level)

    handler = SocketHandler(logger._url, logger._log_event_name)
    handler.setFormatter(logging.Formatter('{"time": "%(asctime)s.%(msecs)03d", '
                                            '"source": "%(name)s", '
                                            '"level": "%(levelname)s", '
                                            '"message": "%(message)s"}',
                                            datefmt="%d-%m-%y %H:%M:%S"))
    logger.addHandler(handler)

    return logger
