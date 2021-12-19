import logging
from .socket_handler import SocketHandler
from ..consts.socket_logger import URL, LOG_EVENT_LOG


class SocketLogger(logging.Logger):
    def __init__(self, name):
        logging.Logger.__init__(self, name)

        self._url = URL
        self._log_event_name = LOG_EVENT_LOG

    def getChild(self, suffix: str):
        child_logger = super(SocketLogger, self).getChild(suffix)

        child_logger.url = self._url
        child_logger.propagate = False
        child_logger.setLevel(self.level)
        handler = SocketHandler(self._url, self._log_event_name)

        handler.setFormatter(logging.Formatter("{'time': %(asctime)s.%(msecs)03d, "
                                               "'source': %(name)s, "
                                               "'level': %(levelname)s, "
                                               "'message': %(message)s}",
                                               datefmt="%d-%m-%y %H:%M:%S"))
        child_logger.addHandler(handler)

        return child_logger
