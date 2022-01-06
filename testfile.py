import cv2
import time
import logging
import numpy as np
from pipert2.core.base.data import Data
from pipert2.core.base.data.frame_data import FrameData
from pipert2.utils.annotations import class_functions_dictionary
from pipert2.utils.consts import LOG_DATA
from pipert2.utils.logging_module_modifiers import get_socket_logger
from pipert2 import SourceRoutine, DestinationRoutine, Pipe, START_EVENT_NAME, MiddleRoutine
from pipert2.utils.socketio_logger.frame_utils import  create_log_record_of_frame, numpy_frame_to_base64


class Base64Frame(FrameData):
    frame: np.array
    current_frame: int

    def __init__(self, frame, current_frame):
        self.frame = frame
        self.current_frame = current_frame
        self.additional_data = dict()

    def get_frame(self):
        return self.frame


class Source(SourceRoutine):
    events = class_functions_dictionary()

    def __init__(self, name):
        super().__init__(name)
        self.cap = None
        self.current_frame = 0

    @events("SET_OPENCV")
    def set_opencv(self):
        self.cap = cv2.VideoCapture("/home/bina3/seg_2/Record_2020_09_10_11_37_24_short3.mp4")

    def main_logic(self) -> Data:
        ret, frame = self.cap.read()

        if ret:
            self.current_frame += 1
            cv2.putText(frame, f"{self.current_frame}", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36, 255, 12), 1)

            time.sleep(0.05)

            base64_frame = Base64Frame(frame=frame, current_frame=self.current_frame)

            # base64_frame.additional_data['image_base64'] = numpy_frame_to_base64(frame)

            return base64_frame


class MiddleRoutineAir(MiddleRoutine):
    def main_logic(self, data) -> Base64Frame:

        bw = cv2.cvtColor(data.frame, cv2.COLOR_BGR2GRAY)
        cv2.putText(bw, f"{data.current_frame}", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36, 255, 12), 1)

        self._logger.info(create_log_record_of_frame("test image", bw))

        data.additional_data = {
            "one_param": 123,
            "second_param": "I sure it is ok"
        }

        time.sleep(0.1)
        # data.additional_data['image_base64'] = numpy_frame_to_base64(bw)

        data.frame = bw

        return data


class Destination(DestinationRoutine):
    def main_logic(self, data: Data) -> None:
        pass


pipe = Pipe(logger=get_socket_logger("pipe", logging.INFO), auto_pacing_mechanism=True)

src = Source("src")
midd = MiddleRoutineAir("Black White routine")
pipe.create_flow("Flow1", True, src, midd, Destination())

pipe.build()

pipe.notify_event(LOG_DATA, {"Flow1": ['Black White routine']})
pipe.notify_event("SET_OPENCV")
pipe.notify_event(START_EVENT_NAME)

time.sleep(20)

print("Kill")
pipe.join(to_kill=True)
