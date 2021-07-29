from collections import defaultdict
from multiprocessing import Pipe, SimpleQueue
from threading import Thread
from functools import partial
from src.pipert2.core.handlers.event_handler import EventHandler
from src.pipert2.utils.method_data import Method


class EventBoard:
    """The event board is responsible for managing the event system in the pipe.

    """

    def __init__(self):
        self.events_pipes = defaultdict(list)
        self.new_events_queue = SimpleQueue()

    def get_event_handler(self, flow_events_to_listen):
        """Return an event handler adjusted to the given events.

        Args:
            flow_events_to_listen: The routines message.

        Returns:
            An event handler adjusted to the given events.

        """

        pipe_output, pipe_input = Pipe(duplex=False)

        for event_name in flow_events_to_listen:
            self.events_pipes[event_name].append(pipe_input)

        return EventHandler(pipe_output)

    def event_loop(self):
        """Wait for new events to come and spread them to the pipes.

        """

        event: Method = self.new_events_queue.get()
        while event.name != "kill":
            for pipe in self.events_pipes[event.name]:
                pipe.send(event)

            event = self.new_events_queue.get()

    def build(self):
        """Start the event loop

        """

        self.event_board_thread = Thread(target=self.event_loop)
        self.event_board_thread.start()

    def get_event_notifier(self):
        """Return a callable for notifying that new event occurred

        """

        def notify_event(output_event_queue, event_name, **kwargs):
            output_event_queue.put(Method(event_name, kwargs))

        return partial(notify_event, output_event_queue=self.new_events_queue)
