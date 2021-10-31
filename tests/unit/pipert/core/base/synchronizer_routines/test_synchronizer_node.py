from pytest_mock import MockerFixture
from pipert2.core.base.synchronize_routines.synchronizer_node import SynchronizerNode


def test_update_fps_by_nodes_required_fps_in_leaf_should_change_source_fps_to_leaf(mocker: MockerFixture):
    d1 = SynchronizerNode(routine_name="d1", flow_name="f1", nodes=[], manager=mocker.MagicMock())
    d1.fps.value = 3

    d2 = SynchronizerNode(routine_name="d2", flow_name="f1", nodes=[], manager=mocker.MagicMock())
    d2.fps.value = 9

    c = SynchronizerNode(routine_name="c", flow_name="f1", nodes=[d1, d2], manager=mocker.MagicMock())
    c.fps.value = 10

    b = SynchronizerNode(routine_name="b", flow_name="f1", nodes=[c], manager=mocker.MagicMock())
    b.fps.value = 30

    b.update_fps_by_nodes()

    assert b.fps.value == 9
    assert c.fps.value == 9


def test_update_fps_by_nodes_required_fps_in_crossroad_should_change_source_fps_to_leaf(mocker: MockerFixture):
    d1 = SynchronizerNode(routine_name="d1", flow_name="f1", nodes=[], manager=mocker.MagicMock())
    d1.fps.value = 7

    d2 = SynchronizerNode(routine_name="d2", flow_name="f1", nodes=[], manager=mocker.MagicMock())
    d2.fps.value = 9

    c = SynchronizerNode(routine_name="c", flow_name="f1", nodes=[d1, d2], manager=mocker.MagicMock())
    c.fps.value = 5

    b = SynchronizerNode(routine_name="b", flow_name="f1", nodes=[c], manager=mocker.MagicMock())
    b.fps.value = 30

    b.update_fps_by_nodes()

    assert b.fps.value == 5
    assert c.fps.value == 5
    assert d1.fps.value == 7
    assert d2.fps.value == 9


def test_update_fps_by_father_required_fps_in_source_change_all_nodes(mocker: MockerFixture):
    d1 = SynchronizerNode(routine_name="d1", flow_name="f1", nodes=[], manager=mocker.MagicMock())
    d1.fps.value = 7

    d2 = SynchronizerNode(routine_name="d2", flow_name="f1", nodes=[], manager=mocker.MagicMock())
    d2.fps.value = 9

    c = SynchronizerNode(routine_name="c", flow_name="f1", nodes=[d1, d2], manager=mocker.MagicMock())
    c.fps.value = 15

    b = SynchronizerNode(routine_name="b", flow_name="f1", nodes=[c], manager=mocker.MagicMock())
    b.fps.value = 3

    b.update_fps_by_fathers()

    assert b.fps.value == 3
    assert c.fps.value == 3
    assert d1.fps.value == 3
    assert d2.fps.value == 3


def test_update_fps_by_father_required_fps_in_crossroad_should_change_the_nodes_in_the_hierarchy(mocker: MockerFixture):
    d1 = SynchronizerNode(routine_name="d1", flow_name="f1", nodes=[], manager=mocker.MagicMock())
    d1.fps.value = 7

    d2 = SynchronizerNode(routine_name="d2", flow_name="f1", nodes=[], manager=mocker.MagicMock())
    d2.fps.value = 9

    c = SynchronizerNode(routine_name="c", flow_name="f1", nodes=[d1, d2], manager=mocker.MagicMock())
    c.fps.value = 3

    b = SynchronizerNode(routine_name="b", flow_name="f1", nodes=[c], manager=mocker.MagicMock())
    b.fps.value = 10

    b.update_fps_by_fathers()

    assert b.fps.value == 10
    assert c.fps.value == 3
    assert d1.fps.value == 3
    assert d2.fps.value == 3


def test_notify_fps_notify_count_should_be_the_number_of_routines(mocker: MockerFixture):

    callback = mocker.MagicMock()

    d1 = SynchronizerNode(routine_name="d1", flow_name="f1", nodes=[], manager=mocker.MagicMock())
    d2 = SynchronizerNode(routine_name="d2", flow_name="f1", nodes=[], manager=mocker.MagicMock())

    c = SynchronizerNode(routine_name="c", flow_name="f1", nodes=[d1, d2], manager=mocker.MagicMock())
    b = SynchronizerNode(routine_name="b", flow_name="f1", nodes=[c], manager=mocker.MagicMock())

    b.notify_fps(callback)

    assert callback.call_count == 4


def test_reset(mocker: MockerFixture):
    callback = mocker.MagicMock()

    d1 = SynchronizerNode(routine_name="d1", flow_name="f1", nodes=[], manager=mocker.MagicMock())
    d1.fps.value = 7

    d2 = SynchronizerNode(routine_name="d2", flow_name="f1", nodes=[], manager=mocker.MagicMock())
    d2.fps.value = 9

    c = SynchronizerNode(routine_name="c", flow_name="f1", nodes=[d1, d2], manager=mocker.MagicMock())
    c.fps.value = 3

    b = SynchronizerNode(routine_name="b", flow_name="f1", nodes=[c], manager=mocker.MagicMock())
    b.fps.value = 10

    b.update_fps_by_fathers()
    b.update_fps_by_nodes()
    b.update_fps_by_nodes()

    b.reset()

    assert not b.calculated_fps
    assert not b.notified_delay_time
