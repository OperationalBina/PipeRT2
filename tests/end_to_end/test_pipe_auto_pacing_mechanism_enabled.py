import time

from pipert2 import Pipe, START_EVENT_NAME, KILL_EVENT_NAME, Wire
from tests.end_to_end.utils.routines.middle_counter_routine import MiddleCounterRoutine

from tests.end_to_end.utils.routines.source_counter_routine import SourceCounterRoutine
from tests.end_to_end.utils.routines.destination_counter_routine import DestinationCounterRoutine


def test_number_of_executions_of_main_logic_slow_routine_in_the_last_one():
    source_counter_routine = SourceCounterRoutine(20, "src")
    destination_counter_routine = DestinationCounterRoutine(12, "dst")

    pipe = Pipe(auto_pacing_mechanism=True)
    pipe.routine_synchronizer.updating_interval = 0.25

    pipe.create_flow("f1", True, source_counter_routine, destination_counter_routine)
    pipe.build()

    pipe.notify_event(START_EVENT_NAME)

    time.sleep(0.9)

    pipe.notify_event(KILL_EVENT_NAME)
    pipe.join()

    # For 0.25 seconds it runs in 20 fps, so source count will be ~= 5, and destination will be ~= 3
    # For 0.75 seconds it runs in 12 fps, so source count will be ~= 5 + 9, and destination will be ~= 3 + 9

    # assert 13 <= source_counter_routine.counter.value <= 15
    # assert 10 <= destination_counter_routine.counter.value <= 12


def test_number_of_executions_of_main_logic_slow_routine_in_the_first_one():
    source_counter_routine = SourceCounterRoutine(12, "src")
    destination_counter_routine = DestinationCounterRoutine(20, "dst")

    pipe = Pipe(auto_pacing_mechanism=True)
    pipe.routine_synchronizer.updating_interval = 0.25

    pipe.create_flow("f1", True, source_counter_routine, destination_counter_routine)
    pipe.build()

    pipe.notify_event(START_EVENT_NAME)

    time.sleep(0.9)

    pipe.notify_event(KILL_EVENT_NAME)
    pipe.join()

    # For 1 second it runs in 12 fps, so source count will be ~= 12, and destination will be less by one, then ~= 11

    # assert 10 <= source_counter_routine.counter.value <= 12
    # assert 10 <= destination_counter_routine.counter.value <= 12


def test_complex_pipe():
    source_counter_routine = SourceCounterRoutine(20, "src")
    middle_counter_routine = MiddleCounterRoutine(12, "mid")
    destination1_counter_routine = DestinationCounterRoutine(30, "d1")
    destination2_counter_routine = DestinationCounterRoutine(8, "d2")

    pipe = Pipe(auto_pacing_mechanism=True)
    pipe.routine_synchronizer.updating_interval = 0.25

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

    time.sleep(1)

    pipe.notify_event(KILL_EVENT_NAME)
    pipe.join()

    # For 0.25 seconds source runs in 20 fps, middle and the dest1 run in 12 fps, dest2 runs in 5
    # For 0.75 seconds source runs in 12 fps, middle and the dest1 run in 12 fps, dest2 runs in 5

    assert 14 <= source_counter_routine.counter.value <= 15
    assert 11 <= middle_counter_routine.counter.value <= 13
    assert 11 <= destination1_counter_routine.counter.value <= 13
    assert 7 <= destination2_counter_routine.counter.value <= 9
