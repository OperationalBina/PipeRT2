import time
import pytest
from mock import patch
from pipert2 import Pipe, START_EVENT_NAME, KILL_EVENT_NAME, Wire, FPS_MULTIPLIER
from tests.end_to_end.utils.routines.middle_counter_routine import MiddleCounterRoutine
from tests.end_to_end.utils.routines.source_counter_routine import SourceCounterRoutine
from tests.end_to_end.utils.routines.destination_counter_routine import DestinationCounterRoutine


TEST_TIME = 2


@pytest.mark.timeout(15)
@patch("pipert2.core.base.routines.fps_routine.ROUTINE_NOTIFY_DURATIONS_INTERVAL", 0.25)
@patch("pipert2.core.base.synchronise_routines.routines_synchroniser.SYNCHRONISER_UPDATE_INTERVAL", 0.25)
def test_number_of_executions_of_main_logic_slow_routine_in_the_last_one():
    source_counter_routine = SourceCounterRoutine(20, "src")
    destination_counter_routine = DestinationCounterRoutine(12, "dst")

    pipe = Pipe(auto_pacing_mechanism=True)

    pipe.create_flow("f1", True, source_counter_routine, destination_counter_routine)
    pipe.build()

    pipe.notify_event(START_EVENT_NAME)

    time.sleep(TEST_TIME)

    pipe.notify_event(KILL_EVENT_NAME)
    pipe.join()

    assert 0 < round(source_counter_routine.estimate_fps.value) <= 12 * FPS_MULTIPLIER
    assert 0 < round(destination_counter_routine.estimate_fps.value) <= 12 * FPS_MULTIPLIER


@pytest.mark.timeout(15)
@patch("pipert2.core.base.routines.fps_routine.ROUTINE_NOTIFY_DURATIONS_INTERVAL", 0.25)
@patch("pipert2.core.base.synchronise_routines.routines_synchroniser.SYNCHRONISER_UPDATE_INTERVAL", 0.25)
def test_number_of_executions_of_main_logic_slow_routine_in_the_last_one_consts_fps():
    source_counter_routine = SourceCounterRoutine(40, "src")
    source_counter_routine.set_const_fps(20)

    destination_counter_routine = DestinationCounterRoutine(12, "dst")

    pipe = Pipe(auto_pacing_mechanism=True)

    pipe.create_flow("f1", True, source_counter_routine, destination_counter_routine)
    pipe.build()

    pipe.notify_event(START_EVENT_NAME)

    time.sleep(TEST_TIME)

    pipe.notify_event(KILL_EVENT_NAME)
    pipe.join()

    assert source_counter_routine.estimate_fps.value == 20
    assert 0 < round(destination_counter_routine.estimate_fps.value) <= 12 * FPS_MULTIPLIER


@pytest.mark.timeout(15)
@patch("pipert2.core.base.routines.fps_routine.ROUTINE_NOTIFY_DURATIONS_INTERVAL", 0.25)
@patch("pipert2.core.base.synchronise_routines.routines_synchroniser.SYNCHRONISER_UPDATE_INTERVAL", 0.25)
def test_number_of_executions_of_main_logic_slow_routine_in_the_first_one():
    source_counter_routine = SourceCounterRoutine(12, "src")
    destination_counter_routine = DestinationCounterRoutine(20, "dst")

    pipe = Pipe(auto_pacing_mechanism=True)

    pipe.create_flow("f1", True, source_counter_routine, destination_counter_routine)
    pipe.build()

    pipe.notify_event(START_EVENT_NAME)

    time.sleep(TEST_TIME)

    pipe.notify_event(KILL_EVENT_NAME)
    pipe.join()

    assert 0 < round(source_counter_routine.estimate_fps.value) <= 12 * FPS_MULTIPLIER
    assert 0 < round(destination_counter_routine.estimate_fps.value) <= 12 * FPS_MULTIPLIER


@pytest.mark.timeout(15)
@patch("pipert2.core.base.routines.fps_routine.ROUTINE_NOTIFY_DURATIONS_INTERVAL", 0.25)
@patch("pipert2.core.base.synchronise_routines.routines_synchroniser.SYNCHRONISER_UPDATE_INTERVAL", 0.25)
def test_complex_pipe():
    source_counter_routine = SourceCounterRoutine(20, "src")
    middle_counter_routine = MiddleCounterRoutine(12, "mid")
    destination1_counter_routine = DestinationCounterRoutine(30, "d1")
    destination2_counter_routine = DestinationCounterRoutine(8, "d2")

    pipe = Pipe(auto_pacing_mechanism=True)

    pipe.create_flow("f1",
                     False,
                     source_counter_routine,
                     middle_counter_routine,
                     destination1_counter_routine,
                     destination2_counter_routine)

    pipe.link(
        Wire(source=source_counter_routine, destinations=(middle_counter_routine,)),
        Wire(source=middle_counter_routine, destinations=(destination1_counter_routine, destination2_counter_routine,))
    )

    pipe.build()

    pipe.notify_event(START_EVENT_NAME)

    time.sleep(TEST_TIME)

    pipe.notify_event(KILL_EVENT_NAME)
    pipe.join()

    assert 0 < round(source_counter_routine.estimate_fps.value) <= 12 * FPS_MULTIPLIER
    assert 0 < round(middle_counter_routine.estimate_fps.value) <= 12 * FPS_MULTIPLIER
    assert 0 < round(destination1_counter_routine.estimate_fps.value) <= 12 * FPS_MULTIPLIER
    assert 0 < round(destination2_counter_routine.estimate_fps.value) <= 8 * FPS_MULTIPLIER
