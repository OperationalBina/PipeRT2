import logging
from pipert2.utils.socketio_logger.socket_handler import SocketHandler


class SocketLogger(logging.Logger):
    def __init__(self, name):
        logging.Logger.__init__(self, name)

        self._log_event_name = None
        self._url = None

    def set_url(self, url):
        self._url = url

    def set_log_event_name(self, log_event_name):
        self._log_event_name = log_event_name

    def getChild(self, suffix: str):
        child_logger = super(SocketLogger, self).getChild(suffix)

        child_logger.set_url(self._url)
        child_logger.set_log_event_name(self._log_event_name)
        child_logger.propagate = False
        child_logger.setLevel(self.level)
        handler = SocketHandler(self._url, self._log_event_name)

        handler.setFormatter(logging.Formatter('{"time": "%(asctime)s.%(msecs)03d", '
                                               '"source": "%(name)s", '
                                               '"level": "%(levelname)s", '
                                               '"message": "%(message)s"}',
                                               datefmt="%d-%m-%y %H:%M:%S"))
        child_logger.addHandler(handler)

        return child_logger
