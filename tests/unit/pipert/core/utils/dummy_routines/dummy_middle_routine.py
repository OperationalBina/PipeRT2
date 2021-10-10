from src.pipert2.core.base.routines.middle_routine import MiddleRoutine
from src.pipert2.utils.method_data import Method

DUMMY_ROUTINE_EVENT = Method("Change")


class DummyMiddleRoutine(MiddleRoutine):

    def __init__(self, counter=0, **kwargs):
        super().__init__(flow_name='dummy', **kwargs)
        self.counter = counter
        self.inc = True

    def main_logic(self, data):
        if self.inc:
            self.counter += 1
        else:
            self.counter -= 1

    def setup(self) -> None:
        self.counter = 0

    def cleanup(self) -> None:
        pass

    @MiddleRoutine.events(DUMMY_ROUTINE_EVENT.event_name)
    def change_logic(self):
        self.inc = not self.inc


class DummyMiddleRoutineException(MiddleRoutine):

    def __init__(self, counter=0, **kwargs):
        super().__init__(flow_name='dummy', **kwargs)
        self.counter = counter
        self.inc = True

    def main_logic(self, data):
        raise Exception()

    def setup(self) -> None:
        self.counter = 0

    def cleanup(self) -> None:
        pass

    @MiddleRoutine.events(DUMMY_ROUTINE_EVENT.event_name)
    def change_logic(self):
        self.inc = not self.inc
