import time

from demo.const import RPC_ENDPOINT
from pipert2.utils.consts.event_names import START_EVENT_NAME, STOP_EVENT_NAME
from pipert2 import Pipe, BasicTransmitter, SourceRoutine, MiddleRoutine, DestinationRoutine, Data


class DummyCount(SourceRoutine):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.count = 0

    def main_logic(self) -> Data:
        data = Data()
        time.sleep(0.5)
        data.additional_data = {"count": self.count}
        self.count += 1
        print(self.count)

        return data


class DummyMiddle(MiddleRoutine):
    def main_logic(self, data) -> Data:
        data_dict = data.additional_data
        data_dict["count"] *= 10

        return data


class DummyDest(DestinationRoutine):
    def main_logic(self, data: Data) -> None:
        data_dict = data.additional_data
        # self.message_handler.logger.info(data_dict["count"] * 10)


def create_test_pipe():
    in_pipe = Pipe(data_transmitter=BasicTransmitter(), auto_pacing_mechanism=False, run_cli=True,
                   rpc_args={'endpoint': RPC_ENDPOINT})

    source = DummyCount()
    middle = DummyMiddle()
    dest = DummyDest()

    in_pipe.create_flow("Test", True, source, middle, dest)

    in_pipe.build()

    return in_pipe


if __name__ == '__main__':
    pipe = create_test_pipe()
    pipe.notify_event(START_EVENT_NAME)
    # pipe.notify_event(STOP_EVENT_NAME)
    # pipe.join(to_kill=True)
