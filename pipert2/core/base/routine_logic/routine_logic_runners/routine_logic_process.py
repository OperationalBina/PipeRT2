from typing import Callable
import multiprocessing as mp
from pipert2.utils.dummy_object import Dummy
from pipert2.core.base.routine_logic.routine_logic_runner import RoutineLogicRunner


class RoutineLogicProcess(RoutineLogicRunner):
    def __init__(self, routine_logic: Callable):
        self.routine_logic = routine_logic
        self.runner: mp.Process = Dummy()

    def start(self):
        """Starts the routine logic in a process.

        """

        self.runner = mp.Process(target=self.routine_logic)
        self.runner.start()

    def join(self):
        """Join the routine logic process.

        """

        self.runner.join()
