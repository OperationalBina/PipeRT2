from logging import Logger
from multiprocessing import Process
from pipert2.utils.method_data import Method
from pipert2.utils.dummy_object import Dummy
from pipert2.utils.interfaces import EventExecutorInterface
from pipert2.utils.annotations import class_functions_dictionary
from pipert2.utils.consts import KILL_EVENT_NAME, STOP_EVENT_NAME
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

        """

        self._logger = logger
        self.event_loop_process: Process = Dummy()

        self.events_to_listen = set(self.get_events().keys())
        self.event_board = event_board

        self.event_handler: EventHandler = Dummy()

    def build(self) -> None:
        """Start the event loop process.

        """

        self._before_build()

        self.event_handler = self.event_board.get_event_handler(self.events_to_listen)

        self.event_loop_process = Process(target=self.run)
        self.event_loop_process.start()

    def run(self) -> None:
        """The event loop process, executing the pipe events that occur.

        """

        event: Method = self.event_handler.wait()

        while event.event_name != KILL_EVENT_NAME:
            self.execute_event(event)
            event = self.event_handler.wait()

        self.execute_event(Method(STOP_EVENT_NAME))

    def execute_event(self, event: Method) -> None:
        """Execute the event callbacks.

        Args:
            event: The event to be executed.

        """

        EventExecutorInterface.execute_event(self, event)

    def join(self) -> None:
        """Block until the event loop process terminates

        """

        if self.event_loop_process.is_alive():
            self.event_loop_process.join()

        self._after_join()

    @classmethod
    def get_events(cls):
        """Get the events of the implement.

        Returns:
            dict[str, set[Callback]]: The events callbacks mapped by their events.

        """

        return cls.events.all[cls.__name__]

    def _before_build(self) -> None:
        """The implementation can implement this method and called in build.

        """

        pass

    def _after_join(self):
        """The implementation can implement this method and called in build.

        """

        pass
