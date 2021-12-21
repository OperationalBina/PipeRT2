import time
from pipert2.utils.logging_module_modifiers import get_socket_logger
from pipert2.utils.consts.event_names import START_EVENT_NAME, KILL_EVENT_NAME, LOG_DATA
from pipert2 import Pipe, Wire, QueueNetwork, BasicTransmitter, SourceRoutine, MiddleRoutine, DestinationRoutine, Data


class DummyCount(SourceRoutine):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.count = 0

    def main_logic(self) -> Data:
        data = Data()
        data.additional_data = {"count": self.count}
        self.count += 1
        time.sleep(0.5)

        return data


class DummyMiddle(MiddleRoutine):
    def main_logic(self, data) -> Data:
        data.additional_data["count"] *= 10

        return data


class DummyDest(DestinationRoutine):
    def main_logic(self, data: Data) -> None:
        data_dict = data.additional_data
        if self.adapter is not None:
            self.adapter.info(f"{self.name} Result: ", data=data_dict['count']*10)


def create_test_pipe():
    in_pipe = Pipe(network=QueueNetwork(get_block=True), data_transmitter=BasicTransmitter(),
                   logger=get_socket_logger("pipe", 20), auto_pacing_mechanism=False)

    source = DummyCount()
    middle = DummyMiddle()
    dest = DummyDest()

    in_pipe.create_flow("Test", True, source, middle, dest)

    in_pipe.build()

    return in_pipe


if __name__ == '__main__':
    pipe = create_test_pipe()

    pipe.notify_event(LOG_DATA)
    pipe.notify_event(START_EVENT_NAME)

    time.sleep(5)

    pipe.notify_event(KILL_EVENT_NAME)
