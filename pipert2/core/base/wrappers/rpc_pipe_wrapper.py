from zerorpc import Server
from pipert2.core.base.pipe import Pipe
from pipert2.utils.consts import START_EVENT_NAME, STOP_EVENT_NAME


class RPCPipeWrapper(Server):
    """A RPC wrapper which invokes pipeline cli commands

    """

    def __init__(self, pipe: Pipe):
        """
            Arguments:
                pipe: the center of the pipeline
        """
        super().__init__()
        self.pipe = pipe

    def run_rpc_server(self, endpoint: str):
        """Binds it to a given endpoint and runs the rpc server.

            Arguments:
                endpoint: server's endpoint
        """
        self.bind(endpoint)
        self.run()

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
        self.stop()
