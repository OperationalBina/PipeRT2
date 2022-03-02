import time
import multiprocessing as mp
from pipert2 import FPSRoutine, Data
from pipert2.utils.annotations import class_functions_dictionary


class SourceGeneratingRoutine(FPSRoutine):
    events = class_functions_dictionary()

    def __init__(self, data, name="src"):
        super().__init__(name=name)

        self.data_to_iterate = data
        self.indexing = 0
        self.custom_event_notifies = mp.Event()

        self.event_param = mp.Value('i', 0)

    def main_logic(self, data: Data = None) -> Data:
        if self.indexing < len(self.data_to_iterate):
            d = Data()
            d.additional_data = {
                "val": self.data_to_iterate[self.indexing]
            }

            self.indexing += 1
            time.sleep(0.1)

            return d

    @events("CUSTOM_EVENT")
    def custom_event(self):
        self.custom_event_notifies.set()

    @events("CUSTOM_EVENT_PARAM")
    def custom_event_with_param(self, param):
        self.custom_event_notifies.set()
        self.event_param.value = param

    @events("CUSTOM_EVENT_NOTIFY")
    def custom_event_notify_event(self):
        self.custom_event_notifies.set()
        self.notify_event("MIDDLE_EVENT")
