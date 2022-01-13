import time

from pipert2 import SourceRoutine, Data, MiddleRoutine, DestinationRoutine, Pipe


class Src(SourceRoutine):
    def main_logic(self) -> Data:
        data = Data()

        time.sleep(2)

        return data


class Mid(MiddleRoutine):
    def main_logic(self, data) -> Data:

        time.sleep(2)

        return data


class Dst(DestinationRoutine):
    def main_logic(self, data):

        time.sleep(2)
        print("End")


src = Src()
mid = Mid()
dst = Dst()

pipe = Pipe(run_rpc_cli=True)
pipe.run_rpc_server("tcp://127.0.0.1:1234")

