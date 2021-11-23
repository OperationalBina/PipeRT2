import time
import multiprocessing as mp
from pipert2 import SourceRoutine
from pipert2.utils.consts import NULL_FPS


class SourceCounterRoutine(SourceRoutine):
    def __init__(self, fps, name):
        super().__init__(name)
        self.routine_fps = fps
        self.counter = mp.Value('i', 0)

        self.prev_run_time = None
        self.estimate_fps = mp.Value('f', NULL_FPS)

    def main_logic(self) -> dict:

        fps = self._const_fps if not self._const_fps == NULL_FPS else self._fps

        if fps is not None:
            self.estimate_fps.value = fps

        self.counter.value = self.counter.value + 1
        time.sleep(1 / self.routine_fps)

        return {
            'test': 'test'
        }
