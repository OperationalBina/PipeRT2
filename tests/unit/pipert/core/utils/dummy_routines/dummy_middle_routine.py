from pipert2.core.base.routines import MiddleRoutine
from pipert2.utils.method_data import Method

DUMMY_ROUTINE_EVENT = Method("Change")


class DummyMiddleRoutine(MiddleRoutine):

    def __init__(self, counter=0, **kwargs):
        super().__init__(**kwargs)
        self.counter = counter
        self.inc = True

    def main_logic(self, data):
        if self.inc:
            self.counter += 1
        else:
            self.counter -= 1

        return {"value": self.counter}

    def setup(self) -> None:
        self.counter = 0

    def cleanup(self) -> None:
        pass

    @MiddleRoutine.events(DUMMY_ROUTINE_EVENT.event_name)
    def change_logic(self):
        self.inc = not self.inc


class DummyMiddleRoutineException(MiddleRoutine):

    def __init__(self, counter=0, **kwargs):
        super().__init__(**kwargs)
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


class DummyMiddleRoutineWithCustomDurationTime(DummyMiddleRoutine):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.duration = 5

    def _extended_run(self) -> float:
        return self.duration
