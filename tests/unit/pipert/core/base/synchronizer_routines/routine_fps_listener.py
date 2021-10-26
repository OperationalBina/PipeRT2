import time
import multiprocessing as mp
from datetime import datetime

import pytest
from pytest_mock import MockerFixture
from pipert2.core.base.synchronize_routines.routine_fps_listener import RoutineFPSListener


@pytest.fixture
def routine_fps_listener(mocker: MockerFixture):
    return RoutineFPSListener(mocker.MagicMock)


def test_update_start_routine_logic_time(routine_fps_listener):
    routine_fps_listener.update_start_routine_logic_time(**{'routine_name': 'r1'})

    assert time.time() - routine_fps_listener.latest_routines_start_time["r1"] < 0.00001


def test_update_finish_routine_logic_time_empty_queue(routine_fps_listener):
    routine_fps_listener.latest_routines_start_time["r2"] = time.time()
    routine_fps_listener.update_finish_routine_logic_time(**{'routine_name': 'r2'})

    assert 'r2' in routine_fps_listener.routines_measurements


def test_calculate_median(routine_fps_listener):
    routine_fps_listener.routines_measurements = {
        'r3': mp.Queue(5)
    }

    routine_fps_listener.routines_measurements['r3'].put(1)
    routine_fps_listener.routines_measurements['r3'].put(2)
    routine_fps_listener.routines_measurements['r3'].put(2)
    routine_fps_listener.routines_measurements['r3'].put(4)

    med = routine_fps_listener.calculate_median_fps('r3')
    # assert med == 1/2