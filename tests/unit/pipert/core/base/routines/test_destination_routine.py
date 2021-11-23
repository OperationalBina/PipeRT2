import pytest
from pytest_mock import MockerFixture
from pipert2.utils.dummy_object import Dummy
from tests.unit.pipert.core.utils.dummy_routines.dummy_destination_routine import DummyDestinationRoutine, \
    DummyDestinationRoutineException

MAX_TIMEOUT_WAITING = 3


@pytest.fixture()
def dummy_routine(mocker: MockerFixture):
    dummy_routine = DummyDestinationRoutine()
    mock_message_handler = mocker.MagicMock()
    dummy_routine.initialize(mock_message_handler, event_notifier=Dummy())
    return dummy_routine


def test_routine_execution(dummy_routine):

    dummy_routine.start()

    assert not dummy_routine.stop_event.is_set()

    dummy_routine.stop()

    assert dummy_routine.stop_event.is_set()

    number_of_main_logic_calls = dummy_routine.counter
    message_handler = dummy_routine.message_handler

    assert message_handler.get.call_count == number_of_main_logic_calls
    assert message_handler.put.call_count == 0


def test_routine_execution_catch_exception(mocker, dummy_routine):

    dummy_routine = DummyDestinationRoutineException()
    mock_message_handler = mocker.MagicMock()
    dummy_routine.initialize(mock_message_handler, event_notifier=Dummy())

    assert dummy_routine.stop_event.is_set()

    dummy_routine.start()

    assert not dummy_routine.stop_event.is_set()

    dummy_routine.stop()

    assert dummy_routine.stop_event.is_set()

    message_handler = dummy_routine.message_handler

    assert message_handler.put.call_count == 0