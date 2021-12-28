import logging

import cv2
import time
import base64
from pipert2.utils.logging_module_modifiers import get_socket_logger
from pipert2 import SourceRoutine, Data, dataclass, DestinationRoutine, Pipe, START_EVENT_NAME


@dataclass
class Base64Frame(Data):
    base64: str


class Source(SourceRoutine):
    def __init__(self, name):
        super().__init__(name)
        self.cap = cv2.VideoCapture("/home/bina3/seg_2/Record_2020_09_10_11_37_24_short3.mp4")
        self.current_frame = 0

    def main_logic(self) -> Data:
        ret, frame = self.cap.read()

        if ret:
            self.current_frame += 1

            cv2.putText(frame, f"{self.current_frame}", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36, 255, 12), 1)
            ret, encoded_frame = cv2.imencode('.jpg', frame)
            jpg_as_base64 = base64.b64encode(encoded_frame)
            as_str = f"{jpg_as_base64}"[2:]
            as_str = as_str[:len(as_str) - 1]

            time.sleep(0.1)

            return Base64Frame(base64=as_str)


class Destination(DestinationRoutine):
    def main_logic(self, data: Data) -> None:
        pass


pipe = Pipe(logger=get_socket_logger("pipe", logging.INFO), auto_pacing_mechanism=True)

src = Source("src")

pipe.create_flow("Flow1", True, src, Destination())
pipe.build()

src.message_handler.send_data = True

pipe.notify_event(START_EVENT_NAME)
time.sleep(5)
pipe.join(to_kill=True)
