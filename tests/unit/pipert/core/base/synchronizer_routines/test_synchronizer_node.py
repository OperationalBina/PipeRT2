from pytest_mock import MockerFixture
from pipert2.core.base.synchronise_routines.synchroniser_node import SynchroniserNode


def test_update_fps_by_nodes_required_fps_in_leaf_should_change_source_fps_to_leaf():
    d1 = SynchroniserNode(routine_name="d1", flow_name="f1", nodes=[])
    d1.curr_fps = 3
    d1.original_fps = 3

    d2 = SynchroniserNode(routine_name="d2", flow_name="f1", nodes=[])
    d2.curr_fps = 9
    d2.original_fps = 9

    c = SynchroniserNode(routine_name="c", flow_name="f1", nodes=[d1, d2])
    c.curr_fps = 10
    c.original_fps = 10

    b = SynchroniserNode(routine_name="b", flow_name="f1", nodes=[c])
    b.curr_fps = 30
    b.original_fps = 30

    b.update_fps_by_nodes()

    assert b.curr_fps == 9
    assert c.curr_fps == 9


def test_update_fps_by_nodes_required_fps_in_crossroad_should_change_source_fps_to_leaf():
    d1 = SynchroniserNode(routine_name="d1", flow_name="f1", nodes=[])
    d1.curr_fps = 7

    d2 = SynchroniserNode(routine_name="d2", flow_name="f1", nodes=[])
    d2.curr_fps = 9

    c = SynchroniserNode(routine_name="c", flow_name="f1", nodes=[d1, d2])
    c.curr_fps = 5

    b = SynchroniserNode(routine_name="b", flow_name="f1", nodes=[c])
    b.curr_fps = 30

    b.update_fps_by_nodes()

    assert b.curr_fps == 5
    assert c.curr_fps == 5
    assert d1.curr_fps == 7
    assert d2.curr_fps == 9


def test_update_fps_by_father_required_fps_in_source_change_all_nodes():
    d1 = SynchroniserNode(routine_name="d1", flow_name="f1", nodes=[])
    d1.curr_fps = 7
    d1.original_fps = 7

    d2 = SynchroniserNode(routine_name="d2", flow_name="f1", nodes=[])
    d2.curr_fps = 9
    d2.original_fps = 9

    c = SynchroniserNode(routine_name="c", flow_name="f1", nodes=[d1, d2])
    c.curr_fps = 15
    c.original_fps = 15

    b = SynchroniserNode(routine_name="b", flow_name="f1", nodes=[c])
    b.curr_fps = 3
    b.original_fps = 3

    b.update_fps_by_fathers()

    assert b.curr_fps == 3
    assert c.curr_fps == 3
    assert d1.curr_fps == 3
    assert d2.curr_fps == 3


def test_update_fps_by_father_required_fps_in_crossroad_should_change_the_nodes_in_the_hierarchy():
    d1 = SynchroniserNode(routine_name="d1", flow_name="f1", nodes=[])
    d1.curr_fps = 7
    d1.original_fps = 7

    d2 = SynchroniserNode(routine_name="d2", flow_name="f1", nodes=[])
    d2.curr_fps = 9
    d2.original_fps = 9

    c = SynchroniserNode(routine_name="c", flow_name="f1", nodes=[d1, d2])
    c.curr_fps = 3
    c.original_fps = 3

    b = SynchroniserNode(routine_name="b", flow_name="f1", nodes=[c])
    b.curr_fps = 10
    b.original_fps = 10

    b.update_fps_by_fathers()

    assert b.curr_fps == 10
    assert c.curr_fps == 3
    assert d1.curr_fps == 3
    assert d2.curr_fps == 3


def test_notify_fps_notify_count_should_be_the_number_of_routines(mocker: MockerFixture):
    callback = mocker.MagicMock()

    d1 = SynchroniserNode(routine_name="d1", flow_name="f1", nodes=[])
    d2 = SynchroniserNode(routine_name="d2", flow_name="f1", nodes=[])

    c = SynchroniserNode(routine_name="c", flow_name="f1", nodes=[d1, d2])
    b = SynchroniserNode(routine_name="b", flow_name="f1", nodes=[c])

    b.notify_fps(callback)

    assert callback.call_count == 4


def test_reset():
    d1 = SynchroniserNode(routine_name="d1", flow_name="f1", nodes=[])
    d1.curr_fps = 7

    d2 = SynchroniserNode(routine_name="d2", flow_name="f1", nodes=[])
    d2.curr_fps = 9

    c = SynchroniserNode(routine_name="c", flow_name="f1", nodes=[d1, d2])
    c.curr_fps = 3

    b = SynchroniserNode(routine_name="b", flow_name="f1", nodes=[c])
    b.curr_fps = 10

    b.update_fps_by_fathers()
    b.update_fps_by_nodes()
    b.update_fps_by_nodes()

    b.reset()

    assert not b.calculated_fps
    assert not b.notified_delay_time
