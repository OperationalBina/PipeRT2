import time
import random
import multiprocessing as mp
from pipert2 import FPSRoutine, Data, STOP_EVENT_NAME
from pipert2.utils.annotations import class_functions_dictionary


class MiddleBufferingRoutine(FPSRoutine):
    events = class_functions_dictionary()

    def __init__(self, buffer, limit, name, sleeping_time=0):
        super().__init__(name)
        self.custom_event_notifies = mp.Event()
        self.middle_event_notifies = mp.Event()
        self.buffer = buffer
        self.limit = limit
        self.index = 0
        self.sleeping_time = sleeping_time
        self.event_param = mp.Value('i', 0)

    def main_logic(self, data: Data = None) -> Data:
        if self.sleeping_time > 0:
            time.sleep(self.sleeping_time)

        data.additional_data["val"] += self.buffer
        self.index += 1

        if self.index == self.limit:
            self.notify_event(STOP_EVENT_NAME, specific_routine=self.name)

        time.sleep(random.randint(1, 10) / 10)
        return data

    @events("CUSTOM_EVENT")
    def custom_event(self):
        self.custom_event_notifies.set()

    @events("MIDDLE_EVENT")
    def middle_event(self):
        self.middle_event_notifies.set()

    @events("CUSTOM_EVENT_PARAM")
    def custom_event_with_param(self, param):
        self.custom_event_notifies.set()
        self.event_param.value = param
