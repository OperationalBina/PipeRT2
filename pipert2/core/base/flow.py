from typing import List
from logging import Logger
from pipert2.utils.method_data import Method
from pipert2.core.base.routine import Routine
from pipert2.core.managers.event_board import EventBoard
from pipert2.utils.base_event_executor import BaseEventExecutor
from pipert2.utils.annotations import class_functions_dictionary
from pipert2.utils.interfaces.event_executor_interface import EventExecutorInterface


class Flow(BaseEventExecutor):
    """Flow is an entity designed for running a group of routines in a single process.
    It is also responsible to notify his routines when an event is triggered.

    """

    events = class_functions_dictionary()

    def __init__(self, name: str, event_board: EventBoard, logger: Logger, routines: List[Routine]):
        """
        Args:
            name (str): Name of the flow.
            event_board (EventBoard): The EventBoard of the pipe.
            logger (Logger): Logger object for logging the flow actions.
            routines (Routine): The routines that will be in the flow.

        Attributes:
            routines (dict[str, Routine]): Dictionary mapping the routines to their name.
            name (str): Name of the flow.
            logger (Logger): Logger object for logging the flow actions.
        """

        super().__init__(event_board, logger)
        self.routines = {}
        self.name = name
        self._logger = logger

        flow_events_to_listen = set(self.get_events().keys())

        for routine in routines:
            routine.set_logger(logger=logger.getChild(routine.name))
            routine.flow_name = self.name
            flow_events_to_listen.update(routine.get_events().keys())
            self.routines[routine.name] = routine

        self.events_to_listen.update(flow_events_to_listen)

    def execute_event(self, event: Method) -> None:
        """Execute the event callbacks in the flow and its routines.

        Args:
            event: The event to be executed.

        """

        if event.is_applied_on_flow(self.name):
            if event.is_applied_on_specific_routines(self.name):
                routines = event.specific_flow_routines.get(self.name)
                for routine in routines:
                    if routine in self.routines.keys():
                        self.routines.get(routine).execute_event(event)
            else:
                for routine in self.routines.values():
                    routine.execute_event(event)

            EventExecutorInterface.execute_event(self, event)

    def _after_join(self):
        """Block until the flow process terminates.

        """

        for routine in self.routines.values():
            routine.join()

    @classmethod
    def get_events(cls):
        """Get the events of the flow.

        Returns:
            dict[str, set[Callback]]: The events callbacks mapped by their events.

        """

        return cls.events.all[cls.__name__]
