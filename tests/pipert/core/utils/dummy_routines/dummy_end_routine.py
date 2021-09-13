from src.pipert2.core.handlers.message_handler import MessageHandler
from src.pipert2.core.base.routines.end_routine import EndRoutine


class DummyEndRoutine(EndRoutine):
    
    def __init__(self):
        super(DummyEndRoutine, self).__init__("dummy_end_routine")
        self.counter = 0

    def main_logic(self, param) -> None:
        self.counter += 1

    def setup(self) -> None:
        pass

    def cleanup(self) -> None:
        pass
