from src.pipert2.core.base.logger import PipeLogger
from src.pipert2.core.base.routine import Routine
from src.pipert2.core.managers.event_board import EventBoard
from src.pipert2.utils.annotations import marking_functions_annotation
from multiprocessing import Process


class Flow:
    events = marking_functions_annotation()

    def __init__(self, name: str, event_board: EventBoard, logger: PipeLogger, *routines: Routine):
        self.routines = {}
        self.name = name

        flow_events_to_listen = set(self.get_events().keys())

        for routine in routines:
            routine.initialize(logger=logger.get_child(), event_notifier=event_board.get_notifier())
            flow_events_to_listen.update(routine.get_events().keys())

        self.logger = logger
        self.event_handler = event_board.get_event_handler(flow_events_to_listen)

    def build(self):
        self.flow_process = Process(target=self.run)
        self.flow_process.start()

    # The process function, starts the event listener
    def run(self):
        event_names = ""
        while event_names != "kill":
            self.event_handler.wait()
            event_names = self.event_handler.get_names()
            for event in event_names:  # Maybe do this in threads to not get stuck on listening to events.
                self.execute_event(event)

    @events("start")
    def start(self):
        self.logger.info("Starting")

    @events("stop")
    def stop(self):
        self.logger.info("Stopping")

    def execute_event(self, event_name):
        for routine in self.routines.values():
            routine.execute_event(event_name)

        if event_name in self.events.all:
            self.logger.info(f"Running event '{event_name}'")
            for callback in self.events.all[event_name]:
                callback(self)

    @classmethod
    def get_events(cls):
        return cls.events.all[cls.__name__]
