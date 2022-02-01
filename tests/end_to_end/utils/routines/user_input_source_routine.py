from multiprocessing import Event

from pipert2.core.base.routines import FPSRoutine
from tests.unit.pipert.core.utils.events_utils import STOP_EVENT


class UserInputSourceRoutine(FPSRoutine):

    def __init__(self, name="dummy_start_routine", data_to_send=None):
        super(UserInputSourceRoutine, self).__init__(name=name)
        self.data = data_to_send
        self.does_data_sent = Event()
        self.index = 0

    def main_logic(self, data) -> any:
        if self.index < len(self.data):
            self.index += 1
            return self.data[self.index - 1]
        self.does_data_sent.set()
        self.notify_event(STOP_EVENT.event_name, {self.flow_name: [self.name]})

    def setup(self) -> None:
        self.does_data_sent.clear()

    def cleanup(self) -> None:
        pass
