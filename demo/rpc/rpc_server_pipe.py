import time

from pipert2.core.base.routines import FPSRoutine
from pipert2.core.wrappers.rpc_pipe_wrapper import RPCPipeWrapper
from utlis import load_rpc_endpoint
from pipert2 import Pipe, BasicTransmitter, Data


class DummyCount(FPSRoutine):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.count = 0

    def main_logic(self, data) -> Data:
        data = Data()
        time.sleep(0.5)
        data.additional_data = {"count": self.count}
        self.count += 1
        print(self.count)

        return data


class DummyMiddle(FPSRoutine):
    def main_logic(self, data) -> Data:
        data_dict = data.additional_data
        data_dict["count"] *= 10

        return data


class DummyDest(FPSRoutine):
    def main_logic(self, data: Data) -> None:
        data_dict = data.additional_data


def create_test_pipe():
    rpc_pipe = Pipe(data_transmitter=BasicTransmitter(), auto_pacing_mechanism=False)
    rpc_server = RPCPipeWrapper(rpc_pipe)
    rpc_server.run_rpc_server(endpoint="tcp://127.0.0.1:1234")

    source = DummyCount()
    middle = DummyMiddle()
    dest = DummyDest()

    rpc_pipe.create_flow("Test", True, source, middle, dest)

    rpc_pipe.build()

    return rpc_pipe


if __name__ == '__main__':
    pipe = create_test_pipe()
