from abc import ABC, abstractmethod


class PipeLogger(ABC):

    @abstractmethod
    def exception(self, param):
        pass

    @abstractmethod
    def info(self, param):
        pass

    @abstractmethod
    def get_child(self):
        pass
