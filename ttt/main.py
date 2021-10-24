import time
from pipert2 import Pipe, SourceRoutine, DestinationRoutine, START_EVENT_NAME, STOP_EVENT_NAME, KILL_EVENT_NAME


class SourceR(SourceRoutine):
    def main_logic(self) -> dict:
        time.sleep(0.2)

        return {
            "value": 62727
        }


class DestinationR(DestinationRoutine):
    def main_logic(self, data: dict) -> None:
        time.sleep(0.01)


pipe = Pipe()

r1 = SourceR(name="sourceR")
r2 = DestinationR(name="destR")

pipe.create_flow("Flow1", True, r1, r2)

pipe.build()

pipe.notify_event(START_EVENT_NAME)

time.sleep(4)

pipe.notify_event(KILL_EVENT_NAME)
pipe.join()
