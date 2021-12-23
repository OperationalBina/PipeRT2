from zerorpc import Server
from pipert2.core.base.pipe import Pipe
from pipert2.utils.consts import START_EVENT_NAME, STOP_EVENT_NAME


class RPCPipeWrapper:
    """A RPC wrapper which invokes pipeline cli commands

    """

    def __init__(self, pipe: Pipe, endpoint: str):
        self.pipe = pipe
        self.rpc_server = Server(self)
        self.endpoint = endpoint
        self.rpc_server.bind(self.endpoint)
        self.rpc_server.run()

    def start(self):
        """Invokes the start event in the pipe

        """
        self.pipe.notify_event(event_name=START_EVENT_NAME)

    def pause(self):
        """Invokes the stop event in the pipe

        """
        self.pipe.notify_event(event_name=STOP_EVENT_NAME)

    def kill(self):
        """Invokes the kill event in the pipe

        """
        self.pipe.join(to_kill=True)
        self.rpc_server.stop()
