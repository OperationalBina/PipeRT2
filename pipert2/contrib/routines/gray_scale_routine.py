import cv2
from pipert2.core.base.routines.middle_routine import MiddleRoutine


class GrayScaleRoutine(MiddleRoutine):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def main_logic(self, data):
        self._logger.info("Test")
        frame = data["frame"]
        data["frame"] = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        return data

    def setup(self):
        pass

    def cleanup(self):
        pass