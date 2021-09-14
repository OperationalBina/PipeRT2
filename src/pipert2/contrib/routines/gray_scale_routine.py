import cv2
from src.pipert2.core.base.routine import Routine


class GrayScaleRoutine(Routine):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def main_logic(self, data):
        frame = data["frame"]
        data["frame"] = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        return data

    def setup(self):
        pass
    
    def cleanup(self):
        pass
