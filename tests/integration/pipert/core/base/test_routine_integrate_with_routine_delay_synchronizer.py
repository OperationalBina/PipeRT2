import time
import pytest
from pipert2 import DestinationRoutine
from pytest_mock import MockerFixture
from pipert2.core.base.routine_synchronizers.routine_delay_synchronizer import RoutineDelaySynchronizer


class DummyDestinationRoutine(DestinationRoutine):
    def __init__(self):
        super().__init__()
        self.main_logic_calls_counter = 0

    def main_logic(self, data: dict) -> None:
        self.main_logic_calls_counter = self.main_logic_calls_counter + 1


DURATION_TIME_TEST = 1
FPS_ACCURACY_RATE = 0.9


@pytest.fixture
def destination_routine_and_fps(mocker: MockerFixture):

    delay_time = mocker.MagicMock()
    delay_time.value = 0.01

    fps = DURATION_TIME_TEST / delay_time.value

    synchronizer = RoutineDelaySynchronizer(mocker.MagicMock(), mocker.MagicMock(), mocker.MagicMock())
    synchronizer.delay_time = delay_time

    test_routine = DummyDestinationRoutine()
    test_routine.initialize(mocker.MagicMock(), mocker.MagicMock())
    test_routine.routine_delay_synchronizer = synchronizer

    return test_routine, fps


def test_start_routine_for_two_seconds_should_run_main_logic_about_required_fps(destination_routine_and_fps):
    test_routine, fps = destination_routine_and_fps

    start_stop_routine(test_routine)

    assert fps >= test_routine.main_logic_calls_counter >= fps * FPS_ACCURACY_RATE


def test_start_routine_for_two_second_should_not_call_get_queue_more_then_fps(destination_routine_and_fps):
    test_routine, fps = destination_routine_and_fps

    start_stop_routine(test_routine)

    assert fps >= test_routine.message_handler.get.call_count >= fps * FPS_ACCURACY_RATE


def start_stop_routine(routine):
    routine.start()

    time.sleep(DURATION_TIME_TEST)
    routine.stop_event.set()
