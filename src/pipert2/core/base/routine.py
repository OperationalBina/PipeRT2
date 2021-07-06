from src.pipert2.utils.annotations import marking_functions_annotation

import threading
import multiprocessing as mp
from abc import ABC, abstractmethod
from functools import partial


class Routine(ABC):
    """A routine is responsible for performing one of the component’s main tasks.
    It can be run either as a thread or as a process. First it runs a setup function,
    then it runs its main logic function in a continuous loop (until it is told to terminate),
    and finally it runs a cleanup function.
    """

    events = marking_functions_annotation()
    runners = marking_functions_annotation()

    def __init__(self, name: str, message_handler, logger, *args, **kwargs): # TODO - Add MessageHandler and PipeLogger type hints
        self.name = name
        self.message_handler = message_handler
        self.logger = logger
        self.stop_event = mp.Event()
        self.stop_event.set()

        if "runner" in kwargs and kwargs["runner"] in self.runners.all:
            self.runners.all[kwargs["runner"]](self)
        else:
            self.set_runner_as_thread()

    @abstractmethod
    def main_logic(self, data):
        """The routine logic that will be executed

        Args:
            data: The data for the routine to process
        """

        raise NotImplementedError

    @abstractmethod
    def setup(self) -> None:
        """An initial setup before running"""

        raise NotImplementedError

    @abstractmethod
    def cleanup(self) -> None:
        """The final method that end the routine execution"""

        raise NotImplementedError

    def _extended_run(self) -> None:
        """Wrapper method for executing the entire routine logic.

        """

        self.setup()

        while not self.stop_event.is_set():
            message = self.message_handler.get()
            try:
                output_data = self.main_logic(message.get_payload())
            except Exception as error:
                self.logger.exception(f"The routine has crashed: {error}")
            else:
                message.update_payload(output_data)
                self.message_handler.put(message)

        self.cleanup()

    @runners("thread")
    def set_runner_as_thread(self):
        self.runner_creator = partial(threading.Thread, target=self._extended_run)

    @events("start")
    def start(self) -> None:
        """Start running the routine.

        (This method will be called when the 'start' event is triggered)
        """

        if self.stop_event.is_set():
            self.logger.info("Starting")  # TODO - Maybe add an infrastructure logg type instead of info
            self.stop_event.clear()
            self.runner = self.runner_creator()
            self.runner.start()

    @events("stop")
    def stop(self) -> None:
        """Stop the routine from running.

        (This method will be called when the 'stop' event is triggered)
        """

        if not self.stop_event.is_set():
            self.logger.info("Stopping")
            self.stop_event.set()
            self.runner.join()

    def trigger_event(self, event_name: str) -> None:
        """Trigger an event to start

        Args:
            event_name (str): The name of the event to trigger
        """

        if event_name in self.events.all:
            self.logger.info(f"Running event '{event_name}'")
            for callback in self.events.all[event_name]:
                callback(self)
