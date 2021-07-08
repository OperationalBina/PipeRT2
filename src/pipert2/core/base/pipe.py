from src.pipert2.core.base.flow import Flow
from src.pipert2.core.base.logger import PipeLogger
from src.pipert2.core.managers.event_board import EventBoard
from src.pipert2.core.managers.network import Network


# TODO - Add typings
class Pipe:
    """The pipe object is the center of the pipe.
    Once it is created it act as a central registry for the
    pipe methods such as create flows, register routines, notify events
    and more.
    """

    def __init__(self, networking: Network, logger: PipeLogger):  # TODO - default logger and default networking (Queue)
        self.network = networking
        self.logger = logger
        self.flows = {}
        self.event_board = EventBoard()

    def create_flow(self, flow_name: str, auto_wire: bool = True, *routines):
        """Create a new flow in the pipe.

        Args:
            flow_name (str): The name of the flow to be created
            auto_wire (bool): Automatically connect the routines to each other by the order of their entry.
            routines: (Routine): List of routines to register to the flow.
        """

        flow = Flow(flow_name)
        flow.register_routines(self.event_board, self.network, auto_wire, *routines)
        self.flows[flow_name] = flow

    def link(self, *wires):
        """Connect the routines to each other by their wires configuration.

        Args:
            wires (Wire): List of wires to connect their routines
        """

        for wire in wires:
            wire.connect(self.network)
            # TODO - should we do it outside the wires or just create the 'connect' method in the wire class ???

    def build(self):
        """Build the pipe to be ready to start working.
        """

        # TODO - Start the flows processes (and inside their event listeners should start).
        pass

    def notify_event(self, event_name: str) -> None:
        """Notify an event has started

        Args:
            event_name: The name of the event to notify
        """

        self.event_board.notify_event(event_name)

    def join(self):
        """Block the execution until all of the flows have been killed
        """

        for flow in self.flows.values():
            flow.join()
