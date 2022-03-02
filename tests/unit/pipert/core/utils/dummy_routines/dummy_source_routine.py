from pipert2 import Data
from pipert2.core.base.routines import FPSRoutine


class DummySourceRoutine(FPSRoutine):

    def __init__(self, name="dummy_start_routine"):
        super(DummySourceRoutine, self).__init__(name=name)
        self.counter = 0

    def main_logic(self, data) -> any:
        self.counter += 1
        data = Data()
        data.additional_data["counter"] = self.counter

        return data

    def setup(self) -> None:
        pass

    def cleanup(self) -> None:
        pass


class DummySourceRoutineException(FPSRoutine):

    def __init__(self):
        super(DummySourceRoutineException, self).__init__("dummy_start_routine")
        self.counter = 0

    def main_logic(self, data) -> any:
        raise Exception

    def setup(self) -> None:
        pass

    def cleanup(self) -> None:
        pass
