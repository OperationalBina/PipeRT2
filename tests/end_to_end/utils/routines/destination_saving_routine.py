from multiprocessing import Manager
from pipert2 import FPSRoutine, Data


class DestinationSavingRoutine(FPSRoutine):
    def __init__(self):
        super().__init__()

        manager = Manager()
        self.values = manager.list()

    def main_logic(self, data: Data = None) -> Data:
        self.values.append(data.additional_data["val"])


destination = DestinationSavingRoutine()
da = Data()
da.additional_data["val"] = 123

destination.main_logic(da)
da.additional_data["val"] = 1234

destination.main_logic(da)

print(destination.values)
