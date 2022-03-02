import os
import cv2
import time
import numpy as np
from pipert2 import Data, Pipe
from pipert2.core.base.data import FrameData
from pipert2.core.base.routines import FPSRoutine
from pipert2.core.wrappers.api_wrapper import APIWrapper
from pipert2.utils.socketio_logger.socket_logger import get_socket_logger


class Frame(FrameData):
    def __init__(self, frame, frame_number):
        self.frame = frame
        self.frame_number = frame_number

    def get_frame(self) -> np.array:
        return self.frame


class Src(FPSRoutine):

    def __init__(self, name, video_path):
        super().__init__(name)
        self.video_path = video_path

        self.cap = None
        self.count = 1

    def setup(self) -> None:
        self.cap = cv2.VideoCapture(self.video_path)

    def main_logic(self, data) -> FrameData:
        ret, img = self.cap.read()

        img = cv2.putText(img, f"{self.count}", (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 255, 0), 1, cv2.LINE_AA)

        if ret:
            frame = Frame(img, self.count)
            self.count += 1
        else:
            frame = None

        time.sleep(0.05)

        return frame


class Mid(FPSRoutine):
    def main_logic(self, data: Frame) -> Frame:
        data.frame = cv2.cvtColor(data.frame, cv2.COLOR_BGR2GRAY)

        return data


class Dst(FPSRoutine):
    def main_logic(self, data: Data) -> None:
        self._logger.info("Get to destination")


video_path = os.environ.get("VIDEO_PATH")

src = Src(name="SRC", video_path=video_path)
mid = Mid(name="MID")
dst = Dst(name="DST")

pipe = Pipe(logger=get_socket_logger("socket", 5))
pipe.create_flow("Flow", True, src, mid, dst)
pipe.build()

api_wrapper = APIWrapper("localhost", 4000, pipe)
api_wrapper.run()
