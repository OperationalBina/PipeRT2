import time
import pytest
import multiprocessing as mp
from pytest_mock import MockerFixture
from pipert2.core.base.synchronize_routines.routine_fps_listener import RoutineFPSListener


@pytest.fixture
def routine_fps_listener(mocker: MockerFixture):
    return RoutineFPSListener(mocker.MagicMock())


def test_update_start_routine_logic_time(routine_fps_listener):
    routine_fps_listener.update_start_routine_logic_time(**{'routine_name': 'r1'})

    assert time.time() - routine_fps_listener.latest_routines_start_time["r1"] < 0.001


def test_update_finish_routine_logic_time_empty_queue(routine_fps_listener):
    routine_fps_listener.latest_routines_start_time["r2"] = time.time()
    routine_fps_listener.update_finish_routine_logic_time(**{'routine_name': 'r2'})

    assert 'r2' in routine_fps_listener.routines_measurements


def test_update_finish_routine_logic_time_full_queue(routine_fps_listener: RoutineFPSListener, mocker: MockerFixture):

    routine_fps_listener.max_queue_size = 1

    mocker.patch('time.time', return_value=5)
    routine_fps_listener.update_start_routine_logic_time(**{'routine_name': 'r2'})

    mocker.patch('time.time', return_value=7)
    routine_fps_listener.update_finish_routine_logic_time(**{'routine_name': 'r2'})

    mocker.patch('time.time', return_value=10)
    routine_fps_listener.update_start_routine_logic_time(**{'routine_name': 'r2'})

    mocker.patch('time.time', return_value=15)
    routine_fps_listener.update_finish_routine_logic_time(**{'routine_name': 'r2'})

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