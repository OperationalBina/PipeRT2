import os
import time
import numpy as np
from pipert2.core.base.data import FrameData
from pipert2 import Data, Pipe, START_EVENT_NAME, STOP_EVENT_NAME, \
    Wire
from pipert2.core.base.routines import FPSRoutine


class Frame(FrameData):
    def __init__(self, frame, frame_number):
        self.frame = frame
        self.frame_number = frame_number

    def get_frame(self) -> np.array:
        return self.frame


class Src(FPSRoutine):

    def __init__(self, name):
        super().__init__(name)
        self.cap = None
        self.count = 1
        self.frame = np.zeros((500, 700, 3))

    def main_logic(self, data) -> FrameData:
        self._logger.info("Sending frame")
        frame = Frame(self.frame, self.count)
        self.count += 1

        return frame


class Mid(FPSRoutine):
    def main_logic(self, data: Frame) -> Frame:
        self._logger.info("Get to middle")
        return data


class Dst(FPSRoutine):
    def main_logic(self, data: Data) -> None:
        self._logger.info("Get to destination")


video_path = os.environ.get("VIDEO_PATH")

src = Src(name="SRC")
mid = Mid(name="MID")
dst = Dst(name="DST")

pipe = Pipe()
pipe.create_flow("Flow1", True, src, mid)
pipe.create_flow("Flow2", False, dst)

pipe.link(Wire(source=mid, destinations=(dst,)))
pipe.build()

pipe.notify_event(START_EVENT_NAME)

time.sleep(10)

pipe.notify_event(STOP_EVENT_NAME)
pipe.join(True)
