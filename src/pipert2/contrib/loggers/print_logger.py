import logging
import sys

from src.pipert2.core.base.logger import PipeLogger


class PrintLogger(PipeLogger):
    """Logger class for printing logs on the console.

    """

    def __init__(self, name: str, level=logging.DEBUG):
        super().__init__(name)
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(logging.Formatter("%(asctime)s — %(name)s — %(levelname)s — %(message)s",
                                                       datefmt="%d-%m-%y %H:%M:%S"))
        self.logger.addHandler(console_handler)
        self.logger.propagate = False

    def info(self, message: str):
        self.logger.info(message)

    def error(self, message: str):
        self.logger.error(message)

    def debug(self, message: str):
        self.logger.debug(message)

    def warning(self, message: str):
        self.logger.warning(message)

    def exception(self, message: str):
        self.logger.exception(message)

    def get_logger_child(self, child_name: str) -> 'PipeLogger':
        self.logger.getChild(child_name)

