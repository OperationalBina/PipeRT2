import time
import multiprocessing as mp
from pipert2.utils.method_data import Method
from pipert2.utils.interfaces import EventExecutorInterface
from pipert2.utils.annotations import class_functions_dictionary
from pipert2.utils.consts import START_EVENT_NAME, KILL_EVENT_NAME


class RoutineDelaySynchronizer(EventExecutorInterface):

    events = class_functions_dictionary()

    def __init__(self, synchronize_interval: float, event_board: any, logger):
        self._logger = logger
        self.synchronize_interval = synchronize_interval

        self.stop_event = mp.Event()
        self.stop_event.set()

        self.delay_time = mp.Value('d', 0.0)
        self.logic_duration_time_routines = mp.Manager().dict()

        self.event_listening_process: mp.Process = mp.Process(target=self.listen_events)

        synchronizer_events_to_listen = set(self.get_events().keys())
        self.event_handler = event_board.get_event_handler(synchronizer_events_to_listen)

    def execute_event(self, event: Method) -> None:
        """Execute the event that notified.

        Args:
            event: The event to execute.
        """

        EventExecutorInterface.execute_event(self, event)

    def start_event_listening(self):
        """BStart the queue listener process.

        """

        self.event_listening_process.start()

    def join(self):
        self.event_listening_process.join()

    def listen_events(self) -> None:
        """The synchronize process, executing the pipe events that occur.

        """

        event = self.event_handler.wait()
        while not event.event_name == KILL_EVENT_NAME:
            self.execute_event(event)
            event = self.event_handler.wait()

        self.execute_event(Method(KILL_EVENT_NAME))

    @classmethod
    def get_events(cls):
        """Get the events of the synchronizer.

        Returns:
            dict[str, set[Callback]]: The events callbacks mapped by their events.

        """

        return cls.events.all[cls.__name__]

    def update_delay_time(self):
        """Notify the calculated delay time to all routines.

        """

        while not self.stop_event.is_set():
            max_delay_time = max(self.logic_duration_time_routines.values(), default=0)
            self.delay_time.value = max_delay_time
            time.sleep(self.synchronize_interval)

    def run_synchronized(self, routine_callable: callable, routine_name: str):
        """Run the routine callable logic with the delay time required.

        Args:
            routine_callable: Callback for logic's function.
            routine_name: The logic's name.
        """

        extended_run_start_time = time.time()

        routine_callable()

        duration_of_extended_run = time.time() - extended_run_start_time
        self.logic_duration_time_routines[routine_name] = duration_of_extended_run

        routine_delay_time = self.delay_time.value - duration_of_extended_run

        if routine_delay_time > 0:
            time.sleep(routine_delay_time)

    @events(START_EVENT_NAME)
    def start_notify_process(self):
        """Start the notify process.

        """

        self.stop_event.clear()
        mp.Process(target=self.update_delay_time).start()

    @events(KILL_EVENT_NAME)
    def kill_synchronized_process(self):
        """Kill the listening the queue process.

        """

        if not self.stop_event.is_set():
            self.stop_event.set()
