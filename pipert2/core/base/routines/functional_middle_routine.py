from pipert2 import MiddleRoutine
from typing import Callable


class FunctionalMiddleRoutine(MiddleRoutine):
    """A Middle Routine Class for stateless routines

    """
    def __init__(self, func: Callable = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.logic = func

    def main_logic(self, data):
        return self.logic(data)

    def setup(self, *args, **kwargs):
        pass

    def cleanup(self, *args, **kwargs):
        pass
