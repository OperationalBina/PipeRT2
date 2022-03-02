import time
from pipert2 import Pipe, BasicTransmitter, Data, START_EVENT_NAME
from pipert2.core.base.routines import FPSRoutine


class DummyCount(FPSRoutine):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.count = 0

    def main_logic(self, data) -> Data:
        data = Data()
        time.sleep(0.5)
        data.additional_data = {"count": self.count}
        self._logger.info(self.count)
        self.count += 1

        return data


class DummyMiddle(FPSRoutine):
    def main_logic(self, data) -> Data:
        data_dict = data.additional_data
        self._logger.info(data_dict["count"])

        return data


class DummyDest(FPSRoutine):
    def main_logic(self, data: Data) -> None:
        self._logger.info('msg recieved')


def create_test_pipe():
    in_pipe = Pipe(data_transmitter=BasicTransmitter(), auto_pacing_mechanism=True)

    source = DummyCount()
    middle = DummyMiddle()
    dest = DummyDest()

    in_pipe.create_flow("Test", True, source, middle, dest)

    in_pipe.build()

    return in_pipe


if __name__ == '__main__':
    pipe = create_test_pipe()

    pipe.notify_event(START_EVENT_NAME)

    time.sleep(10)

    pipe.join(to_kill=True)
