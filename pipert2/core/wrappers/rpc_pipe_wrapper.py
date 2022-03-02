try:
    from zerorpc import Server
except ImportError:
    print(f"Oops! seems like zerorpc isn't installed!\nIf you want to use the capabilities of the rpc_wrapper run "
          f"'pip install PipeRT[rpc]'")
    Server = None

if Server:
    from pipert2 import Pipe
    from pipert2.core.wrappers.utils import parse_arguments
    from pipert2.utils.consts import START_EVENT_NAME, STOP_EVENT_NAME, KILL_EVENT_NAME


    class RPCPipeWrapper(Server):
        """A RPC wrapper which invokes pipeline cli commands using the event notifier callback.

        """

        def __init__(self, pipe: Pipe):
            """
                Args:
                    pipe: The pipe that the event will notify through it.

            """
            super().__init__()
            self.notify_callback = pipe.get_event_notify()

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
            self.notify_callback(event_name=KILL_EVENT_NAME)
            self.stop()

        def execute(self, name: str, encoded_arguments: dict = None):
            """Parses user command and arguments and executes it.

            """
            args_type = type(encoded_arguments)
            if args_type == str or encoded_arguments is None:
                if name == self.kill.__name__:
                    self.kill()
                else:
                    kwargs = parse_arguments(encoded_arguments)
                    self.notify_callback(event_name=name, **kwargs)
            elif args_type == dict:
                if name == self.kill.__name__:
                    self.kill()
                self.notify_callback(event_name=name, **encoded_arguments)
