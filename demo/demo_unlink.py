import os
import time
import numpy as np
from pipert2.core.base.data import FrameData
from pipert2 import SourceRoutine, Data, MiddleRoutine, DestinationRoutine, Pipe, START_EVENT_NAME, STOP_EVENT_NAME, \
    Wire
from pipert2.utils.consts import UNLINK


class Frame(FrameData):
    def __init__(self, frame, frame_number):
        self.frame = frame
        self.frame_number = frame_number

    def get_frame(self) -> np.array:
        return self.frame


class Src(SourceRoutine):

    def __init__(self, name):
        super().__init__(name)
        self.cap = None
        self.count = 1
        self.frame = np.zeros((500, 700, 3))

    def main_logic(self) -> FrameData:
        self._logger.info("Sending frame")
        frame = Frame(self.frame, self.count)
        self.count += 1

        time.sleep(1)

        return frame


class Mid(MiddleRoutine):
    def main_logic(self, data: Frame) -> Frame:
        self._logger.info(f"Get to {self.name}")
        return data


class Dst(DestinationRoutine):
    def main_logic(self, data: Data) -> None:
        self._logger.info("Get to destination")


video_path = os.environ.get("VIDEO_PATH")

src = Src(name="SRC")
mid1 = Mid(name="MID1")
mid2 = Mid(name="MID2")
dst = Dst(name="DST")

pipe = Pipe()

pipe.create_flow("Flow1", False, src, mid1, dst)
pipe.create_flow("Flow2", False, mid2)

pipe.link(Wire(source=src, destinations=(mid1, mid2)))
pipe.link(Wire(source=mid1, destinations=(dst,)))
pipe.link(Wire(source=mid2, destinations=(dst,)))

pipe.build()

pipe.notify_event(START_EVENT_NAME)

time.sleep(5)
pipe.notify_event(UNLINK, specific_routine="SRC", unlink_routine_name="MID1")
time.sleep(5)

pipe.notify_event(STOP_EVENT_NAME)
