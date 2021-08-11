from abc import ABC, abstractmethod


class PipeLogger(ABC):

    @abstractmethod
    def info(self, message):
        raise NotImplementedError

    @abstractmethod
    def error(self, message):
        raise NotImplementedError

    @abstractmethod
    def debug(self, message):
        raise NotImplementedError

    @abstractmethod
    def warning(self, message):
        raise NotImplementedError

    @abstractmethod
    def exception(self, message):
        raise NotImplementedError

    @abstractmethod
    def get_logger_child(self, child_name):
        raise NotImplementedError
