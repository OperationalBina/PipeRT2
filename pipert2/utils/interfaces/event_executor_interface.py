import time
from abc import ABC, abstractmethod

from pipert2.utils.annotations import class_functions_dictionary

from pipert2.utils.consts import KILL_EVENT_NAME

from pipert2.utils.method_data import Method


class EventExecutorInterface(ABC):  # TODO - Maybe add a logger abstract class for each class with logger.

    @abstractmethod
    def execute_event(self, event: Method) -> None:
        mapped_events = self.get_events()

        if event.event_name in mapped_events:
            self._logger.plog(f"Running event '{event.event_name}'")
            for callback in mapped_events[event.event_name]:
                callback(self, **event.params)

    @classmethod
    @abstractmethod
    def get_events(cls):
        raise NotImplementedError

    def base_listen_to_events(self):
        event = self.event_handler.wait()
        while not event.event_name == KILL_EVENT_NAME:
            self.execute_event(event)
            event = self.event_handler.wait()

        self.execute_event(Method(KILL_EVENT_NAME))

        print("base listing finishs")
