import pytest
from pytest_mock import MockerFixture
from unittest.mock import call, patch
from src.pipert2.core.base.flow import Flow
from src.pipert2.utils.consts.event_names import START_EVENT_NAME, STOP_EVENT_NAME, KILL_EVENT_NAME
from src.pipert2.utils.method_data import Method
from tests.pipert.core.utils.events_utils import EVENT1_NAME

FIRST_ROUTINE_NAME = "R1"
SECOND_ROUTINE_NAME = "R2"


@pytest.fixture()
def dummy_start_event(mocker: MockerFixture):
    TEST_METHOD = mocker.MagicMock()
    TEST_METHOD.event_name = START_EVENT_NAME
    TEST_METHOD.is_flow_valid.return_value = True
    TEST_METHOD.is_contain_routines.return_value = False

    return TEST_METHOD


@pytest.fixture()
def dummy_stop_event(mocker: MockerFixture):
    TEST_METHOD = mocker.MagicMock()
    TEST_METHOD.event_name = STOP_EVENT_NAME
    TEST_METHOD.is_flow_valid.return_value = True
    TEST_METHOD.is_contain_routines.return_value = False

    return TEST_METHOD


@pytest.fixture()
def dummy_kill_event(mocker: MockerFixture):
    TEST_METHOD = mocker.MagicMock()
    TEST_METHOD.event_name = KILL_EVENT_NAME
    TEST_METHOD.is_flow_valid.return_value = True
    TEST_METHOD.is_contain_routines.return_value = False

    return TEST_METHOD


@pytest.fixture()
def dummy_event1(mocker: MockerFixture):
    TEST_METHOD = mocker.MagicMock()
    TEST_METHOD.event_name = EVENT1_NAME
    TEST_METHOD.is_flow_valid.return_value = True
    TEST_METHOD.is_contain_routines.return_value = False

    return TEST_METHOD


@pytest.fixture()
def patcher_stop_event(dummy_stop_event):
    with patch('src.pipert2.core.base.flow.Method') as mock:
        mock.return_value = dummy_stop_event
        yield mock


@pytest.fixture()
def dummy_flow_with_two_routines(mocker: MockerFixture, dummy_start_event, dummy_event1, dummy_kill_event):
    event_board_mocker = mocker.MagicMock()
    event_handler_mocker = mocker.MagicMock()
    event_handler_mocker.wait.side_effect = [dummy_start_event, dummy_event1, dummy_kill_event]
    event_board_mocker.get_event_handler.return_value = event_handler_mocker

    first_routine_mocker = mocker.MagicMock()
    first_routine_mocker.name = FIRST_ROUTINE_NAME

    second_routine_mocker = mocker.MagicMock()
    second_routine_mocker.name = SECOND_ROUTINE_NAME

    logger_mocker = mocker.MagicMock()
    logger_mocker.getChild.return_value = mocker.MagicMock()

    dummy_flow = Flow(name="Flow1",
                      event_board=event_board_mocker,
                      logger=logger_mocker,
                      routines=[first_routine_mocker, second_routine_mocker])

    return dummy_flow


@pytest.fixture()
def dummy_method_without_specific_flow(mocker: MockerFixture):
    TEST_METHOD = mocker.MagicMock()
    TEST_METHOD.is_flow_valid.return_value = True
    TEST_METHOD.is_contain_routines.return_value = False

    return TEST_METHOD


@pytest.fixture()
def dummy_method_with_specific_flow_and_routines(mocker: MockerFixture):
    TEST_METHOD = mocker.MagicMock()
    TEST_METHOD.is_flow_valid.return_value = True
    TEST_METHOD.is_contain_routines.return_value = True
    TEST_METHOD.routines_by_flow = {"Flow1": [SECOND_ROUTINE_NAME]}

    return TEST_METHOD


def test_run(mocker, dummy_flow_with_two_routines: Flow, dummy_start_event, patcher_stop_event, dummy_stop_event,
             dummy_event1):
    start_event_callback_mock = mocker.MagicMock()
    dummy_flow_with_two_routines.get_events()[START_EVENT_NAME] = {start_event_callback_mock}

    stop_event_callback_mock = mocker.MagicMock()
    dummy_flow_with_two_routines.get_events()[STOP_EVENT_NAME] = {stop_event_callback_mock}

    routine = dummy_flow_with_two_routines.routines[FIRST_ROUTINE_NAME]

    dummy_flow_with_two_routines.run()

    assert routine.execute_event.call_count == 3
    assert routine.execute_event.call_args_list == [call(dummy_start_event), call(dummy_event1), call(dummy_stop_event)]

    start_event_callback_mock.assert_called_once()
    stop_event_callback_mock.assert_called_once()


def test_execute_event(dummy_flow_with_two_routines: Flow, dummy_method_without_specific_flow: Method):

    dummy_flow_with_two_routines.execute_event(dummy_method_without_specific_flow)
    routine_mocker = dummy_flow_with_two_routines.routines[FIRST_ROUTINE_NAME]

    routine_mocker.execute_event.assert_called_with(dummy_method_without_specific_flow)


def test_execute_all_routine_in_specific_flow(dummy_flow_with_two_routines: Flow,
                                              dummy_method_without_specific_flow: Method):

    dummy_flow_with_two_routines.execute_event(dummy_method_without_specific_flow)
    first_routine_mocker = dummy_flow_with_two_routines.routines[FIRST_ROUTINE_NAME]
    second_routine_mocker = dummy_flow_with_two_routines.routines[SECOND_ROUTINE_NAME]

    first_routine_mocker.execute_event.assert_called_with(dummy_method_without_specific_flow)
    second_routine_mocker.execute_event.assert_called_with(dummy_method_without_specific_flow)


def test_execute_specific_routine(dummy_flow_with_two_routines: Flow,
                                  dummy_method_with_specific_flow_and_routines: Method):

    dummy_flow_with_two_routines.execute_event(dummy_method_with_specific_flow_and_routines)
    first_routine_mocker = dummy_flow_with_two_routines.routines[FIRST_ROUTINE_NAME]
    second_routine_mocker = dummy_flow_with_two_routines.routines[SECOND_ROUTINE_NAME]

    assert not first_routine_mocker.execute_event.called
    second_routine_mocker.execute_event.assert_called_with(dummy_method_with_specific_flow_and_routines)


def test_not_execute_flows_routines(dummy_flow_with_two_routines: Flow,
                                    dummy_method_with_specific_flow_and_routines: Method):

    dummy_method_with_specific_flow_and_routines = Method(event_name=START_EVENT_NAME,
                                                          routines_by_flow={"Flow7": [SECOND_ROUTINE_NAME]})

    dummy_flow_with_two_routines.execute_event(dummy_method_with_specific_flow_and_routines)
    first_routine_mocker = dummy_flow_with_two_routines.routines[FIRST_ROUTINE_NAME]
    second_routine_mocker = dummy_flow_with_two_routines.routines[SECOND_ROUTINE_NAME]

    assert not first_routine_mocker.execute_event.called
    assert not second_routine_mocker.execute_event.called
