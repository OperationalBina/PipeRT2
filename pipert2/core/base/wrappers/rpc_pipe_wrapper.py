from zerorpc import Server
from pipert2.core.base.wrappers.utils import parse_arguments
from pipert2.utils.consts import START_EVENT_NAME, STOP_EVENT_NAME, JOIN_EVENT_NAME


class RPCPipeWrapper(Server):
    """A RPC wrapper which invokes pipeline cli commands using the event notifier callback.

    """

    def __init__(self, notify_callback: callable):
        """
            Args:
                notify_callback: The callback for notifying event.

        """
        super().__init__()
        self.notify_callback = notify_callback

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
        self.notify_callback(event_name=START_EVENT_NAME)

    def pause(self):
        """Invokes the stop event in the pipe

        """
        self.notify_callback(event_name=STOP_EVENT_NAME)

    def kill(self):
        """Invokes the kill event in the pipe

        """
        self.notify_callback(event_name=JOIN_EVENT_NAME, to_kill=True)
        self.stop()

    def execute(self, name: str, encoded_arguments: str = None):
        """Parses user command and arguments and executes it.

        """
        if name == self.kill.__name__:
            self.notify_callback(event_name=JOIN_EVENT_NAME, to_kill=True)
            self.stop()
        else:
            kwargs = parse_arguments(encoded_arguments)
            self.notify_callback(event_name=name, **kwargs)
