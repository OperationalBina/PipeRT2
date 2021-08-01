from src.pipert2.core.base.flow import Flow
from src.pipert2.core.base.logger import PipeLogger
from src.pipert2.core.base.routine import Routine
from src.pipert2.core.base.wire import Wire
from src.pipert2.core.managers.event_board import EventBoard
from src.pipert2.core.managers.network import Network


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

    def create_flow(self, flow_name: str, auto_wire: bool = True, *routines: Routine):
        """Create a new flow in the pipe.

        Args:
            flow_name (str): The name of the flow to be created
            auto_wire (bool): Automatically connect the routines to each other by the order of their entry.
            routines: (Routine): List of routines to register to the flow.

        """

        for routine in routines:
            routine.initialize(message_handler=self.network.get_message_handler(routine.name),
                               event_notifier=self.event_board.get_notifier())

        flow = Flow(flow_name, self.event_board, self.logger.get_child(), *routines)
        self.flows[flow_name] = flow

        if auto_wire:
            for first_routine, second_routine in zip(routines, routines[1:]):
                self.network.link(src=first_routine, destination=second_routine)

    def link(self, *wires):
        """Connect the routines to each other by their wires configuration.

        Args:
            wires (Wire): List of wires to connect their routines

        """

        for wire in wires:
            self.network
            # TODO - should we do it outside the wires or just create the 'connect' method in the wire class ???

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

    def join(self):
        """Block the execution until all of the flows have been killed

        """

        for flow in self.flows.values():
            flow.join()

# pipe = Pipe(networking=RedisNetworking, logger="")
#
# r1 = R1(abc=123)
# r2 = R2()
# r3 = R3()
#
# pipe.create_flow(flow_name="1", auto_wire=False,  r1, r2)
# pipe.create_flow(r3, flow_name="2")
#
# pipe.link(Wire(source=r1, destinations=(r2, r3)),
#           Wire(source=r2, destinations=(r3, )))
#
# pipe.build()
#
# pipe.notify_event("start")
#
# time.sleep(20)
#
# pipe.notify_event("kill")
#
# pipe.join()