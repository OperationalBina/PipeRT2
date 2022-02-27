from pipert2.core.base.routines import FPSRoutine
from pipert2.core.wrappers.api_wrapper import APIWrapper
from pipert2.utils.annotations import class_functions_dictionary
from pipert2 import Data, Pipe
from pipert2.utils.socketio_logger.socket_logger import get_socket_logger


class Src(FPSRoutine):
    events = class_functions_dictionary()

    def main_logic(self, data) -> Data:
        return Data()

    @events("Hello")
    def hello(self):
        self._logger.info(f"Get to hello in {self.name}")

    @events("Param")
    def param(self, param):
        self._logger.info(f"Param in {self.name}: {param}")


class Dst(FPSRoutine):
    events = class_functions_dictionary()

    def main_logic(self, data: Data) -> None:
        pass

    @events("Hello")
    def hello(self):
        self._logger.info(f"Get to hello in {self.name}")

    @events("Param")
    def param(self, param):
        self._logger.info(f"Param in {self.name}: {param}")

    @events("Dst only")
    def dst(self, param):
        self._logger.info(f"Dst in {self.name}: {param}")


src = Src(name="SRC")
dst = Dst(name="DST")

pipe = Pipe(logger=get_socket_logger("socket", 5))
pipe.create_flow("Flow", True, src, dst)
pipe.build()

api_wrapper = APIWrapper("localhost", 4000, pipe)
api_wrapper.run()
