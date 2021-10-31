import time
import pytest
import multiprocessing as mp
from pytest_mock import MockerFixture
from pipert2.core.base.synchronize_routines.routine_fps_listener import RoutineFpsListener


@pytest.fixture
def routine_fps_listener(mocker: MockerFixture):
    return RoutineFpsListener(mocker.MagicMock(), mocker.MagicMock())


def test_update_start_routine_logic_time(routine_fps_listener):
    start_time = time.time()
    routine_fps_listener.update_start_routine_logic_time(**{'routine_name': 'r1', 'start_time': start_time})

    assert routine_fps_listener.latest_routines_start_time['r1'] == start_time


def test_update_finish_routine_logic_time_empty_queue(routine_fps_listener: RoutineFpsListener):

    start_time = time.time()

    time.sleep(0.01)

    end_time = time.time()

    routine_fps_listener.latest_routines_start_time['r2'] = start_time
    routine_fps_listener.update_finish_routine_logic_time(**{'routine_name': 'r2', 'end_time': end_time})

    assert 'r2' in routine_fps_listener.routines_measurements
    assert list(routine_fps_listener.routines_measurements['r2']) == list([end_time - start_time])


def test_update_finish_routine_logic_time_full_queue(routine_fps_listener: RoutineFpsListener):

    routine_fps_listener.max_queue_size = 1

    routine_fps_listener.update_start_routine_logic_time(**{'routine_name': 'r2', 'start_time': 5})
    routine_fps_listener.update_finish_routine_logic_time(**{'routine_name': 'r2', 'end_time': 7})

    routine_fps_listener.update_start_routine_logic_time(**{'routine_name': 'r2', 'start_time': 10})
    routine_fps_listener.update_finish_routine_logic_time(**{'routine_name': 'r2', 'end_time': 15})

    assert list(routine_fps_listener.routines_measurements["r2"]) == list([5])


def test_calculate_median_not_empty_list(routine_fps_listener):
    routine_fps_listener.routines_measurements = {
        'r3': mp.Manager().list()
    }

    routine_fps_listener.routines_measurements['r3'].append(0.001)
    routine_fps_listener.routines_measurements['r3'].append(0.002)
    routine_fps_listener.routines_measurements['r3'].append(0.002)
    routine_fps_listener.routines_measurements['r3'].append(0.004)

    assert routine_fps_listener.calculate_median_fps('r3') == 1/0.002


def test_calculate_median_empty_list(routine_fps_listener):
    routine_fps_listener.routines_measurements = {
        'r3': mp.Manager().list()
    }

    assert routine_fps_listener.calculate_median_fps('r3') == 0
