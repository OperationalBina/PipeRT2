from pytest_mock import MockerFixture
from pipert2.utils.dummy_object import Dummy
from pipert2.utils.consts.routine_types import GENERATOR_ROUTINE
from pipert2.core.base.routines.extended_run_factory import get_runner_for_type
from tests.unit.pipert.core.utils.dummy_routines.dummy_source_routine import DummySourceRoutine, \
    DummySourceRoutineException

MAX_TIMEOUT_WAITING = 3


def test_routine_execution(mocker: MockerFixture):
    dummy_routine = DummySourceRoutine()
    dummy_routine.extended_run_strategy = get_runner_for_type(GENERATOR_ROUTINE)
    mock_message_handler = mocker.MagicMock()
    dummy_routine.initialize(mock_message_handler, event_notifier=Dummy())

    dummy_routine.start()

    assert not dummy_routine.stop_event.is_set()

    dummy_routine.stop()

    assert dummy_routine.stop_event.is_set()

    number_of_main_logic_calls = dummy_routine.counter
    message_handler = dummy_routine.message_handler

    assert message_handler.put.call_count == number_of_main_logic_calls
    assert message_handler.get.call_count == 0


def test_throws_exception(mocker: MockerFixture):
    dummy_routine = DummySourceRoutineException()
    dummy_routine.extended_run_strategy = get_runner_for_type(GENERATOR_ROUTINE)
    mock_message_handler = mocker.MagicMock()
    mock_message_handler.get.get_data.side_effect = Exception()
    dummy_routine.initialize(mock_message_handler, event_notifier=Dummy())

    dummy_routine.start()

    assert not dummy_routine.stop_event.is_set()

    dummy_routine.stop()

    assert dummy_routine.stop_event.is_set()

    message_handler = dummy_routine.message_handler

    assert message_handler.put.call_count == 0
    assert message_handler.get.call_count == 0
