from abc import ABCMeta, abstractmethod
from collections import defaultdict
from flask import Flask
from pipert2 import START_EVENT_NAME, STOP_EVENT_NAME, KILL_EVENT_NAME


class CommonPipe(metaclass=ABCMeta):
    """The CommonPipe object is the relevant desired functionalities of the Flask Server.

    """

    def __init__(self):
        self.run_cli_api()

    def run_cli_api(self):
        app = Flask(__name__)

        @app.route('/Start', methods=['POST'])
        def start_pipline():
            self.notify_event(event_name=START_EVENT_NAME)

        @app.route('/Stop', methods=['POST'])
        def start_pipline():
            self.notify_event(event_name=STOP_EVENT_NAME)

        @app.route('/Kill', methods=['POST'])
        def start_pipline():
            self.notify_event(event_name=KILL_EVENT_NAME)

    @abstractmethod
    def notify_event(self, event_name: str, specific_flow_routines: dict = defaultdict(list),
                     **event_parameters) -> None:
        """Notify an event has started

        Args:
            event_name: The name of the event to notify
            specific_flow_routines: In order to notify specific routines/flows we insert a dictionary in the following format -
                For specific routines in a specific flow, each key/value element needs to be in this format - "flow_name": [routines]
                For all of the routines in a specific flow, each element needs to be in this format - "flow_name" - []
            **event_parameters: Parameters for the event to be executed

        """
        pass

    @abstractmethod
    def join(self, to_kill=False):
        """Block the execution until all of the flows have been killed

        """
        pass

    @abstractmethod
    def build(self):
        """Build the pipe to be ready to start working

        """
        pass
