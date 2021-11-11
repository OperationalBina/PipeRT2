from pipert2.core.base.data import Data
from pipert2.utils.method_data import Method
from pipert2.core.base.routines import MiddleRoutine

DUMMY_ROUTINE_EVENT = Method("Change")


class DummyMiddleRoutine(MiddleRoutine):

    def __init__(self, counter=0, **kwargs):
        super().__init__(**kwargs)
        self.counter = counter
        self.inc = True

    @MiddleRoutine.main_logics(Data)
    def main_logic(self, data: Data):
        # print(self.counter)
        if self.inc:
            self.counter += 1
        else:
            self.counter -= 1

        data.additional_data = {"value": self.counter}
        return data

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

    @MiddleRoutine.main_logics(Data)
    def main_logic(self, data: Data):
        raise Exception()

    def setup(self) -> None:
        self.counter = 0

    def cleanup(self) -> None:
        pass

    @MiddleRoutine.events(DUMMY_ROUTINE_EVENT.event_name)
    def change_logic(self):
        self.inc = not self.inc
