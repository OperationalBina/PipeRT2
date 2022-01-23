from pipert2.core.wrappers.api_wrapper import APIWrapper
from pipert2.utils.annotations import class_functions_dictionary
from pipert2 import SourceRoutine, Data, DestinationRoutine, Pipe
from pipert2.utils.logging_module_modifiers import get_socket_logger


class Src(SourceRoutine):
    events = class_functions_dictionary()

    def main_logic(self) -> Data:
        return Data()

    @events("Hello")
    def hello(self):
        print(f"Hello in {self.name}")

    @events("Param")
    def param(self, param):
        print(f"Param in {self.name}: {param}")


class Dst(DestinationRoutine):
    events = class_functions_dictionary()

    def main_logic(self, data: Data) -> None:
        pass

    @events("Hello")
    def hello(self):
        print(f"Hello in {self.name}")

    @events("Param")
    def param(self, param):
        print(f"Param in {self.name}: {param}")

    @events("Dst only")
    def dst(self, param):
        print(f"Dst in {self.name}: {param}")


src = Src(name="SRC")
dst = Dst(name="DST")

pipe = Pipe(logger=get_socket_logger("socket", 5))
pipe.create_flow("Flow", True, src, dst)
pipe.build()

pipe.notify_event("Hello")

api_wrapper = APIWrapper("localhost", 4000, pipe)
api_wrapper.run()
