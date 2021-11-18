import time
from pipert2.core.base.data import Data
from pipert2 import SourceRoutine, DestinationRoutine, Pipe, START_EVENT_NAME


class SrcRoutine(SourceRoutine):
    def __init__(self, name):
        super().__init__(name)
        self.counter = 0

    def main_logic(self) -> Data:
        return_value = Data()
        return_value.additional_data = {"a": self.counter}
        self.counter += 1
        time.sleep(1)

        return return_value


class DestRoutine(DestinationRoutine):
    def main_logic(self, data) -> None:
        time.sleep(2)
        print(f"Got {data.additional_data['a']}")


src = SrcRoutine("src")
dst = DestRoutine(name="dst", thread_number=2)

pipe = Pipe()
pipe.create_flow("test", True, src, dst)
pipe.build()

pipe.notify_event(START_EVENT_NAME)

time.sleep(10)

pipe.join(to_kill=True)
