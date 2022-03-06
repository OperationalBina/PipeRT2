from abc import ABC, abstractmethod
from pipert2.utils.method_data import Method


class EventExecutorInterface(ABC):  # TODO - Maybe add a logger abstract class for each class with logger.

    @abstractmethod
    def execute_event(self, event: Method) -> None:
        mapped_events = self.get_events()

        if event.event_name in mapped_events:
            for callback in mapped_events[event.event_name]:
                callback(self, **event.params)

    @classmethod
    @abstractmethod
    def get_events(cls):
        raise NotImplementedError
