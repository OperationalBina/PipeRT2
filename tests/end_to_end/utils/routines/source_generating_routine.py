import multiprocessing as mp
from pipert2 import FPSRoutine, Data
from pipert2.utils.annotations import class_functions_dictionary


class SourceGeneratingRoutine(FPSRoutine):
    events = class_functions_dictionary()

    def __init__(self, data, name="src"):
        super().__init__(name="src")

        self.data_to_iterate = data
        self.indexing = 0
        self.custom_event_notifies = mp.Event()

    def main_logic(self, data: Data = None) -> Data:
        if self.indexing < len(self.data_to_iterate):
            d = Data()

            d.additional_data = {
                "val": self.data_to_iterate[self.indexing]
            }

            self.indexing += 1

            return d

    @events("CUSTOM_EVENT")
    def custom_event(self):
        self.custom_event_notifies.set()
