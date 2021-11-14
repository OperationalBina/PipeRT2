import time
import multiprocessing as mp
from pipert2 import DestinationRoutine
from pipert2.utils.consts import NULL_FPS


class DestinationCounterRoutine(DestinationRoutine):
    def __init__(self, fps, name):
        super().__init__(name)
        self.routine_fps = fps
        self.counter = mp.Value('i', 0)

        self.prev_run_time = None
        self.estimate_fps = mp.Value('f', 0.0)

    def main_logic(self, data) -> None:
        fps = self._const_fps.value if not self._const_fps.value == NULL_FPS else self._fps.value

        if fps is not None:
            self.estimate_fps.value = self._fps.value

        self.counter.value = self.counter.value + 1
        time.sleep(1 / self.routine_fps)
