import time
import pytest
from pipert2 import Wire, Pipe, START_EVENT_NAME
from tests.end_to_end.utils.routines.middle_buffering_routine import MiddleBufferingRoutine
from tests.end_to_end.utils.routines.source_generating_routine import SourceGeneratingRoutine
from tests.end_to_end.utils.routines.destination_saving_routine import DestinationSavingRoutine


TEST_TIME = 2


@pytest.mark.timeout(15)
def test_pipe_one_flow():
    data = [
        "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"
    ]

    buffer = "A"

    src = SourceGeneratingRoutine(data)
    mid = MiddleBufferingRoutine(buffer, 10, "mid1", True)
    dst = DestinationSavingRoutine()

    pipe = Pipe()
    pipe.create_flow("F1", True, src, mid, dst)
    pipe.build()

    pipe.notify_event(START_EVENT_NAME)

    time.sleep(3)

    pipe.join(True)

    expected_full_results = [
        "1A", "2A", "3A", "4A", "5A", "6A", "7A", "8A", "9A", "10A"
    ]

    assert all((val in expected_full_results) for val in list(dst.values))


@pytest.mark.timeout(15)
def test_pipe_multiple_flows():
    data = [
        "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"
    ]

    buffer = "A"

    src = SourceGeneratingRoutine(data)
    mid = MiddleBufferingRoutine(buffer, 10, "mid1", True)
    dst = DestinationSavingRoutine()

    pipe = Pipe()
    pipe.create_flow("F1", False, src)
    pipe.create_flow("F2", False, mid)
    pipe.create_flow("F3", False, dst)

    pipe.link(Wire(source=src, destinations=(mid,)))
    pipe.link(Wire(source=mid, destinations=(dst,)))

    pipe.build()

    pipe.notify_event(START_EVENT_NAME)

    time.sleep(3)

    pipe.join(True)

    expected_full_results = [
        "1A", "2A", "3A", "4A", "5A", "6A", "7A", "8A", "9A", "10A"
    ]

    assert all((val in expected_full_results) for val in list(dst.values))


def test_pipe_notify_custom_event_to_one_routine():

    src = SourceGeneratingRoutine([], "src")
    mid = MiddleBufferingRoutine("", 10, "mid", True)
    dst = DestinationSavingRoutine()

    pipe = Pipe()
    pipe.create_flow("F1", True, src, mid, dst)
    pipe.build()

    pipe.notify_event("CUSTOM_EVENT", specific_routine="src")
    time.sleep(1)

    pipe.join(True)

    assert src.custom_event_notifies.is_set()
    assert not mid.custom_event_notifies.is_set()


def test_pipe_notify_custom_event_all_routines():

    src = SourceGeneratingRoutine([], "src")
    mid = MiddleBufferingRoutine("", 10, "mid", True)
    dst = DestinationSavingRoutine()

    pipe = Pipe()
    pipe.create_flow("F1", True, src, mid, dst)
    pipe.build()

    pipe.notify_event("CUSTOM_EVENT")
    time.sleep(1)

    pipe.join(True)

    assert src.custom_event_notifies.is_set()
    assert mid.custom_event_notifies.is_set()

