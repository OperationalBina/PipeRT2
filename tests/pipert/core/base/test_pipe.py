import pytest
from mock import patch, Mock
from pytest_mock import MockerFixture
from src.pipert2.utils.exceptions.floating_routine import FloatingRoutine
from src.pipert2 import MiddleRoutine, DestinationRoutine, SourceRoutine
from src.pipert2.core.base.pipe import Pipe
from src.pipert2.core.base.wire import Wire


@pytest.fixture()
def dummy_pipe():
    with patch('src.pipert2.core.base.pipe.Flow'):
        with patch('src.pipert2.core.base.pipe.EventBoard'):
            pipe = Pipe(network=Mock(), logger=Mock())
            yield pipe


@pytest.fixture()
def dummy_pipe_with_flows(dummy_pipe: Pipe, mocker: MockerFixture):
    FLOW_NAMES = ["f1", "f2", "f3"]

    source_routine = mocker.MagicMock(spec=SourceRoutine)
    source_routine.name = "source"

    middle_routine = mocker.MagicMock(spec=MiddleRoutine)
    middle_routine.name = "middle_routine"

    destination_routine = mocker.MagicMock(spec=DestinationRoutine)
    destination_routine.name = "destination_routine"

    for flow_name in FLOW_NAMES:
        dummy_pipe.create_flow(flow_name, True, source_routine, middle_routine, destination_routine)

    return dummy_pipe, FLOW_NAMES


def test_create_flow_auto_wire_false(dummy_pipe: Pipe):
    FLOW_NAME = "f1"
    routine_mock = Mock()
    dummy_pipe.create_flow(FLOW_NAME, False, routine_mock)

    routine_mock.initialize.assert_called_once()

    assert FLOW_NAME in dummy_pipe.flows


def test_link_link_new_wires_should_add_to_dictionary(dummy_pipe: Pipe, mocker: MockerFixture):
    source_routine = mocker.MagicMock(spec=SourceRoutine)
    source_routine.name = "source"

    middle_routine = mocker.MagicMock(spec=MiddleRoutine)
    middle_routine.name = "middle_routine"

    destination_routine = mocker.MagicMock(spec=DestinationRoutine)
    destination_routine.name = "destination_routine"

    source_to_middle_wire = Wire(source_routine, middle_routine)
    dummy_pipe.link(source_to_middle_wire)

    assert dummy_pipe.wires["source"] == source_to_middle_wire

    middle_to_destination_wire = Wire(middle_routine, destination_routine)
    dummy_pipe.link(middle_to_destination_wire)

    assert dummy_pipe.wires["middle_routine"] == middle_to_destination_wire


def test_link_link_existing_wires_sources_should_override_existing_in_dictionary(dummy_pipe: Pipe, mocker: MockerFixture):
    source_routine = mocker.MagicMock(spec=SourceRoutine)
    source_routine.name = "source"

    middle_routine = mocker.MagicMock(spec=MiddleRoutine)
    middle_routine.name = "middle_routine"

    destination_routine = mocker.MagicMock(spec=DestinationRoutine)
    destination_routine.name = "destination_routine"

    source_to_middle_wire = Wire(source_routine, middle_routine)
    dummy_pipe.link(source_to_middle_wire)

    source_to_destination_wire = Wire(source_routine, destination_routine)
    dummy_pipe.link(source_to_destination_wire)

    assert dummy_pipe.wires["source"] == source_to_destination_wire


def test_build(dummy_pipe_with_flows):
    dummy_pipe_object, flow_names = dummy_pipe_with_flows
    dummy_pipe_object.build()
    assert dummy_pipe_object.flows[flow_names[0]].build.call_count == 3


def test_build_floating_routine_build_raises_error(mocker: MockerFixture):
    pipe = Pipe(network=mocker.MagicMock(), logger=mocker.MagicMock())

    dummy_routine1 = mocker.MagicMock()
    dummy_routine1.name = "r1"

    dummy_routine2 = mocker.MagicMock()
    dummy_routine2.name = "r2"

    dummy_flow1 = mocker.MagicMock()
    dummy_flow1.name = "flow1"
    dummy_flow1.routines = [dummy_routine1, dummy_routine2]

    dummy_routine3 = mocker.MagicMock()
    dummy_routine3.name = "r3"

    dummy_routine4 = mocker.MagicMock()
    dummy_routine4.name = "r4"

    dummy_routine5 = mocker.MagicMock()
    dummy_routine5.name = "r5"

    dummy_flow2 = mocker.MagicMock()
    dummy_flow2.name = "flow2"
    dummy_flow2.routines = [dummy_routine3, dummy_routine4, dummy_routine5]

    pipe.flows = {"flow1": dummy_flow1, "flow2": dummy_flow2}

    pipe.wires = {
        "r1": Wire(source=dummy_routine1, destinations=(dummy_routine2, dummy_routine3,)),
        "r3": Wire(source=dummy_routine3, destinations=(dummy_routine4,)),
    }

    with pytest.raises(FloatingRoutine) as error:
        pipe.build()

    assert "r5" in str(error)


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
