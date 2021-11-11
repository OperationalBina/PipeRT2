from pipert2.core.base.routines import DestinationRoutine
from tests.unit.pipert.core.utils.dummy_routines.dummy_middle_routine import DUMMY_ROUTINE_EVENT


class DummyDestinationRoutine(DestinationRoutine):
    
    def __init__(self, name="dummy_end_routine"):
        super(DummyDestinationRoutine, self).__init__(name=name)
        self.counter = 0

    def main_logic(self, data) -> None:
        self.counter += 1

    def setup(self) -> None:
        pass

    def cleanup(self) -> None:
        pass


class DummyDestinationRoutineException(DestinationRoutine):

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

    @DestinationRoutine.events(DUMMY_ROUTINE_EVENT.event_name)
    def change_logic(self):
        self.inc = not self.inc