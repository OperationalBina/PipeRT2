import flask
from flask import Flask
from flask import Response
from pipert2 import START_EVENT_NAME, STOP_EVENT_NAME, KILL_EVENT_NAME


class APIWrapper:
    def __init__(self, url, notify_callback):
        self.url = url
        self.notify_callback = notify_callback

        self.app = Flask(__name__)

        self.app.add_url_rule("/start", "start", self.start)
        self.app.add_url_rule("/pause", "pause", self.pause)
        self.app.add_url_rule("/kill", "kill", self.kill)
        self.app.add_url_rule("/execute", "execute", self.execute)

    def run_api(self):
        """Run flask api.

        """
        self.app.run(host="localhost", port=8888)

    def start(self):
        """Notify the pipe to start.

        Returns:
            Status 200 when succeed.

        """
        self.notify_callback(START_EVENT_NAME)

        return Response(status=200)

    def pause(self):
        """Notify the pipe to pause.

        Returns:
            Status 200 when succeed.

        """
        self.notify_callback(STOP_EVENT_NAME)

        return Response(status=200)

    def kill(self):
        """Invokes the kill event in the pipe

        Returns:
            Status 200 when succeed.

        """
        self.notify_callback(event_name=KILL_EVENT_NAME)

        return Response(status=200)

    def execute(self):
        """Execute custom event. Should get request with 'event_name' and with optional keys parameters.

        Returns:
            Status 200 when succeed.

        """

        self.notify_callback(**flask.request.args.to_dict())

        return Response(status=200)
