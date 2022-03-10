from json.tool import main
import time
from pipert2 import FPSRoutine
from pipert2 import Pipe, QueueNetwork
from pipert2.utils.consts.event_names import START_EVENT_NAME, KILL_EVENT_NAME


class GenerateData(FPSRoutine):

    def main_logic(self) -> dict:
        return {
            "value": "example"
        }


class PrintResult(FPSRoutine):

    def main_logic(self, data: dict) -> None:
        print(data["value"])


# Creating the pipe.
example_pipe = Pipe()

# Create an instance of each routine.
generate_data_routine = GenerateData()
print_result_routine = PrintResult()

# Create a flow with the required routines.
example_pipe.create_flow("example_flow", True,
                         generate_data_routine, print_result_routine)

# Build the pipe.
example_pipe.build()

# Run the pipe.
example_pipe.notify_event(START_EVENT_NAME)

# Let the pipeline run for 10 seconds before shutdown
time.sleep(10)

# Force all the pipe's routines stop.
example_pipe.notify_event(KILL_EVENT_NAME)
