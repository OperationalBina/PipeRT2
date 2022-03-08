import time
import multiprocessing as mp
from pipert2.core.base.routines.fps_routine import FPSRoutine
from pipert2.utils.consts.synchronise_routines import NULL_FPS


class SourceCounterRoutine(FPSRoutine):
    def __init__(self, fps, name):
        super().__init__(name)
        self.routine_fps = fps
        self.counter = mp.Value('i', 0)

        self.prev_run_time = None
        self.estimate_fps = mp.Value('f', NULL_FPS)

    def main_logic(self, data) -> dict:

        fps = self._const_fps if not self._const_fps == NULL_FPS else self._fps

        if fps is not None:
            self.estimate_fps.value = fps

        self.counter.value = self.counter.value + 1
        time.sleep(1 / self.routine_fps)

        return {
            'test': 'test'
        }
