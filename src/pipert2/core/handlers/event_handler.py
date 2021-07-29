class EventHandler:

    def __init__(self, input_event_pipe):
        self.input_event_pipe = input_event_pipe

    def wait(self):
        return self.input_event_pipe.recv()
