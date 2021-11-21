import threading
from pipert2.core.base.routine_runner import RoutineRunner


class ThreadRunner(RoutineRunner):

    def __init__(self):
        self.routine_thread = None

    def create_runner(self, callable):
        self.routine_thread = threading.Thread(target=callable)

    def start(self):
        self.routine_thread.start()

    def join(self):
        self.routine_thread.join()
