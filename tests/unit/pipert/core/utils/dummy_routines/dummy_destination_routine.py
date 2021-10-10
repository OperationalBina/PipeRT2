from pipert2.core.base.routines import DestinationRoutine


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
