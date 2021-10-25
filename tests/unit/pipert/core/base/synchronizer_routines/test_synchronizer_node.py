from pytest_mock import MockerFixture
from pipert2.core.base.synchronize_routines.synchronizer_node import SynchronizerNode


def test_update_fps_by_nodes_required_fps_in_leaf_should_change_source_fps_to_leaf(mocker: MockerFixture):
    d1 = SynchronizerNode(name="d1", fps=3, nodes=[], notify_delay_time_callback=mocker.MagicMock())
    d2 = SynchronizerNode(name="d2", fps=9, nodes=[], notify_delay_time_callback=mocker.MagicMock())

    c = SynchronizerNode(name="c", fps=10, nodes=[d1, d2], notify_delay_time_callback=mocker.MagicMock())
    b = SynchronizerNode(name="b", fps=30, nodes=[c], notify_delay_time_callback=mocker.MagicMock())

    b.update_fps_by_nodes()

    assert b.fps == 9
    assert c.fps == 9


def test_update_fps_by_nodes_required_fps_in_crossroad_should_change_source_fps_to_leaf(mocker: MockerFixture):
    d1 = SynchronizerNode(name="d1", fps=7, nodes=[], notify_delay_time_callback=mocker.MagicMock())
    d2 = SynchronizerNode(name="d2", fps=9, nodes=[], notify_delay_time_callback=mocker.MagicMock())

    c = SynchronizerNode(name="c", fps=5, nodes=[d1, d2], notify_delay_time_callback=mocker.MagicMock())
    b = SynchronizerNode(name="b", fps=30, nodes=[c], notify_delay_time_callback=mocker.MagicMock())

    b.update_fps_by_nodes()

    assert b.fps == 5
    assert c.fps == 5
    assert d1.fps == 7
    assert d2.fps == 9


def test_update_fps_by_father_required_fps_in_source_change_all_nodes(mocker: MockerFixture):
    d1 = SynchronizerNode(name="d1", fps=7, nodes=[], notify_delay_time_callback=mocker.MagicMock())
    d2 = SynchronizerNode(name="d2", fps=9, nodes=[], notify_delay_time_callback=mocker.MagicMock())

    c = SynchronizerNode(name="c", fps=15, nodes=[d1, d2], notify_delay_time_callback=mocker.MagicMock())
    b = SynchronizerNode(name="b", fps=3, nodes=[c], notify_delay_time_callback=mocker.MagicMock())

    b.update_fps_by_fathers()

    assert b.fps == 3
    assert c.fps == 3
    assert d1.fps == 3
    assert d2.fps == 3


def test_update_fps_by_father_required_fps_in_crossroad_should_change_the_nodes_in_the_hierarchy(mocker: MockerFixture):
    d1 = SynchronizerNode(name="d1", fps=7, nodes=[], notify_delay_time_callback=mocker.MagicMock())
    d2 = SynchronizerNode(name="d2", fps=9, nodes=[], notify_delay_time_callback=mocker.MagicMock())

    c = SynchronizerNode(name="c", fps=3, nodes=[d1, d2], notify_delay_time_callback=mocker.MagicMock())
    b = SynchronizerNode(name="b", fps=10, nodes=[c], notify_delay_time_callback=mocker.MagicMock())

    b.update_fps_by_fathers()

    assert b.fps == 10
    assert c.fps == 3
    assert d1.fps == 3
    assert d2.fps == 3


def test_notify_fps_notify_count_should_be_the_number_of_routines(mocker: MockerFixture):

    callback = mocker.MagicMock()

    d1 = SynchronizerNode(name="d1", fps=7, nodes=[], notify_delay_time_callback=callback)
    d2 = SynchronizerNode(name="d2", fps=9, nodes=[], notify_delay_time_callback=callback)

    c = SynchronizerNode(name="c", fps=3, nodes=[d1, d2], notify_delay_time_callback=callback)
    b = SynchronizerNode(name="b", fps=10, nodes=[c], notify_delay_time_callback=callback)

    b.notify_fps()

    assert callback.call_count == 4


def test_reset(mocker: MockerFixture):
    callback = mocker.MagicMock()

    d1 = SynchronizerNode(name="d1", fps=7, nodes=[], notify_delay_time_callback=callback)
    d2 = SynchronizerNode(name="d2", fps=9, nodes=[], notify_delay_time_callback=callback)

    c = SynchronizerNode(name="c", fps=3, nodes=[d1, d2], notify_delay_time_callback=callback)
    b = SynchronizerNode(name="b", fps=10, nodes=[c], notify_delay_time_callback=callback)

    b.update_fps_by_fathers()
    b.update_fps_by_nodes()
    b.update_fps_by_nodes()

    b.reset()

    assert not b.calculated_fps
    assert not b.notified_delay_time
