from abc import ABC, abstractmethod


class PipeLogger(ABC):

    @abstractmethod
    def get_child(self):
        pass

    @abstractmethod
    def info(self, param):
        pass
