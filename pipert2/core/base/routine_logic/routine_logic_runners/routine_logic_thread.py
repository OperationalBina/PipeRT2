import threading as th
from typing import Callable
from pipert2.utils.dummy_object import Dummy
from pipert2.core.base.routine_logic.routine_logic_runner import RoutineLogicRunner


class RoutineLogicThread(RoutineLogicRunner):
    def __init__(self, routine_logic: Callable):
        self.routine_logic = routine_logic
        self.runner: th.Thread = Dummy()

    def start(self):
        """Starts the routine logic in a thread.

        """

        self.runner = th.Thread(target=self.routine_logic)
        self.runner.start()

    def join(self):
        """Join the routine logic thread.

        """

        self.runner.join()
