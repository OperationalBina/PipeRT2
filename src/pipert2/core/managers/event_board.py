from collections import defaultdict
from multiprocessing import Pipe, SimpleQueue
from threading import Thread
from functools import partial
from typing import Callable
from src.pipert2.core import EventHandler
from src.pipert2.utils.method_data import Method
from src.pipert2.utils.consts.event_names import KILL_EVENT_NAME, STOP_EVENT_NAME, START_EVENT_NAME

DEFAULT_EVENT_HANDLER_EVENTS = [START_EVENT_NAME, STOP_EVENT_NAME, KILL_EVENT_NAME]


class EventBoard:
    """The event board is responsible for managing the event system in the pipe.

    """

    def __init__(self):
        self.events_pipes = defaultdict(list)
        self.new_events_queue = SimpleQueue()

    def get_event_handler(self, events_to_listen: list):
        """Return an event handler adjusted to the given events.

        Args:
            events_to_listen: List of event names to listen.

        Returns:
            An event handler adjusted to the given events.

        """

        pipe_output, pipe_input = Pipe(duplex=False)

        for event_name in events_to_listen:
            self.events_pipes[event_name].append(pipe_input)

        for default_event_name in DEFAULT_EVENT_HANDLER_EVENTS:
            self.events_pipes[default_event_name].append(pipe_input)

        return EventHandler(pipe_output)

    def event_loop(self):
        """Wait for new events to come and spread them to the pipes.

        """

        event: Method = self.new_events_queue.get()
        while event.event_name != KILL_EVENT_NAME:
            for pipe in self.events_pipes[event.event_name]:
                pipe.send(event)

            event = self.new_events_queue.get()

        # Send the kill event to the other pipes
        for pipe in self.events_pipes[event.event_name]:
            pipe.send(event)

    def build(self):
        """Start the event loop

        """

        self.event_board_thread = Thread(target=self.event_loop)
        self.event_board_thread.start()

    def get_event_notifier(self) -> Callable:
        """Return a callable for notifying that new event occurred

        """

        def notify_event(event_name, output_event_queue, routines_by_flow: dict = {}, **params):
            output_event_queue.put(Method(event_name, routines_by_flow=routines_by_flow, params=params))

        return partial(notify_event, output_event_queue=self.new_events_queue)

    def notify_event(self, event_name, routines_by_flow: dict = {}, **params):
        self.new_events_queue.put(Method(event_name=event_name,
                                         routines_by_flow=routines_by_flow,
                                         params=params))

    def join(self):
        self.event_board_thread.join()
