import time
from pipert2 import DestinationRoutine
from pytest_mock import MockerFixture
from pipert2.core.base.routine_delay_synchronizer import RoutineDelaySynchronizer


class DummyDestinationRoutine(DestinationRoutine):
    def __init__(self):
        super().__init__()
        self.main_logic_calls_counter = 0

    def main_logic(self, data: dict) -> None:
        self.main_logic_calls_counter = self.main_logic_calls_counter + 1


def test_start_routine_for_two_seconds_should_run_main_logic_about_required_fps(mocker: MockerFixture):
    duration_test_time = 2

    delay_time = mocker.MagicMock()
    delay_time.value = 0.01

    fps = duration_test_time / delay_time.value

    synchronizer = RoutineDelaySynchronizer(mocker.MagicMock(), mocker.MagicMock(), mocker.MagicMock())
    synchronizer.delay_time = delay_time

    test_routine = DummyDestinationRoutine()
    test_routine.initialize(mocker.MagicMock(), mocker.MagicMock())
    test_routine.routine_delay_synchronizer = synchronizer

    test_routine.stop_event.set()

    test_routine.start()

    time.sleep(duration_test_time)

    test_routine.stop_event.set()

    assert fps >= test_routine.main_logic_calls_counter >= fps / 2
