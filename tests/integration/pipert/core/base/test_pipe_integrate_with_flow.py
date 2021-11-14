import os
import pytest
import signal
from pipert2.core import Flow
from pytest_mock import MockerFixture
from pipert2 import Pipe, SourceRoutine, Wire, DestinationRoutine

FIRST_FLOW_NAME = "first_flow_name"
SECOND_FLOW_NAME = "second_flow_name"


@pytest.fixture()
def pipe_with_multiple_flows(mocker: MockerFixture) -> Pipe:

    pipe = Pipe()

    source_routine = mocker.MagicMock(spec=SourceRoutine)
    source_routine.name = "source"
    source_routine.message_handler = mocker.MagicMock()

    destination_routine = mocker.MagicMock(spec=DestinationRoutine)
    destination_routine.name = "destination"
    destination_routine.message_handler = mocker.MagicMock()

    pipe.wires[(FIRST_FLOW_NAME, "source")] = Wire(source=source_routine,
                                                   destinations=(destination_routine,),
                                                   data_transmitter=mocker.MagicMock())

    first_flow = Flow(name=FIRST_FLOW_NAME,
                      routines=[source_routine],
                      logger=mocker.MagicMock(),
                      event_board=mocker.MagicMock())

    second_flow = Flow(name=SECOND_FLOW_NAME,
                       routines=[destination_routine],
                       logger=mocker.MagicMock(),
                       event_board=mocker.MagicMock())

    pipe.flows[FIRST_FLOW_NAME] = first_flow
    pipe.flows[SECOND_FLOW_NAME] = second_flow

    pipe.event_board = mocker.MagicMock()

    return pipe


def test_build_multiple_flows_should_create_flow_process(pipe_with_multiple_flows: Pipe):

    pipe_with_multiple_flows.build()

    for flow in pipe_with_multiple_flows.flows.values():
        assert flow.event_loop_process is not None
        os.kill(flow.event_loop_process.pid, signal.SIGTERM)


def test_join_multiple_flows_should_join_processes(pipe_with_multiple_flows: Pipe, mocker: MockerFixture):

    flow_processes = []

    for flow in pipe_with_multiple_flows.flows.values():
        flow.event_loop_process = mocker.MagicMock()
        flow_processes.append(flow.event_loop_process)

    pipe_with_multiple_flows.join()
