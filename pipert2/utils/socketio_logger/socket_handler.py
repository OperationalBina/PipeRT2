import logging
import socketio
from socketio.exceptions import SocketIOError


class SocketHandler(logging.Handler):
    def __init__(self, url, log_event_name):
        super().__init__()

        self.sio = socketio.Client()
        self.url = url
        self.log_event_name = log_event_name

    def emit(self, record: logging.LogRecord) -> None:
        if not self.sio.connected:
            self.sio.connect(self.url)
        try:
            self.sio.emit(self.log_event_name, self.formatter.format(record))
        except SocketIOError:
            pass

    def close(self) -> None:
        self.sio.disconnect()
