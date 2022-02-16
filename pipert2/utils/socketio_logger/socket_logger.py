try:
    from pipert2.utils.socketio_logger.socket_handler import SocketHandler
except ImportError:
    SocketHandler = None

if SocketHandler:
    import os
    import logging
    from pipert2.utils.consts.emit_socket_names import LOG_NAME
    from pipert2.utils.socketio_logger.frame_utils import numpy_frame_to_base64
    from pipert2.utils.socketio_logger.socket_formatter import SocketFormatter


    class SocketLogger(logging.Logger):
        def __init__(self, name):
            logging.Logger.__init__(self, name)

            self._log_event_name = None
            self._url = None

        def log_frame(self, input_output_type, message):
            self.info(f"{input_output_type}: ", data={
                'image_base64': numpy_frame_to_base64(message.payload.data.get_frame())
            })

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

            handler.setFormatter(SocketFormatter('{"time": "%(asctime)s.%(msecs)03d", '
                                                 '"source": "%(name)s", '
                                                 '"level": "%(levelname)s", '
                                                 '"message": "%(message)s"}',
                                                 datefmt="%d-%m-%y %H:%M:%S"))
            child_logger.addHandler(handler)

            return child_logger

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