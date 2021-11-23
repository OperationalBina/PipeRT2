import pytest
from collections import deque
from functools import partial
from pipert2 import MiddleRoutine
from pytest_mock import MockerFixture
from pipert2.utils.dummy_object import Dummy
from tests.unit.pipert.core.utils.functions_test_utils import timeout_wrapper
from tests.unit.pipert.core.utils.dummy_routines.dummy_middle_routine import DummyMiddleRoutine, DUMMY_ROUTINE_EVENT, \
    DummyMiddleRoutineException

MAX_TIMEOUT_WAITING = 3


@pytest.fixture()
def dummy_routine(mocker: MockerFixture):
    dummy_routine = DummyMiddleRoutine()
    mock_message_handler = mocker.MagicMock()
    dummy_routine.initialize(mock_message_handler, event_notifier=Dummy())
    return dummy_routine


def test_event_execution(dummy_routine):
    dummy_routine.execute_event(DUMMY_ROUTINE_EVENT)
    assert not dummy_routine.inc


def test_routine_has_registered_events(dummy_routine):
    assert DUMMY_ROUTINE_EVENT.event_name in dummy_routine.get_events()


def test_routine_execution(mocker, dummy_routine):
    main_logic_spy = mocker.spy(dummy_routine, "main_logic")

    does_routine_executed_enough_times_function = \
        partial((lambda spy, expected_counter_value: spy.call_count >= expected_counter_value),
                spy=main_logic_spy,
                expected_counter_value=10)

    assert dummy_routine.stop_event.is_set()

    dummy_routine.start()

    assert not dummy_routine.stop_event.is_set()

    assert timeout_wrapper(func=does_routine_executed_enough_times_function,
                           expected_value=True,
                           timeout_duration=MAX_TIMEOUT_WAITING)

    dummy_routine.stop()

    assert dummy_routine.stop_event.is_set()

    number_of_main_logic_calls = dummy_routine.counter
    message_handler = dummy_routine.message_handler

    assert message_handler.get.call_count == number_of_main_logic_calls
    assert message_handler.put.call_count == number_of_main_logic_calls


def test_routine_execution_catch_exception(mocker, dummy_routine):

    dummy_routine = DummyMiddleRoutineException()
    mock_message_handler = mocker.MagicMock()
    dummy_routine.initialize(mock_message_handler, event_notifier=Dummy())

    assert dummy_routine.stop_event.is_set()

    dummy_routine.start()

    assert not dummy_routine.stop_event.is_set()

    dummy_routine.stop()

    assert dummy_routine.stop_event.is_set()

    message_handler = dummy_routine.message_handler

    assert message_handler.put.call_count == 0


def test_run_main_logic_with_time_measurement_full_duration_queue(mocker: MockerFixture, dummy_routine: MiddleRoutine):

    dummy_routine.durations = deque(maxlen=1)
    dummy_routine.durations.append(1)

    callback = mocker.MagicMock()

    dummy_routine._run_main_logic_with_durations_updating(callback)


def test_update_delay_time(dummy_routine: MiddleRoutine):

    dummy_routine.fps_multiplier = 2

    dummy_routine.update_delay_time(**{"fps": 10})

    assert dummy_routine._fps == 20