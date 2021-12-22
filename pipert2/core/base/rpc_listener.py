from pipert2.utils.consts import START_EVENT_NAME, STOP_EVENT_NAME, KILL_EVENT_NAME


class RPCListener:
    """A RPC listener which invokes pipeline cli commands

    """

    def __init__(self, pipe):
        self.pipe = pipe

    def start(self):
        """Invokes the start event in the pipe

        """
        self.pipe.notify_event(event_name=START_EVENT_NAME)

    def stop(self):
        """Invokes the stop event in the pipe

        """
        self.pipe.notify_event(event_name=STOP_EVENT_NAME)

    def kill(self):
        """Invokes the kill event in the pipe

        """
        self.pipe.notify_event(event_name=KILL_EVENT_NAME)

    def event(self, event: str):
        """General Invocation of pipe events

        """
        raise NotImplementedError()
