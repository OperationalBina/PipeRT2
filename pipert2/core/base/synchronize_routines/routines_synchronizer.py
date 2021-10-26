from logging import Logger
import multiprocessing as mp
from typing import List, Dict
from pipert2.core.base.wire import Wire
from pipert2.utils.method_data import Method
from pipert2.utils.interfaces import EventExecutorInterface
from pipert2.utils.annotations import class_functions_dictionary
from pipert2.utils.consts import START_EVENT_NAME, KILL_EVENT_NAME
from pipert2.core.base.routines.source_routine import SourceRoutine
from pipert2.core.base.synchronize_routines.synchronizer_node import SynchronizerNode


class RoutinesSynchronizer(EventExecutorInterface):

    events = class_functions_dictionary()

    def __init__(self, updating_interval: int, event_board: any, logger: Logger, wires: List[Wire], notify: callable):
        self.wires = wires
        self._logger = logger
        self.notify_callback = notify
        self.updating_interval = updating_interval

        self.stop_event = mp.Event()

        self.event_listening_process: mp.Process = mp.Process(target=self.listen_events)
        self.update_delay_process: mp.Process = mp.Process(target=self.update_delay)

        synchronizer_events_to_listen = set(self.get_events().keys())
        self.event_handler = event_board.get_event_handler(synchronizer_events_to_listen)

        mp_manager = mp.Manager()
        mp_manager.register('SynchronizerNode', SynchronizerNode)

        self.mp_manager = mp_manager
        self.routines_graph: Dict[str, SynchronizerNode] = mp_manager.dict()

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
        self.event_listening_process.start()

    def create_routines_graph(self) -> 'DictProxy':
        """Build the routine's graph.

        Returns:
            Multiprocess dictionary of { "routine name", synchronized_node }
        """

        synchronize_graph = {}
        synchronizer_nodes = {}

        for wire in self.wires:
            for wire_destination_routine in wire.destinations:
                if wire_destination_routine.name not in synchronizer_nodes:
                    synchronizer_nodes[wire_destination_routine.name] = SynchronizerNode(
                        wire_destination_routine.name,
                        self.get_routine_fps(wire_destination_routine.name),
                        [],
                        self.notify_callback
                    )

            destinations_synchronizer_nodes = [synchronizer_nodes[wire_destination_routine.name]
                                               for wire_destination_routine
                                               in wire.destinations]

            if wire.source.name in synchronizer_nodes:
                synchronizer_nodes[wire.source.name].nodes = destinations_synchronizer_nodes
            else:
                source_node = SynchronizerNode(
                    wire.source.name,
                    self.get_routine_fps(wire.source.name),
                    destinations_synchronizer_nodes,
                    self.notify_callback
                )

                if isinstance(wire.source, SourceRoutine):
                    synchronize_graph[source_node.name] = source_node

        return self.mp_manager.dict(synchronize_graph)

    def get_routine_fps(self, routine_name: str):
        """Calculate the fps for a specific routine.

        Args:
            routine_name: The routine name.

        Returns:
            The routine's rps.
        """

        return 0

    def join(self):
        """Join the event listening process.

        """

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
        """Get the events of the synchronize_routines.

        Returns:
            dict[str, set[Callback]]: The events callbacks mapped by their events.
        """

        return cls.events.all[cls.__name__]

    def update_delay(self):
        """Notify the calculated delay time to all routines.

        """

        while not self.stop_event.is_set():
            self.update_delay_iteration()

    def update_delay_iteration(self):
        """One iteration of updating fps for all graph's routines.

        """

        self._execute_function_for_sources(SynchronizerNode.update_fps_by_nodes.__name__)
        self._execute_function_for_sources(SynchronizerNode.update_fps_by_fathers.__name__)
        self._execute_function_for_sources(SynchronizerNode.notify_fps.__name__)
        self._execute_function_for_sources(SynchronizerNode.reset.__name__)

    @events(START_EVENT_NAME)
    def start_notify_process(self):
        """Start the notify process.

        """

        self.stop_event.clear()
        self.update_delay_process.start()

    @events(KILL_EVENT_NAME)
    def kill_synchronized_process(self):
        """Kill the listening the queue process.

        """

        if not self.stop_event.is_set():
            self.stop_event.set()

        self.update_delay_process.terminate()

    def _execute_function_for_sources(self, callback: callable):
        """Execute the callback function for all the graph's sources.

        Args:
            callback: Function in synchronize node to activate

        """

        for value in self.routines_graph.values():
            value.__getattribute__(callback)()
