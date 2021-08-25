from abc import ABC, abstractmethod


class DataTransmitter(ABC):

    @abstractmethod
    def transmit(self):
        def func(data: dict):
            raise NotImplementedError

        return func

    @abstractmethod
    def receive(self):
        def func(data: dict):
            raise NotImplementedError

        return func
