try:
    import socketio
    from socketio.exceptions import SocketIOError
except ImportError:
    print(
        "Seems like socketio isn't installed...\nIn order to use the cockpit and its features run pip install PipeRT["
        "cockpit]")
    socketio = None

if socketio:
    import logging


    class SocketHandler(logging.Handler):
        def __init__(self, url, log_event_name):
            super().__init__()

            self.sio = socketio.Client()
            self.url = url
            self.log_event_name = log_event_name

        def emit(self, record: logging.LogRecord) -> None:
            if not self.sio.connected:
                try:
                    self.sio.connect(self.url)
                except socketio.exceptions.ConnectionError:
                    return
            try:
                self.sio.emit(self.log_event_name, self.formatter.format(record))
            except SocketIOError:
                pass

        def close(self) -> None:
            self.sio.disconnect()
