import multiprocessing as mp
import queue
import time
from statistics import median
from typing import Dict

from pipert2.utils.consts import KILL_EVENT_NAME, START_ROUTINE_LOGIC_NAME, FINISH_ROUTINE_LOGIC_NAME

from pipert2.utils.annotations import class_functions_dictionary
from pipert2.utils.interfaces import EventExecutorInterface
from pipert2.utils.method_data import Method


class RoutineFPSListener(EventExecutorInterface):

    events = class_functions_dictionary()

    def __init__(self, event_board):
        self.event_listening_process: mp.Process = mp.Process(target=self.listen_events)

        events_to_listen = set(self.get_events().keys())
        # self.event_handler = event_board.get_event_handler(events_to_listen)

        self.latest_routines_start_time: Dict[str, float] = {}
        self.routines_measurements: Dict[str, queue.Queue] = {}

    def listen_events(self):
        """The synchronize process, executing the pipe events that occur.

                """

        event = self.event_handler.wait()
        while not event.event_name == KILL_EVENT_NAME:
            self.execute_event(event)
            event = self.event_handler.wait()

        self.execute_event(Method(KILL_EVENT_NAME))

    def calculate_median_fps(self, routine_name):
        """Get the median fps by routine name.

        Args:
            routine_name: The routine name.

        Returns:
            The median fps for the required fps.
        """

        routine_queue = self.routines_measurements[routine_name]
        routine_measurements_as_list = []

        try:
            for fps in iter(routine_queue.get_nowait, None):
                routine_measurements_as_list.append(fps)
        except queue.Empty:
            return 1 / median(routine_measurements_as_list)

    def execute_event(self, event: Method) -> None:
        """Execute the event that notified.

                Args:
                    event: The event to execute.
                """

        EventExecutorInterface.execute_event(self, event)

    @classmethod
    def get_events(cls):
        """Get the events of the synchronize_routines.

                Returns:
                    dict[str, set[Callback]]: The events callbacks mapped by their events.
                """

        return cls.events.all[cls.__name__]

    @events(START_ROUTINE_LOGIC_NAME)
    def update_start_routine_logic_time(self, **params):
        """Updating the starting routine logic time.

        Args:
            **params: Dictionary contained the routine name.
        """

        routine_name = params["routine_name"]
        self.latest_routines_start_time[routine_name] = time.time()

    @events(FINISH_ROUTINE_LOGIC_NAME)
    def update_finish_routine_logic_time(self, **params):
        """Updating the duration of routine.

        Args:
            **params: Dictionary contained the routine name.
        """

        routine_name = params["routine_name"]
        routine_start_time = self.latest_routines_start_time[routine_name]
        duration = time.time() - routine_start_time

        if routine_name not in self.routines_measurements:
            self.routines_measurements[routine_name] = mp.Queue(100)

        self.routines_measurements[routine_name].put(duration)
