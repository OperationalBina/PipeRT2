import time

import pytest
from pytest_mock import MockerFixture
from pipert2.core.base.routine_synchronizers.routine_delay_synchronizer import RoutineDelaySynchronizer


DURATION_TEST = 1
MAXIMUM_RUNNING_ROUTINE_TIME = 0.2
DUMMY_SHORT_LOGIC_DURATION = 0.01
DUMMY_LONG_LOGIC_DURATION = 1
ACCURACY_RATE = 0.9


@pytest.fixture
def routine_delay_synchronizer(mocker: MockerFixture):
    routine_delay_synchronizer = RoutineDelaySynchronizer(0.010, mocker.MagicMock(), mocker.MagicMock())

    routine_delay_synchronizer.logic_duration_time_routines = {
        "r1": 0.1,
        "r2": MAXIMUM_RUNNING_ROUTINE_TIME
    }

    routine_delay_synchronizer.delay_time.value = MAXIMUM_RUNNING_ROUTINE_TIME

    return routine_delay_synchronizer


def dummy_logic_shorter_duration():
    time.sleep(DUMMY_SHORT_LOGIC_DURATION)


def dummy_logic_longer_duration():
    time.sleep(DUMMY_LONG_LOGIC_DURATION)


def test_update_delay_time_should_set_delay_time_as_maximum_value(routine_delay_synchronizer):
    routine_delay_synchronizer.stop_event.clear()
    routine_delay_synchronizer.start_notify_process()

    time.sleep(DURATION_TEST)
    routine_delay_synchronizer.kill_synchronized_process()

    assert routine_delay_synchronizer.delay_time.value == MAXIMUM_RUNNING_ROUTINE_TIME


def test_run_synchronized_with_shorter_duration_should_delay(routine_delay_synchronizer):
    start_time = time.time()
    routine_delay_synchronizer.run_synchronized(dummy_logic_shorter_duration, "test")
    end_time = time.time()

    expected_time = (DUMMY_SHORT_LOGIC_DURATION + MAXIMUM_RUNNING_ROUTINE_TIME)
    actual_time = end_time - start_time

    assert 1 > actual_time/expected_time > ACCURACY_RATE


def test_run_synchronized_with_long_duration_should_not_delay(routine_delay_synchronizer):
    start_time = time.time()
    routine_delay_synchronizer.run_synchronized(dummy_logic_longer_duration, "test")
    end_time = time.time()

    expected_time = DUMMY_LONG_LOGIC_DURATION
    actual_time = end_time - start_time

    assert 1 > expected_time / actual_time > ACCURACY_RATE
