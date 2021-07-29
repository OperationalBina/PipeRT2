from abc import ABC, abstractmethod
from src.pipert2.utils.method_data import Method


class EventExecutorInterface(ABC):

    @abstractmethod
    def execute_event(self, event: Method) -> None:
        mapped_events = self.get_events()

        if event.name in mapped_events:
            self.logger.info(f"Running event '{event.name}'")
            for callback in mapped_events[event.name]:
                callback(self, **event.params)

    @classmethod
    @abstractmethod
    def get_events(cls):
        raise NotImplementedError

