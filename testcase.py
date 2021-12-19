import json
import time
import logging
from pipert2.core.base.data import Data
from pipert2 import SourceRoutine, MiddleRoutine, DestinationRoutine, Pipe, START_EVENT_NAME, KILL_EVENT_NAME
from pipert2.utils.logging_module_modifiers import get_socket_logger
from pipert2.utils.consts import UPDATE_FPS_NAME
import socketio


class Src(SourceRoutine):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.counter = 0
        self.start_time = time.time()
        # self._logger = logger_

    def main_logic(self) -> Data:
        self.counter += 1
        data = Data()
        data.additional_data = {
            "src": self.counter
        }

        self._logger.info(f"Count in SRC {self.counter}")
        time.sleep(0.05)
        # print(f"current time: {time.time() - self.start_time}, count: {self.counter}")

        return data


class Mid(MiddleRoutine):
    def main_logic(self, data) -> Data:
        self._logger.info(f"Count in MID {data.additional_data['src']}")
        return data


class Destination(DestinationRoutine):
    def main_logic(self, data: Data) -> None:
        self._logger.info(f"Count in DEST {data.additional_data['src']}")
        pass


def create_pipe_and_test_socket_handler():
    src = Src()
    mid = Mid()
    dst = Destination()

    pipe = Pipe(logger=get_socket_logger("Pipe", 5, "http://localhost:3000/api/socketio"), auto_pacing_mechanism=False)
    pipe.create_flow("f1", True, src, mid, dst)
    # logger.info("Message")
    pipe.build()

    pipe.notify_event(START_EVENT_NAME)

    time.sleep(3)

    # print(" --- Update fps")
    # pipe.notify_event(UPDATE_FPS_NAME, fps=100)

    time.sleep(5)

    pipe.notify_event(KILL_EVENT_NAME)
    pipe.join()


# def socket_handler_in_processes():
#     import multiprocessing, logging.handlers
#
#     my_logger = logger
#     # my_logger = logging.getLogger("new_handler")
#     # logger.setLevel(logging.INFO)
#     # my_logger.addHandler(logging.handlers.SocketHandler(host="http://localhost:3000/api/socketio", port=3000))
#
#     def log_process_func():
#         counter = 1
#         process_name = multiprocessing.current_process().name
#         # _logger = my_logger.getChild(process_name)
#         # _logger.addHandler(SocketHandler("http://localhost:3000/api/socketio"))
#         # _logger.setLevel(logging.INFO)
#
#         while counter < 5:
#             time.sleep(1)
#             # _logger.info(f"process: {process_name} - {counter}")
#             my_logger.info(f"process: {process_name} - {counter}")
#             counter += 1
#
#     p1 = multiprocessing.Process(target=log_process_func)
#     p2 = multiprocessing.Process(target=log_process_func)
#
#     p1.start()
#     p2.start()
#
#     p1.join()
#     p2.join()
#

if __name__ == '__main__':
    # socket_handler_in_processes()
    create_pipe_and_test_socket_handler()
