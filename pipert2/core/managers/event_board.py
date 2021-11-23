from threading import Thread
from functools import partial
from typing import Callable, Set
from collections import defaultdict
from pipert2.utils.method_data import Method
from multiprocessing import Pipe, SimpleQueue
from pipert2.core.handlers.event_handler import EventHandler
from pipert2.utils.consts.event_names import KILL_EVENT_NAME, STOP_EVENT_NAME, START_EVENT_NAME

DEFAULT_EVENT_HANDLER_EVENTS = [START_EVENT_NAME, STOP_EVENT_NAME, KILL_EVENT_NAME]


class EventBoard:
    """The event board is responsible for managing the event system in the pipe.

    """

    def __init__(self):
        self.events_pipes = defaultdict(list)
        self.new_events_queue = SimpleQueue()

    def get_event_handler(self, events_to_listen: Set[str]):
        """Return an event handler adjusted to the given events.

        Args:
            events_to_listen: List of event names to listen.

        Returns:
            An event handler adjusted to the given events.

        """

        pipe_output, pipe_input = Pipe(duplex=False)
        events_to_listen.update(DEFAULT_EVENT_HANDLER_EVENTS)

        for event_name in events_to_listen:
            self.events_pipes[event_name].append(pipe_input)

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

        def notify_event(output_event_queue, event_name, specific_flow_routines: dict = defaultdict(list), **params):
            output_event_queue.put(Method(event_name,
                                          specific_flow_routines=specific_flow_routines,
                                          params=params))

        return partial(notify_event, self.new_events_queue)

    def notify_event(self, event_name, specific_flow_routines: dict = defaultdict(list), **params):
        self.new_events_queue.put(Method(event_name=event_name,
                                         specific_flow_routines=specific_flow_routines,
                                         params=params))

    def join(self):
        self.event_board_thread.join()
