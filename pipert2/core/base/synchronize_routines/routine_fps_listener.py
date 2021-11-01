import time
from logging import Logger
from typing import Dict
import multiprocessing as mp
from statistics import median
from pipert2.utils.method_data import Method
from pipert2.utils.annotations import class_functions_dictionary
from pipert2.utils.interfaces import EventExecutorInterface
from pipert2.utils.consts import KILL_EVENT_NAME, START_ROUTINE_LOGIC_NAME, FINISH_ROUTINE_LOGIC_NAME


class RoutineFpsListener(EventExecutorInterface):

    events = class_functions_dictionary()

    def __init__(self, event_board, logger: Logger, max_queue_size=100):
        self._logger = logger
        self.max_queue_size = max_queue_size

        events_to_listen = set(self.get_events().keys())
        self.event_handler = event_board.get_event_handler(events_to_listen)

        self.mp_manager = mp.Manager()
        self.latest_routines_start_time: Dict[str, float] = self.mp_manager.dict()

        # Use list as a queue, because mp source code has a bug that can't use queue in manager dict.
        self.routines_measurements: Dict[str, list] = self.mp_manager.dict()

    def build(self):
        """Start the event listening.

        """

        mp.Process(target=self.base_listen_to_events).start()

    def calculate_median_fps(self, routine_name):
        """Get the median fps by routine name.

        Args:
            routine_name: The routine name.

        Returns:
            The median fps for the required fps.
        """

        if routine_name in self.routines_measurements:
            routine_fps_list = self.routines_measurements[routine_name]

            if len(routine_fps_list):
                return 1 / median(routine_fps_list)

        return 0

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

        routine_name = params['routine_name']
        self.latest_routines_start_time[routine_name] = params['start_time']

    @events(FINISH_ROUTINE_LOGIC_NAME)
    def update_finish_routine_logic_time(self, **params):
        """Updating the duration of routine.

        Args:
            **params: Dictionary contained the routine name.
        """

        routine_name = params['routine_name']
        routine_start_time = self.latest_routines_start_time[routine_name]
        duration = params['end_time'] - routine_start_time

        if routine_name not in self.routines_measurements:
            self.routines_measurements[routine_name] = self.mp_manager.list()

        if len(self.routines_measurements[routine_name]) >= self.max_queue_size:
            self.routines_measurements[routine_name].pop()

        self.routines_measurements[routine_name].append(duration)
