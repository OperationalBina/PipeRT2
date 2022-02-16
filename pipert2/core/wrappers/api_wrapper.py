try:
    import flask
    from flask import Flask
    from flask import Response
    from flask_cors import CORS
except ImportError:
    print(f"Oops! seems like flask isn't installed!\nIf you want to use the capabilities of the api_wrapper run 'pip "
          f"install PipeRT[api]'")
    flask = None

if flask:
    from pipert2.core.base import Pipe
    from multiprocessing import Process
    from pipert2.utils.consts import START_EVENT_NAME, STOP_EVENT_NAME, KILL_EVENT_NAME


    class APIWrapper:
        def __init__(self, host: str, port: int, pipe: Pipe):
            """Api wrapper for notify events through HTTP.

            Args:
                host: The host the API will run on.
                port: The port the API will run in.
                pipe: The pipe to notify event through it.
            """

            self.notify_callback = pipe.get_event_notify()
            self.pipe = pipe

            self.app = Flask(__name__)
            self.app.add_url_rule("/start", "start", self.start, methods=['POST'])
            self.app.add_url_rule("/pause", "pause", self.pause, methods=['POST'])
            self.app.add_url_rule("/kill", "kill", self.kill, methods=['POST'])
            self.app.add_url_rule("/pipe/structure", "pipe_structure", self.get_pipe_structure, methods=['GET'])

            self.app.add_url_rule("/routines/<routine_name>/events/<event_name>/execute/",
                                  "routine_execute",
                                  self.routine_execute,
                                  methods=['POST'])

            self.app.add_url_rule("/routines/events/<event_name>/execute/",
                                  "routines_execute",
                                  self.routines_execute,
                                  methods=['POST'])

            self.api_process = Process(target=self.app.run, args=(host, port))

            CORS(self.app)

        def run(self):
            """Run flask api.

            """
            self.api_process.start()

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
            self.notify_callback(KILL_EVENT_NAME)

            shutdown_hook = flask.request.environ.get('werkzeug.server.shutdown')
            if shutdown_hook is not None:
                shutdown_hook()

            return Response(status=200)

        def get_pipe_structure(self):
            """Get the structure of the pipeline with the events its including.

            Returns:
                Dictionary of routines details, and custom events the pipe supported.
                {
                    Routines: [
                        {
                            flow_name: xxx,
                            routine_name: xxx,
                            events: []
                        }
                    ],
                    Events: []
                }
            """
            return self.pipe.get_pipe_structure()

        def routine_execute(self, routine_name, event_name):
            """Execute custom event. Should get request with 'event_name' and with optional keys parameters.

            Returns:
                Status 200 when succeed.

            """

            params = flask.request.json

            if params is not None:
                extra_args = params.get("extra_args", {})
            else:
                extra_args = {}

            self.notify_callback(event_name, specific_routine=routine_name, **extra_args)

            return Response(status=200)

        def routines_execute(self, event_name):
            """Execute custom event. Should get request with 'event_name' and with optional keys parameters.

            Returns:
                Status 200 when succeed.

            """

            params = flask.request.json
            extra_args = params.get("extra_args", {})

            self.notify_callback(event_name, **extra_args)

            return Response(status=200)
