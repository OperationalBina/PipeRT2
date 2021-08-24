from abc import ABC, abstractmethod


class DataTransmitter(ABC):

    @abstractmethod
    def transmit(self):
        raise NotImplementedError

    @abstractmethod
    def receive(self):
        raise NotImplementedError
