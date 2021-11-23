import time
import threading
from typing import Dict
from logging import Logger
import multiprocessing as mp
from statistics import median
from pipert2.utils.dummy_object import Dummy
from pipert2.utils.base_event_executor import BaseEventExecutor
from pipert2.utils.annotations import class_functions_dictionary
from pipert2.core.base.routines.source_routine import SourceRoutine
from pipert2.core.base.synchronise_routines.synchroniser_node import SynchroniserNode
from pipert2.utils.consts import START_EVENT_NAME, KILL_EVENT_NAME, NOTIFY_ROUTINE_DURATIONS_NAME, NULL_FPS, \
    SYNCHRONISER_UPDATE_INTERVAL, STOP_EVENT_NAME


class RoutinesSynchroniser(BaseEventExecutor):

    events = class_functions_dictionary()

    def __init__(self, event_board: any, logger: Logger, notify_callback: callable):
        super().__init__(event_board, logger)

        self._logger = logger
        self.notify_callback = notify_callback
        self.wires = {}

        self._stop_event = mp.Event()

        self.routines_measurements: Dict[str, list] = {}
        self.routines_graph: Dict[str, SynchroniserNode] = {}

        self.notify_delay_thread = Dummy()

    def _before_build(self) -> None:
        """Run before the build of the event loop process.

        """

        self.routines_graph = self.create_routines_graph()

    def create_routines_graph(self):
        """Build the routine's graph.

        Returns:
            Multiprocess dictionary of { "routine name": synchronised_node }

        """

        synchronise_graph = {}
        synchroniser_nodes = {}

        for wire in self.wires.values():
            for wire_destination_routine in wire.destinations:
                if wire_destination_routine.name not in synchroniser_nodes:
                    synchroniser_nodes[wire_destination_routine.name] = SynchroniserNode(
                        wire_destination_routine.name,
                        wire_destination_routine.flow_name
                    )

            destinations_synchroniser_nodes = [synchroniser_nodes[wire_destination_routine.name]
                                               for wire_destination_routine
                                               in wire.destinations]

            if wire.source.name in synchroniser_nodes:
                synchroniser_nodes[wire.source.name].nodes = destinations_synchroniser_nodes
            else:
                source_node = SynchroniserNode(
                    wire.source.name,
                    wire.source.flow_name,
                    destinations_synchroniser_nodes
                )

                if isinstance(wire.source, SourceRoutine):
                    synchronise_graph[source_node.name] = source_node

        return synchronise_graph

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

        return NULL_FPS

    def update_fps_loop(self):
        """Update fps for all graph's routines.

        """

        while not self._stop_event.is_set():
            # Run each function of the algorithm for all roots, and then continue to the next functions.
            self._execute_function_for_sources(SynchroniserNode.update_original_fps_by_real_time.__name__, self.get_routine_fps)
            self._execute_function_for_sources(SynchroniserNode.update_fps_by_nodes.__name__)
            self._execute_function_for_sources(SynchroniserNode.update_fps_by_fathers.__name__)
            self._execute_function_for_sources(SynchroniserNode.notify_fps.__name__, self.notify_callback)
            self._execute_function_for_sources(SynchroniserNode.reset.__name__)

            time.sleep(SYNCHRONISER_UPDATE_INTERVAL)

    @events(START_EVENT_NAME)
    def start_notify_process(self):
        """Start the notify process.

        """

        self._stop_event.clear()
        threading.Thread(target=self.update_fps_loop).start()

    @events(STOP_EVENT_NAME)
    def stop_synchronised_process(self):
        """Kill the listening the queue process.

        """

        self._stop_event.set()

    @events(KILL_EVENT_NAME)
    def kill_synchronised_process(self):
        """Kill the listening the queue process.

        """

        self._stop_event.set()

    @events(NOTIFY_ROUTINE_DURATIONS_NAME)
    def update_finish_routine_logic_time(self, source_name: str, data: []):
        """Updating the duration of routine.

        Args:
            source_name: The source routine name.
            data: The durations time.
        """

        self.routines_measurements[source_name] = list(data)

    def _execute_function_for_sources(self, name: str, param=None):
        """Execute the callback function for all the graph's sources.

        Args:
            name: Function name in synchronise node to activate

        """

        for value in self.routines_graph.values():
            if param is not None:
                value.__getattribute__(name)(param)
            else:
                value.__getattribute__(name)()
