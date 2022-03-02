import time
import random
import multiprocessing as mp
from pipert2 import FPSRoutine, Data, STOP_EVENT_NAME
from pipert2.utils.annotations import class_functions_dictionary


class MiddleBufferingRoutine(FPSRoutine):
    events = class_functions_dictionary()

    def __init__(self, buffer, limit, name, is_running):
        super().__init__(name)
        self.custom_event_notifies = mp.Event()
        self.buffer = buffer
        self.limit = limit
        self.index = 0
        self.is_running = is_running

    def main_logic(self, data: Data = None) -> Data:
        print(f"Buffer {self.buffer}, Get: {data}")

        if not self.is_running:
            time.sleep(3)

        data.additional_data["val"] += self.buffer
        self.index += 1

        if self.index == self.limit:
            print("Notify stop")
            self.notify_event(STOP_EVENT_NAME, specific_routine=self.name)

        time.sleep(random.randint(1, 10) / 10)
        return data

    @events("CUSTOM_EVENT")
    def custom_event(self):
        self.custom_event_notifies.set()
