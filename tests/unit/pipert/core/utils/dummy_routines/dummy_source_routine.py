from pipert2.core.base.routines import SourceRoutine


class DummySourceRoutine(SourceRoutine):
    
    def __init__(self, name="dummy_start_routine"):
        super(DummySourceRoutine, self).__init__(name=name)
        self.counter = 0
    
    def main_logic(self) -> any:
        self.counter += 1
        return self.counter

    def setup(self) -> None:
        pass

    def cleanup(self) -> None:
        pass


class DummySourceRoutineException(SourceRoutine):

    def __init__(self):
        super(DummySourceRoutineException, self).__init__("dummy_start_routine")
        self.counter = 0

    def main_logic(self) -> any:
        raise Exception

    def setup(self) -> None:
        pass

    def cleanup(self) -> None:
        pass