from abc import ABC, abstractmethod


class RoutineRunner(ABC):
    @abstractmethod
    def create_runner(self, callable):
        pass

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def join(self):
        pass
