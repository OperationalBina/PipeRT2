import time
import multiprocessing as mp
from pipert2 import SourceRoutine


class SourceCounterRoutine(SourceRoutine):
    def __init__(self, fps, name):
        super().__init__(name)
        self.routine_fps = fps
        self.counter = mp.Value('i', 0)

    def main_logic(self) -> dict:
        self.counter.value = self.counter.value + 1

        time.sleep(1 / self.routine_fps)

        return {
            'test': 'test'
        }
