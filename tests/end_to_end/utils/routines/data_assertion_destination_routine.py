from multiprocessing import Event
from pipert2.utils.consts.event_names import KILL_EVENT_NAME
from pipert2.core.base.routines.destination_routine import DestinationRoutine


class DataAssertionDestinationRoutine(DestinationRoutine):
    """"Routine used to assert that data coming to routine is equal to the expected one.
    When the data is not equal the routine will set the does_data_equal flag and kill the pipe.
    When all of the expected data is reached the routine will kill the pipe as well.

    """

    ERROR_KEY = "error"

    def __init__(self, data_to_expect: list, shared_process_dict: dict,  name="dummy_end_routine"):
        super().__init__(name=name)
        self.data_to_expect = data_to_expect
        self.is_data_equals_to_expected_data_flag = Event()
        self.error_dict = shared_process_dict
        self.error_dict[self.ERROR_KEY] = "No Error"

    def main_logic(self, data) -> None:
        if data not in self.data_to_expect:
            self._set_error(f"Got unexpected Data: {data}")
            self.is_data_equals_to_expected_data_flag.set()
            self.notify_event(KILL_EVENT_NAME)
        else:
            self.data_to_expect.remove(data)
            if len(self.data_to_expect) == 0:
                self.notify_event(KILL_EVENT_NAME)

    def setup(self) -> None:
        self.is_data_equals_to_expected_data_flag.clear()

    def cleanup(self) -> None:
        if len(self.data_to_expect) != 0:
            self._set_error(f"Didn't get all of the expected datas, Expected to get also: {self.data_to_expect}")
            self.is_data_equals_to_expected_data_flag.set()

    def get_error(self):
        return self.error_dict[self.ERROR_KEY]

    def _set_error(self, error_message):
        self.error_dict[self.ERROR_KEY] = error_message
