import zerorpc
from zerorpc import Server
from pipert2.utils.consts import START_EVENT_NAME, STOP_EVENT_NAME


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
        self.notify_callback(event_name="join", to_kill=True)
        self.stop()

    def execute(self, name):
        self.notify_callback(event_name=name)
