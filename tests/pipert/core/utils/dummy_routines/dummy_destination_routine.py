from src.pipert2.core.handlers.message_handler import MessageHandler
from src.pipert2.core.base.routines.destination_routine import DestinationRoutine


class DummyDestinationRoutine(DestinationRoutine):
    
    def __init__(self):
        super(DummyDestinationRoutine, self).__init__(name="dummy_end_routine")
        self.counter = 0

    def main_logic(self, data) -> None:
        self.counter += 1

    def setup(self) -> None:
        pass

    def cleanup(self) -> None:
        pass
