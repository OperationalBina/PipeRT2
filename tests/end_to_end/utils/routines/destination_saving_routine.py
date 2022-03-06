import multiprocessing as mp
from pipert2 import FPSRoutine, Data
from pipert2.utils.annotations import class_functions_dictionary


class DestinationSavingRoutine(FPSRoutine):
    events = class_functions_dictionary()

    def __init__(self):
        super().__init__()

        manager = mp.Manager()
        self.values = manager.list()

        self.custom_event_notifies = mp.Event()
        self.event_param = mp.Value('i', 0)

    def main_logic(self, data: Data = None) -> Data:
        self.values.append(data.additional_data["val"])

    @events("CUSTOM_EVENT_PARAM")
    def custom_event_with_param(self, param):
        self.custom_event_notifies.set()
        self.event_param.value = param

