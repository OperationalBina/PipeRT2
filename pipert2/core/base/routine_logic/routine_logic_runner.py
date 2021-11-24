from abc import ABC, abstractmethod


class RoutineLogicRunner(ABC):
    @abstractmethod
    def start(self):
        """Start the runner.

        """

        pass

    @abstractmethod
    def join(self):
        """Join the runner.

        """

        pass
