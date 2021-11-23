from typing import Dict
from logging import Logger
from collections import defaultdict
from pipert2.core.base.flow import Flow
from pipert2.core.base.wire import Wire
from pipert2.core.base.routine import Routine
from pipert2.core.managers.network import Network
from pipert2.core.managers.event_board import EventBoard
from pipert2.utils.consts.event_names import KILL_EVENT_NAME
from pipert2.core.base.data_transmitter import DataTransmitter
from pipert2.core.managers.networks.queue_network import QueueNetwork
from pipert2.core.base.validators import wires_validator, flow_validator
from pipert2.core.base.transmitters.basic_transmitter import BasicTransmitter
from pipert2.core.base.synchronise_routines.routines_synchroniser import RoutinesSynchroniser
from pipert2.utils.logging_module_modifiers import add_pipe_log_level, get_default_print_logger

add_pipe_log_level()


class Pipe:
    """The pipe object is the center of the pipe.
    Once it is created it act as a central registry for the
    pipe methods such as create flows, register routines, notify events
    and more.

    """

    def __init__(self, network: Network = QueueNetwork(),
                 logger: Logger = get_default_print_logger("Pipe"),
                 data_transmitter: DataTransmitter = BasicTransmitter(),
                 auto_pacing_mechanism: bool = False):
        """
        Args:
            network: Network object responsible for the routine's communication.
            logger: Logger object for logging the pipe actions.
            data_transmitter: DataTransmitter object to indicate how data flows through the pipe by default.
            auto_pacing_mechanism: True if the user want to use auto pacing mechanism.

        Attributes:
            network: Network object responsible for the routine's communication.
            logger: Logger object for logging the pipe actions.
            data_transmitter: DataTransmitter object to indicate how data flows through the pipe by default.
            flows (dict[str, Flow]): Dictionary mapping the pipe flows to their name.
            event_board (EventBoard): EventBoard object responsible for the pipe events.
            routine_synchroniser (RoutinesSynchroniser): Routine synchroniser if auto_pacing_mechanism is true, else None.

        """

        self.network = network
        self.logger = logger
        self.flows = {}
        self.event_board = EventBoard()
        self.default_data_transmitter = data_transmitter
        self.wires: Dict[tuple, Wire] = {}

        if auto_pacing_mechanism:
            self.routine_synchroniser = RoutinesSynchroniser(event_board=self.event_board,
                                                             logger=self.logger,
                                                             notify_callback=self.event_board.get_event_notifier())
        else:
            self.routine_synchroniser = None

    def create_flow(self, flow_name: str, auto_wire: bool, *routines: Routine,
                    data_transmitter: DataTransmitter = None):
        """Create a new flow in the pipe.

        Args:
            flow_name (str): The name of the flow to be created.
            auto_wire (bool): Automatically connect the routines to each other by the order of their entry.
            routines: (Routine): List of routines to register to the flow.
            data_transmitter (DataTransmitter): A data transmitter object that indicates how data will be transferred
                                                inside the flow.

        """

        for routine in routines:
            routine.initialize(message_handler=self.network.get_message_handler(routine.name),
                               event_notifier=self.event_board.get_event_notifier())

        flow = Flow(flow_name, self.event_board, self.logger.getChild(flow_name), routines=list(routines))
        self.flows[flow_name] = flow

        if auto_wire:
            for first_routine, second_routine in zip(routines, routines[1:]):
                wire = Wire(source=first_routine, destinations=(second_routine,), data_transmitter=data_transmitter)
                self.wires[(wire.source.flow_name, wire.source.name)] = wire

    def link(self, *wires):
        """Connect the routines to each other by their wires configuration.

        Args:
            wires (Wire): List of wires to connect their routines

        """

        for wire in wires:
            self.wires[(wire.source.flow_name, wire.source.name)] = wire

    def build(self):
        """Build the pipe to be ready to start working.

        """

        self._validate_pipe()

        for wire in self.wires.values():
            data_transmitter = wire.data_transmitter if wire.data_transmitter is not None else self.default_data_transmitter
            self.network.link(source=wire.source, destinations=wire.destinations, data_transmitter=data_transmitter)

        for flow in self.flows.values():
            flow.build()

        if self.routine_synchroniser is not None:
            self.routine_synchroniser.wires = self.wires
            self.routine_synchroniser.build()

        self.event_board.build()

    def notify_event(self, event_name: str, specific_flow_routines: dict = defaultdict(list),
                     **event_parameters) -> None:
        """Notify an event has started

        Args:
            event_name: The name of the event to notify
            specific_flow_routines: In order to notify specific routines/flows we insert a dictionary in the following format -
                For specific routines in a specific flow, each key/value element needs to be in this format - "flow_name": [routines]
                For all of the routines in a specific flow, each element needs to be in this format - "flow_name" - []
            **event_parameters: Parameters for the event to be executed

            """

        self.event_board.notify_event(event_name, specific_flow_routines, **event_parameters)

    def join(self, to_kill=False):
        """Block the execution until all of the flows have been killed

        """

        if to_kill:
            self.notify_event(KILL_EVENT_NAME)

        for flow in self.flows.values():
            flow.join()

        self.logger.plog(f"Joined all flows")

        self.event_board.join()
        self.logger.plog(f"Joined event board")

        if self.routine_synchroniser is not None:
            self.routine_synchroniser.join()
            self.logger.plog("Joined synchroniser")

    def _validate_pipe(self):
        """Validate routines and wires in current pipeline.

        Raises:
            FloatingRoutine: If flows contain a routine that don't link to any other routine.
            WiresValidation: If wires are not valid.
        """

        flow_validator.validate_flow(self.flows, self.wires)
        wires_validator.validate_wires(self.wires.values())
