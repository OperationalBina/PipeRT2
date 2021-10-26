import time
import pytest
from mock import call
from pytest_mock import MockerFixture
from pipert2.core.base.synchronize_routines.routines_synchronizer import RoutinesSynchronizer
from pipert2.core.base.synchronize_routines.synchronizer_node import SynchronizerNode


@pytest.fixture
def base_synchronizer(mocker: MockerFixture):
    return RoutinesSynchronizer(mocker.MagicMock(), mocker.MagicMock(), mocker.MagicMock(), [], mocker.MagicMock())


def test_update_delay_iteration_small_fps_in_node(base_synchronizer, mocker: MockerFixture):

    notify_func = mocker.MagicMock()
    base_synchronizer.notify_callback = notify_func

    d1 = SynchronizerNode(name="d1", fps=3, nodes=[], notify_delay_time_callback=notify_func)
    d2 = SynchronizerNode(name="d2", fps=9, nodes=[], notify_delay_time_callback=notify_func)

    c = SynchronizerNode(name="c", fps=10, nodes=[d1, d2], notify_delay_time_callback=notify_func)
    b = SynchronizerNode(name="b", fps=30, nodes=[c], notify_delay_time_callback=notify_func)

    a1 = SynchronizerNode(name="a1", fps=15, nodes=[b], notify_delay_time_callback=notify_func)
    a2 = SynchronizerNode(name="a2", fps=10, nodes=[b], notify_delay_time_callback=notify_func)

    base_synchronizer.routines_graph = {
        "a1": a1,
        "a2": a2
    }

    base_synchronizer.update_delay_iteration()

    notify_arg_list = notify_func.call_args_list

    assert call("d1", 3) in notify_arg_list
    assert call("d2", 9) in notify_arg_list
    assert call("c", 9) in notify_arg_list
    assert call("b", 9) in notify_arg_list
    assert call("a1", 9) in notify_arg_list
    assert call("a2", 9) in notify_arg_list


def test_update_delay_iteration_small_fps_in_crossroad(base_synchronizer, mocker: MockerFixture):

    notify_func = mocker.MagicMock()
    base_synchronizer.notify_callback = notify_func

    d1 = SynchronizerNode(name="d1", fps=30, nodes=[], notify_delay_time_callback=notify_func)
    d2 = SynchronizerNode(name="d2", fps=9, nodes=[], notify_delay_time_callback=notify_func)

    c = SynchronizerNode(name="c", fps=10, nodes=[d1, d2], notify_delay_time_callback=notify_func)
    b = SynchronizerNode(name="b", fps=3, nodes=[c], notify_delay_time_callback=notify_func)

    a1 = SynchronizerNode(name="a1", fps=15, nodes=[b], notify_delay_time_callback=notify_func)
    a2 = SynchronizerNode(name="a2", fps=2, nodes=[b], notify_delay_time_callback=notify_func)

    base_synchronizer.routines_graph = {
        "a1": a1,
        "a2": a2
    }

    base_synchronizer.update_delay_iteration()

    notify_arg_list = notify_func.call_args_list

    assert call("d1", 3) in notify_arg_list
    assert call("d2", 3) in notify_arg_list
    assert call("c", 3) in notify_arg_list
    assert call("b", 3) in notify_arg_list
    assert call("a1", 3) in notify_arg_list
    assert call("a2", 2) in notify_arg_list


def test_update_delay_iteration_small_fps_in_source(base_synchronizer, mocker: MockerFixture):

    notify_func = mocker.MagicMock()
    base_synchronizer.notify_callback = notify_func

    d1 = SynchronizerNode(name="d1", fps=30, nodes=[], notify_delay_time_callback=notify_func)
    d2 = SynchronizerNode(name="d2", fps=9, nodes=[], notify_delay_time_callback=notify_func)

    c = SynchronizerNode(name="c", fps=10, nodes=[d1, d2], notify_delay_time_callback=notify_func)
    b = SynchronizerNode(name="b", fps=30, nodes=[c], notify_delay_time_callback=notify_func)

    a1 = SynchronizerNode(name="a1", fps=2, nodes=[b], notify_delay_time_callback=notify_func)

    base_synchronizer.routines_graph = {
        "a1": a1
    }

    base_synchronizer.update_delay_iteration()

    notify_arg_list = notify_func.call_args_list

    assert call("d1", 2) in notify_arg_list
    assert call("d2", 2) in notify_arg_list
    assert call("c", 2) in notify_arg_list
    assert call("b", 2) in notify_arg_list
    assert call("a1", 2) in notify_arg_list
