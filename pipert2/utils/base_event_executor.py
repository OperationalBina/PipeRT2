from logging import Logger
from multiprocessing import Process
from pipert2.utils.method_data import Method
from pipert2.utils.dummy_object import Dummy
from pipert2.utils.interfaces import EventExecutorInterface
from pipert2.utils.consts import KILL_EVENT_NAME, STOP_EVENT_NAME
from pipert2.utils.annotations import class_functions_dictionary
from pipert2.core.managers.event_board import EventBoard, EventHandler


class BaseEventExecutor(EventExecutorInterface):
    """BaseEventExecutor is an base implementation for event loop listener.

    """

    events = class_functions_dictionary()

    def __init__(self, event_board: EventBoard, logger: Logger):
        """
        Args:
            event_board (EventBoard): The EventBoard of the pipe.
            logger (Logger): Logger object for logging the flow actions.

        Attributes:
            logger (Logger): Logger object for logging the flow actions.
            event_handler (EventHandler): EventHandler object for communicating with the
                event system of the pipe.

        """

        self.routines = {}
        self._logger = logger
        self.event_loop_process = Dummy()

        self.events_to_listen = set(self.get_events().keys())
        self.event_board = event_board

        self.event_handler: EventHandler = Dummy()

    def build(self) -> None:
        """Start the event loop process.

        """

        self.before_build()

        self.event_handler = self.event_board.get_event_handler(self.events_to_listen)

        self.event_loop_process = Process(target=self.run)
        self.event_loop_process.start()

    def before_build(self) -> None:
        """The implementation can implement this method and called in build.

        """

        pass

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

    def join(self) -> None:
        """Block until the event loop process terminates

        """

        self.event_loop_process.terminate()

    @classmethod
    def get_events(cls):
        """Get the events of the flow.

        Returns:
            dict[str, set[Callback]]: The events callbacks mapped by their events.

        """

        return cls.events.all[cls.__name__]

