import time
import multiprocessing as mp
from pipert2.core.base.data import Data
from pipert2 import SourceRoutine, DestinationRoutine, Pipe, START_EVENT_NAME


class SrcRoutine(SourceRoutine):
    def __init__(self):
        super().__init__()
        self.counter = 0

    def main_logic(self) -> Data:
        return_value = Data()
        return_value.additional_data = {'counter': self.counter}
        self.counter += 1

        time.sleep(1)

        return return_value


class DestRoutine(DestinationRoutine):
    def __init__(self, thread_number):
        super().__init__("routine_name", thread_number)
        self.values = mp.Manager().list()

    def main_logic(self, data) -> None:
        time.sleep(2)

        self.values.append(
            data.additional_data['counter']
        )


def test_pipe_with_scaling_routine_get_all_inputs():
    src_routine = SrcRoutine()
    dst_routine = DestRoutine(thread_number=2)

    pipe = Pipe()
    pipe.create_flow("flow", True, src_routine, dst_routine)

    pipe.build()

    pipe.notify_event(START_EVENT_NAME)
    time.sleep(4)
    pipe.join(to_kill=True)

    assert (list(dst_routine.values) == [0, 1, 2, 3] or list(dst_routine.values) == [0, 1, 2])
