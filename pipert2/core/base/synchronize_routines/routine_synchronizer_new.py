from logging import Logger
from multiprocessing import Process
from pipert2.utils.consts import KILL_EVENT_NAME, STOP_EVENT_NAME, START_EVENT_NAME
from pipert2.utils.method_data import Method
from pipert2.utils.dummy_object import Dummy
from pipert2.core.managers.event_board import EventBoard, EventHandler
from pipert2.utils.annotations import class_functions_dictionary
from pipert2.utils.interfaces import EventExecutorInterface


class EventExecutorImplementation(EventExecutorInterface):
    """Flow is an entity designed for running a group of routines in a single process.
    It is also responsible to notify his routines when an event is triggered.

    """

    events = class_functions_dictionary()

    def __init__(self, event_board: EventBoard, logger: Logger):
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
            event_handler (EventHandler): EventHandler object for communicating with the
                event system of the pipe.

        """

        self.routines = {}
        self._logger = logger
        self.synchronizer_process = Dummy()

        events_to_listen = set(self.get_events().keys())
        self.event_handler: EventHandler = event_board.get_event_handler(events_to_listen)

    def base_build(self) -> None:
        """Start the flow process.

        """

        self.synchronizer_process = Process(target=self.run)
        self.synchronizer_process.start()

    def run(self) -> None:
        """The flow process, executing the pipe events that occur.

        """

        event: Method = self.event_handler.wait()

        while event.event_name != KILL_EVENT_NAME:
            self.execute_event(event)
            event = self.event_handler.wait()

        self.execute_event(Method(STOP_EVENT_NAME))

    def execute_event(self, event: Method) -> None:
        """Execute the event callbacks in the flow and its routines.

        Args:
            event: The event to be executed.

        """

        EventExecutorInterface.execute_event(self, event)

    def base_join(self) -> None:
        """Block until the flow process terminates

        """

        self.synchronizer_process.join()

    @classmethod
    def get_events(cls):
        """Get the events of the flow.

        Returns:
            dict[str, set[Callback]]: The events callbacks mapped by their events.

        """

        return cls.events.all[cls.__name__]

