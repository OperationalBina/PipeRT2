import pytest

from src.pipert2.utils.dummy_object import Dummy
from utils.dummy_routine import DummyRoutine, DUMMY_ROUTINE_EVENT_NAME
from utils.functions_test_utils import timeout_wrapper
from functools import partial

MAX_TIMEOUT_WAITING = 3


@pytest.fixture()
def dummy_routine():
    return DummyRoutine(name="Dummy", message_handler=Dummy(), logger=Dummy())


def test_event_trigger(dummy_routine):
    dummy_routine.trigger_event(DUMMY_ROUTINE_EVENT_NAME)
    assert not dummy_routine.inc


def test_routine_has_registered_events(dummy_routine):
    assert DUMMY_ROUTINE_EVENT_NAME in dummy_routine.events.all


def test_routine_execution(dummy_routine):
    assert dummy_routine.stop_event.is_set()
    dummy_routine.start()
    assert not dummy_routine.stop_event.is_set()

    does_routine_executed_enough_times_function = \
        partial((lambda routine, expected_counter_value: routine.counter >= expected_counter_value),
                routine=dummy_routine,
                expected_counter_value=10)

    assert timeout_wrapper(does_routine_executed_enough_times_function, True, timeout_duration=MAX_TIMEOUT_WAITING)

    dummy_routine.stop()
    assert dummy_routine.stop_event.is_set()
