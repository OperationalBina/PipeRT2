from src.pipert2.core.base.flow import Flow
from src.pipert2.core.base.wire import Wire
from src.pipert2.core.base.routine import Routine
from src.pipert2.core.base.logger import PipeLogger
from src.pipert2.core.managers.network import Network
from src.pipert2.core.managers.event_board import EventBoard
from src.pipert2.utils.consts.event_names import KILL_EVENT_NAME
from src.pipert2.core.base.data_transmitter import DataTransmitter
from src.pipert2.core.base.basic_transmitter import BasicTransmitter


class Pipe:
    """The pipe object is the center of the pipe.
    Once it is created it act as a central registry for the
    pipe methods such as create flows, register routines, notify events
    and more.

    """

    def __init__(self, network: Network, logger: PipeLogger, data_transmitter: DataTransmitter = BasicTransmitter()):  # TODO - default logger and default networking (Queue)
        """
        Args:
            network: Network object responsible for the routine's communication.
            logger: PipeLogger object for logging the pipe actions.
            data_transmitter: DataTransmitter object to indicate how data flows through the pipe by default.

        Attributes:
            network: Network object responsible for the routine's communication.
            logger: PipeLogger object for logging the pipe actions.
            data_transmitter: DataTransmitter object to indicate how data flows through the pipe by default.
            flows (dict[str, Flow]): Dictionary mapping the pipe flows to their name.
            event_board (EventBoard): EventBoard object responsible for the pipe events.

        """

        self.network = network
        self.logger = logger
        self.flows = {}
        self.event_board = EventBoard()
        self.default_data_transmitter = data_transmitter

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

        flow = Flow(flow_name, self.event_board, self.logger.get_child(), routines=list(routines))
        self.flows[flow_name] = flow

        if auto_wire:
            data_transmitter = self.default_data_transmitter if data_transmitter is None else data_transmitter

            for first_routine, second_routine in zip(routines, routines[1:]):
                self.network.link(source=first_routine, destinations=(second_routine,),
                                  data_transmitter=data_transmitter)

    def link(self, *wires):
        """Connect the routines to each other by their wires configuration.

        Args:
            wires (Wire): List of wires to connect their routines

        """

        for wire in wires:
            data_transmitter = wire.data_transmitter if wire.data_transmitter else self.default_data_transmitter

            self.network.link(source=wire.source, destinations=wire.destinations, data_transmitter=data_transmitter)

    def build(self):
        """Build the pipe to be ready to start working.

        """

        for flow in self.flows.values():
            flow.build()

    def notify_event(self, event_name: str, **event_parameters) -> None:
        """Notify an event has started

        Args:
            event_name: The name of the event to notify

        """

        self.event_board.notify_event(event_name, **event_parameters)

    def join(self, to_kill=False):
        """Block the execution until all of the flows have been killed

        """

        if to_kill:
            self.notify_event(KILL_EVENT_NAME)

        for flow in self.flows.values():
            flow.join()
