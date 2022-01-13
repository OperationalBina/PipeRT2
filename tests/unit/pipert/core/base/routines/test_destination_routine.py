import pytest
from functools import partial
from pytest_mock import MockerFixture
from pipert2.core.base.data import Data
from pipert2.utils.dummy_object import Dummy
from pipert2.utils.exceptions.main_logic_not_exist_error import MainLogicNotExistError
from tests.unit.pipert.core.utils.dummy_data import DummyData
from tests.unit.pipert.core.utils.functions_test_utils import message_generator, timeout_wrapper
from tests.unit.pipert.core.utils.dummy_routines.dummy_destination_routine import DummyDestinationRoutine, \
    DummyDestinationRoutineException

MAX_TIMEOUT_WAITING = 3


@pytest.fixture()
def dummy_routine(mocker: MockerFixture):
    dummy_routine = DummyDestinationRoutine()
    mock_message_handler = mocker.MagicMock()
    mock_message_handler.get.side_effect = message_generator(Data)
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


def test_destination_routine_receive_unexpected_data_type_expects_error_log(mocker: MockerFixture, dummy_routine):
    message_handler = dummy_routine.message_handler
    message_handler.get.side_effect = message_generator(DummyData)

    logger_mock = mocker.MagicMock()
    dummy_routine.set_logger(logger_mock)

    does_routine_executed_enough_times_function = \
        partial((lambda mock: mock.error.call_count > 0),
                mock=logger_mock)

    dummy_routine.start()
    did_not_timeout = timeout_wrapper(func=does_routine_executed_enough_times_function,
                                      expected_value=True,
                                      timeout_duration=MAX_TIMEOUT_WAITING)
    dummy_routine.stop()

    assert did_not_timeout

    assert type(logger_mock.error.call_args[0][0]) == MainLogicNotExistError


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
