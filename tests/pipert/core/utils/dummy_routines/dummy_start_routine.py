from src.pipert2.core.base.routines.start_routine import StartRoutine


class DummyStartRoutine(StartRoutine):
    
    def __init__(self):
        super(DummyStartRoutine, self).__init__("dummy_start_routine")
        self.counter = 0
    
    def main_logic(self) -> any:
        self.counter += 1
        return self.counter

    def setup(self) -> None:
        pass

    def cleanup(self) -> None:
        pass