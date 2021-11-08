import threading
import time
from statistics import median
from threading import Thread
from typing import Dict
from logging import Logger
import multiprocessing as mp
from pipert2.utils.method_data import Method
from pipert2.utils.interfaces import EventExecutorInterface
from pipert2.utils.annotations import class_functions_dictionary
from pipert2.utils.consts import START_EVENT_NAME, KILL_EVENT_NAME, FINISH_ROUTINE_LOGIC_NAME, START_ROUTINE_LOGIC_NAME
from pipert2.core.base.routines.source_routine import SourceRoutine
from pipert2.core.base.synchronize_routines.synchronizer_node import SynchronizerNode


class RoutinesSynchronizer(EventExecutorInterface):

    events = class_functions_dictionary()

    def __init__(self, updating_interval: float,
                 event_board: any,
                 logger: Logger,
                 wires: Dict,
                 notify_callback: callable):

        self.max_queue_size = 200
        self.wires = wires
        self._logger = logger
        self.notify_callback = notify_callback
        self.updating_interval = 4

        self._stop_event = mp.Event()

        synchronizer_events_to_listen = set(self.get_events().keys())
        self.event_handler = event_board.get_event_handler(synchronizer_events_to_listen)

        mp_manager = mp.Manager()
        mp_manager.register('SynchronizerNode', SynchronizerNode)

        self.mp_manager = mp_manager
        self.routines_graph: Dict[str, SynchronizerNode] = mp_manager.dict()

        self.notify_delay_thread: threading.Thread = threading.Thread(target=self.update_delay_iteration)

        self.routines_measurements: Dict[str, list] = self.mp_manager.dict()

        self.base_listen_to_events_process: mp.Process = None

    def execute_event(self, event: Method) -> None:
        """Execute the event that notified.

        Args:
            event: The event to execute.
        """

        EventExecutorInterface.execute_event(self, event)

    def build(self):
        """Start the queue listener process.

        """

        self.routines_graph = self.create_routines_graph()
        self.base_listen_to_events_process = mp.Process(target=self.listen_to_events)
        self.base_listen_to_events_process.start()

        self._stop_event.set()

    def listen_to_events(self):
        event = self.event_handler.wait()
        while not event.event_name == KILL_EVENT_NAME:
            self.execute_event(event)
            event = self.event_handler.wait()
            print(f"In synchronizer get event: {event.event_name}")

        self.execute_event(Method(KILL_EVENT_NAME))

        print("base listing finishs")

    def create_routines_graph(self) -> 'DictProxy':
        """Build the routine's graph.

        Returns:
            Multiprocess dictionary of { "routine name", synchronized_node }
        """

        synchronize_graph = {}
        synchronizer_nodes = {}

        for wire in self.wires.values():
            for wire_destination_routine in wire.destinations:
                if wire_destination_routine.name not in synchronizer_nodes:
                    synchronizer_nodes[wire_destination_routine.name] = SynchronizerNode(
                        wire_destination_routine.name,
                        wire_destination_routine.flow_name,
                        [],
                        self.mp_manager
                    )

            destinations_synchronizer_nodes = [synchronizer_nodes[wire_destination_routine.name]
                                               for wire_destination_routine
                                               in wire.destinations]

            if wire.source.name in synchronizer_nodes:
                synchronizer_nodes[wire.source.name].nodes = destinations_synchronizer_nodes
            else:
                source_node = SynchronizerNode(
                    wire.source.name,
                    wire.source.flow_name,
                    destinations_synchronizer_nodes,
                    self.mp_manager
                )

                if isinstance(wire.source, SourceRoutine):
                    synchronize_graph[source_node.name] = source_node

        return self.mp_manager.dict(synchronize_graph)

    def get_routine_fps(self, routine_name):
        """Get the median fps by routine name.

        Args:
            routine_name: The routine name.

        Returns:
            The median fps for the required fps.
        """

        if routine_name in self.routines_measurements:
            routine_fps_list = self.routines_measurements[routine_name]

            if len(routine_fps_list) > 0:
                return 1 / median(routine_fps_list)

        return 0

    @classmethod
    def get_events(cls):
        """Get the events of the synchronize_routines.

        Returns:
            dict[str, set[Callback]]: The events callbacks mapped by their events.
        """

        return cls.events.all[cls.__name__]

    def update_delay_iteration(self):
        """One iteration of updating fps for all graph's routines.

        """

        while not self._stop_event.is_set():
            print(f'Stop event check in loop - {self._stop_event.is_set()}')
            self._execute_function_for_sources(SynchronizerNode.update_original_fps_by_real_time.__name__, self.get_routine_fps)
            self._execute_function_for_sources(SynchronizerNode.update_fps_by_nodes.__name__)
            self._execute_function_for_sources(SynchronizerNode.update_fps_by_fathers.__name__)
            self._execute_function_for_sources(SynchronizerNode.notify_fps.__name__, self.notify_callback)
            self._execute_function_for_sources(SynchronizerNode.reset.__name__)
            time.sleep(1)

        print("synchnozier OUT")

    @events(START_EVENT_NAME)
    def start_notify_process(self):
        """Start the notify process.

        """

        if self._stop_event.is_set():
            self._stop_event.clear()
            self.notify_delay_thread.start()

    @events(KILL_EVENT_NAME)
    def kill_synchronized_process(self):
        """Kill the listening the queue process.

        """

        print("Kill event start")

        if not self._stop_event.is_set():
            print("set stop event")
            self._stop_event.set()

    @events(FINISH_ROUTINE_LOGIC_NAME)
    def update_finish_routine_logic_time(self, **params):
        """Updating the duration of routine.

        Args:
            **params: Dictionary contained the routine name.
        """

        routine_name = params['routine_name']
        durations: [] = params['durations']

        if routine_name not in self.routines_measurements:
            self.routines_measurements[routine_name] = self.mp_manager.list()

        expected_length = len(durations) + len(self.routines_measurements[routine_name])

        if expected_length >= self.max_queue_size:
            for _ in range(self.max_queue_size - expected_length):
                self.routines_measurements[routine_name].pop(0)

        [self.routines_measurements[routine_name].append(duration) for duration in durations]

    def join(self):
        self.base_listen_to_events_process.join()

    def _execute_function_for_sources(self, callback: callable, param=None):
        """Execute the callback function for all the graph's sources.

        Args:
            callback: Function in synchronize node to activate

        """

        for value in self.routines_graph.values():
            if param is not None:
                value.__getattribute__(callback)(param)
            else:
                value.__getattribute__(callback)()
