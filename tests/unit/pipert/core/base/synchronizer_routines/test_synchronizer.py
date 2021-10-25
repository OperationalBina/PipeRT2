import pytest
from pytest_mock import MockerFixture
from pipert2 import SourceRoutine, DestinationRoutine, MiddleRoutine, Wire
from pipert2.core.base.synchronize_routines.synchronizer import Synchronizer


@pytest.fixture
def base_synchronizer(mocker: MockerFixture):
    return Synchronizer(mocker.MagicMock(), mocker.MagicMock(), mocker.MagicMock(), [], mocker.MagicMock())


def test_build_routines_graph(base_synchronizer, mocker: MockerFixture):

    source1_routine = mocker.MagicMock(spec=SourceRoutine)
    source1_routine.name = "source1"

    source2_routine = mocker.MagicMock(spec=SourceRoutine)
    source2_routine.name = "source2"

    middle1_routine = mocker.MagicMock(spec=MiddleRoutine)
    middle1_routine.name = "m1"

    middle2_routine = mocker.MagicMock(spec=MiddleRoutine)
    middle2_routine.name = "m2"

    destination_routine = mocker.MagicMock(spec=DestinationRoutine)
    destination_routine.name = "destination"

    wires = [
        Wire(source=source1_routine, destinations=(middle1_routine, middle2_routine,)),
        Wire(source=source2_routine, destinations=(middle1_routine,)),
        Wire(source=middle1_routine, destinations=(destination_routine,)),
        Wire(source=middle2_routine, destinations=(destination_routine,))
    ]

    base_synchronizer.wires = wires
    base_synchronizer.build_routines_graph()

    routine_graphs = base_synchronizer.routines_graph

    synchronize1_source = routine_graphs['source1']

    assert len(synchronize1_source.nodes) == 2
    assert [node.name for node in synchronize1_source.nodes] == ["m1", "m2"]
    assert [node.nodes[0].name for node in synchronize1_source.nodes] == ["destination", "destination"]

    synchronize1_source = routine_graphs['source2']

    assert len(synchronize1_source.nodes) == 1
    assert [node.name for node in synchronize1_source.nodes] == ["m1"]
    assert [node.nodes[0].name for node in synchronize1_source.nodes] == ["destination"]

