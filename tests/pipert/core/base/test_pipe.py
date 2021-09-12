import pytest
from mock import patch, Mock
from src.pipert2.core.base.pipe import Pipe
from src.pipert2.core.base.wire import Wire


@pytest.fixture()
def dummy_pipe():
    with patch('src.pipert2.core.base.pipe.Flow'):
        with patch('src.pipert2.core.base.pipe.EventBoard'):
            pipe = Pipe(network=Mock(), logger=Mock())
            yield pipe


@pytest.fixture()
def dummy_pipe_with_flows(dummy_pipe: Pipe):
    FLOW_NAMES = ["f1", "f2", "f3"]
    routine_mocks = [Mock(), Mock(), Mock()]
    for flow_name, routine_mock in zip(FLOW_NAMES, routine_mocks):
        dummy_pipe.create_flow(flow_name, False, routine_mock)

    return dummy_pipe, FLOW_NAMES


def test_create_flow_auto_wire_false(dummy_pipe: Pipe):
    FLOW_NAME = "f1"
    routine_mock = Mock()
    dummy_pipe.create_flow(FLOW_NAME, False, routine_mock)

    routine_mock.initialize.assert_called_once()

    assert FLOW_NAME in dummy_pipe.flows


def test_create_flow_auto_wire_true(dummy_pipe: Pipe):
    FLOW_NAME = "f1"
    data_transmitter_mock = Mock()
    routine_mocks = [Mock(), Mock(), Mock()]
    dummy_pipe.create_flow(FLOW_NAME, True, *routine_mocks, data_transmitter=data_transmitter_mock)

    for routine_mock in routine_mocks:
        routine_mock.initialize.assert_called_once()

    network_mock: Mock = dummy_pipe.network

    for first_routine_mock, second_routine_mock in zip(routine_mocks, routine_mocks[1:]):
        network_mock.link.assert_any_call(source=first_routine_mock, destinations=(second_routine_mock,),
                                          transmit=data_transmitter_mock.transmit(),
                                          receive=data_transmitter_mock.receive())


def test_link(dummy_pipe: Pipe):
    routine_mocks = [Mock(), Mock(), Mock()]
    data_transmitter_mock = Mock()
    wires = []

    for first_routine_mock, second_routine_mock in zip(routine_mocks, routine_mocks[1:]):
        wires.append(Wire(source=first_routine_mock, destinations=(second_routine_mock,),
                          data_transmitter=data_transmitter_mock))

    dummy_pipe.link(*wires)

    network_mock: Mock = dummy_pipe.network

    for first_routine_mock, second_routine_mock in zip(routine_mocks, routine_mocks[1:]):
        network_mock.link.assert_any_call(source=first_routine_mock, destinations=(second_routine_mock,),
                                          transmit=data_transmitter_mock.transmit(),
                                          receive=data_transmitter_mock.receive())


def test_build(dummy_pipe_with_flows):
    dummy_pipe_object, flow_names = dummy_pipe_with_flows
    dummy_pipe_object.build()
    assert dummy_pipe_object.flows[flow_names[0]].build.call_count == 3


def test_notify_event(dummy_pipe: Pipe):
    EVENT_NAME = "Recover"
    EVENT_PARAMS = {"State": True}
    dummy_pipe.notify_event(EVENT_NAME, **EVENT_PARAMS)
    event_board_mock: Mock = dummy_pipe.event_board
    event_board_mock.notify_event.assert_called_with(EVENT_NAME, **EVENT_PARAMS)


def test_join(dummy_pipe_with_flows):
    dummy_pipe_object, flow_names = dummy_pipe_with_flows
    dummy_pipe_object.join()
    assert dummy_pipe_object.flows[flow_names[0]].join.call_count == 3
