import time
import cv2
from src.pipert2.core.base.routine import Routine


class OpenCVDisplayFrame(Routine):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.counter_frame_fps = 1
        self.last_frame_time = time.time()
        self.fps = 0

    def main_logic(self, data):
        image = data["frame"]
        self.fps = self.calculate_fps()
        image = cv2.putText(image, self.fps, (0, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
        cv2.imshow('video', image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            pass

    def setup(self):
        self.counter_frame_fps = 0

    def cleanup(self):
        cv2.destroyAllWindows()

    def calculate_fps(self):
        self.counter_frame_fps += 1

        fps = self.fps
        frame_time = time.time()

        if frame_time - self.last_frame_time >= 1:
            fps = str(round(self.counter_frame_fps / (frame_time - self.last_frame_time), 2))
            self.counter_frame_fps = 0
            self.last_frame_time = time.time()

        return fps
