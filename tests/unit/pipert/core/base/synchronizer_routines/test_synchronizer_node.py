from pytest_mock import MockerFixture
from pipert2.core.base.synchronise_routines.synchroniser_node import synchroniserNode


def test_update_fps_by_nodes_required_fps_in_leaf_should_change_source_fps_to_leaf():
    d1 = synchroniserNode(routine_name="d1", flow_name="f1", nodes=[])
    d1.fps = 3

    d2 = synchroniserNode(routine_name="d2", flow_name="f1", nodes=[])
    d2.fps = 9

    c = synchroniserNode(routine_name="c", flow_name="f1", nodes=[d1, d2])
    c.fps = 10

    b = synchroniserNode(routine_name="b", flow_name="f1", nodes=[c])
    b.fps = 30

    b.update_fps_by_nodes()

    assert b.fps == 9
    assert c.fps == 9


def test_update_fps_by_nodes_required_fps_in_crossroad_should_change_source_fps_to_leaf():
    d1 = synchroniserNode(routine_name="d1", flow_name="f1", nodes=[])
    d1.fps = 7

    d2 = synchroniserNode(routine_name="d2", flow_name="f1", nodes=[])
    d2.fps = 9

    c = synchroniserNode(routine_name="c", flow_name="f1", nodes=[d1, d2])
    c.fps = 5

    b = synchroniserNode(routine_name="b", flow_name="f1", nodes=[c])
    b.fps = 30

    b.update_fps_by_nodes()

    assert b.fps == 5
    assert c.fps == 5
    assert d1.fps == 7
    assert d2.fps == 9


def test_update_fps_by_father_required_fps_in_source_change_all_nodes():
    d1 = synchroniserNode(routine_name="d1", flow_name="f1", nodes=[])
    d1.fps = 7
    d1.original_fps = 7

    d2 = synchroniserNode(routine_name="d2", flow_name="f1", nodes=[])
    d2.fps = 9
    d2.original_fps = 9

    c = synchroniserNode(routine_name="c", flow_name="f1", nodes=[d1, d2])
    c.fps = 15
    c.original_fps = 15

    b = synchroniserNode(routine_name="b", flow_name="f1", nodes=[c])
    b.fps = 3
    b.original_fps = 3

    b.update_fps_by_fathers()

    assert b.fps == 3
    assert c.fps == 3
    assert d1.fps == 3
    assert d2.fps == 3


def test_update_fps_by_father_required_fps_in_crossroad_should_change_the_nodes_in_the_hierarchy():
    d1 = synchroniserNode(routine_name="d1", flow_name="f1", nodes=[])
    d1.fps = 7
    d1.original_fps = 7

    d2 = synchroniserNode(routine_name="d2", flow_name="f1", nodes=[])
    d2.fps = 9
    d2.original_fps = 9

    c = synchroniserNode(routine_name="c", flow_name="f1", nodes=[d1, d2])
    c.fps = 3
    c.original_fps = 3

    b = synchroniserNode(routine_name="b", flow_name="f1", nodes=[c])
    b.fps = 10
    b.original_fps = 10

    b.update_fps_by_fathers()

    assert b.fps == 10
    assert c.fps == 3
    assert d1.fps == 3
    assert d2.fps == 3


def test_notify_fps_notify_count_should_be_the_number_of_routines(mocker: MockerFixture):

    callback = mocker.MagicMock()

    d1 = synchroniserNode(routine_name="d1", flow_name="f1", nodes=[])
    d2 = synchroniserNode(routine_name="d2", flow_name="f1", nodes=[])

    c = synchroniserNode(routine_name="c", flow_name="f1", nodes=[d1, d2])
    b = synchroniserNode(routine_name="b", flow_name="f1", nodes=[c])

    b.notify_fps(callback)

    assert callback.call_count == 4


def test_reset():

    d1 = synchroniserNode(routine_name="d1", flow_name="f1", nodes=[])
    d1.fps = 7

    d2 = synchroniserNode(routine_name="d2", flow_name="f1", nodes=[])
    d2.fps = 9

    c = synchroniserNode(routine_name="c", flow_name="f1", nodes=[d1, d2])
    c.fps = 3

    b = synchroniserNode(routine_name="b", flow_name="f1", nodes=[c])
    b.fps = 10

    b.update_fps_by_fathers()
    b.update_fps_by_nodes()
    b.update_fps_by_nodes()

    b.reset()

    assert not b.calculated_fps
    assert not b.notified_delay_time
