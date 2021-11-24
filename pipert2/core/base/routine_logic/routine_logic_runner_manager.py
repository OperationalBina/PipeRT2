from typing import Callable
from functools import partial
from pipert2.core.base.routine_logic.routine_logic_runners.routine_logic_thread import RoutineLogicThread
from pipert2.core.base.routine_logic.routine_logic_runners.routine_logic_process import RoutineLogicProcess


class RoutineLogicRunnerManager:
    def __init__(self, to_run_in_process: bool, routine_logic: Callable):
        self.to_run_in_process = to_run_in_process
        routine_logic = partial(routine_logic)

        if self.to_run_in_process:
            self.runner = RoutineLogicProcess(routine_logic)
        else:
            self.runner = RoutineLogicThread(routine_logic)

    def is_running_in_process(self):
        """Check if runner is process runner.

        Returns:
            True if runner is process, False if thread.
        """

        return self.to_run_in_process

    def start(self):
        """Start the runner.

        """

        self.runner.start()

    def join(self):
        """Join the runner.

        """

        self.runner.join()
