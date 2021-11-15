import time
import multiprocessing as mp
from pipert2 import SourceRoutine, MiddleRoutine
from pipert2.utils.consts import NULL_FPS


class MiddleCounterRoutine(MiddleRoutine):
    def __init__(self, fps, name):
        super().__init__(name)
        self.routine_fps = fps
        self.counter = mp.Value('i', 0)

        self.prev_run_time = None
        self.estimate_fps = mp.Value('f', NULL_FPS)

    def main_logic(self, data) -> dict:
        if self._fps is not None:
            self.estimate_fps.value = self._fps

        self.counter.value = self.counter.value + 1
        time.sleep(1 / self.routine_fps)

        return {
            'test': 'test'
        }
