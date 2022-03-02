import time
import pytest
from pipert2 import Wire, Pipe, START_EVENT_NAME
from tests.end_to_end.utils.routines.middle_buffering_routine import MiddleBufferingRoutine
from tests.end_to_end.utils.routines.source_generating_routine import SourceGeneratingRoutine
from tests.end_to_end.utils.routines.destination_saving_routine import DestinationSavingRoutine


TEST_TIME = 2


@pytest.mark.timeout(15)
def test_pipe_one_flow_expect_containing_generated_data():
    data = [
        "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"
    ]

    buffer = "A"

    src = SourceGeneratingRoutine(data)
    mid = MiddleBufferingRoutine(buffer, 10, "mid1")
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

    assert len(list(dst.values)) > 0
    assert all((val in expected_full_results) for val in list(dst.values))


@pytest.mark.timeout(15)
def test_pipe_multiple_flows_expect_containing_generated_data():
    data = [
        "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"
    ]

    buffer = "A"

    src = SourceGeneratingRoutine(data)
    mid = MiddleBufferingRoutine(buffer, 10, "mid1")
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

    assert len(list(dst.values)) > 0
    assert all((val in expected_full_results) for val in list(dst.values))


def test_pipe_notify_custom_event_to_one_routine():

    src = SourceGeneratingRoutine([], "src")
    mid = MiddleBufferingRoutine("", 10, "mid")
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
    mid = MiddleBufferingRoutine("", 10, "mid")
    dst = DestinationSavingRoutine()

    pipe = Pipe()
    pipe.create_flow("F1", True, src, mid, dst)
    pipe.build()

    pipe.notify_event("CUSTOM_EVENT")
    time.sleep(1)

    pipe.join(True)

    assert src.custom_event_notifies.is_set()
    assert mid.custom_event_notifies.is_set()


def test_pipe_notify_event_inside_a_routine_expect_event_to_notified():
    src = SourceGeneratingRoutine([], "src")
    mid = MiddleBufferingRoutine("", 10, "mid")
    dst = DestinationSavingRoutine()

    pipe = Pipe()
    pipe.create_flow("F1", True, src, mid, dst)
    pipe.build()

    pipe.notify_event("CUSTOM_EVENT_NOTIFY")
    time.sleep(1)

    pipe.join(True)

    assert src.custom_event_notifies.is_set()
    assert mid.middle_event_notifies.is_set()


def test_pipe_notify_event_with_argument_expect_setting_the_given_parameter():
    src = SourceGeneratingRoutine([], "src")
    mid = MiddleBufferingRoutine("", 10, "mid")
    dst = DestinationSavingRoutine()

    PARAM = 5

    pipe = Pipe()
    pipe.create_flow("F1", True, src, mid, dst)
    pipe.build()

    pipe.notify_event("CUSTOM_EVENT_PARAM", specific_routine="src", param=PARAM)
    time.sleep(1)

    pipe.join(True)

    assert src.custom_event_notifies.is_set()
    assert src.event_param.value == PARAM


def test_notify_event_from_pipe_with_parameter_expect_all_routines_to_get_the_given_parameter():
    src = SourceGeneratingRoutine([], "src")
    mid = MiddleBufferingRoutine("", 10, "mid")
    dst = DestinationSavingRoutine()

    PARAM = 5

    pipe = Pipe()
    pipe.create_flow("F1", True, src, mid, dst)
    pipe.build()

    pipe.notify_event("CUSTOM_EVENT_PARAM", param=PARAM)
    time.sleep(1)

    pipe.join(True)

    assert src.custom_event_notifies.is_set()
    assert src.event_param.value == PARAM

    assert mid.custom_event_notifies.is_set()
    assert mid.event_param.value == PARAM

    assert dst.custom_event_notifies.is_set()
    assert dst.event_param.value == PARAM


@pytest.mark.timeout(15)
def test_pipe_one_flow_multiple_middle_routines():
    data = [
        "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"
    ]

    src = SourceGeneratingRoutine(data)
    mid1 = MiddleBufferingRoutine("A", 10, "mid1", 0.5)
    mid2 = MiddleBufferingRoutine("B", 2, "mid2", 0.3)
    dst = DestinationSavingRoutine()

    pipe = Pipe()
    pipe.create_flow("F1", False, src, mid1, mid2, dst)
    pipe.link(Wire(source=src, destinations=(mid1, mid2)))
    pipe.link(Wire(source=mid1, destinations=(dst,)))
    pipe.link(Wire(source=mid2, destinations=(dst,)))

    pipe.build()

    pipe.notify_event(START_EVENT_NAME)

    time.sleep(3)

    pipe.join(True)

    expected_mid1_buffer = ["1A", "2A", "3A", "4A", "5A", "6A", "7A", "8A", "9A", "10A"]
    expected_mid2_buffer = ["1B", "2B", "3B", "4B", "5B", "6B", "7B", "8B", "9B", "10B"]

    expected_full_results = expected_mid1_buffer + expected_mid2_buffer

    assert len(list(dst.values)) > 0
    assert any((val in expected_mid1_buffer) for val in list(dst.values))
    assert any((val in expected_mid2_buffer) for val in list(dst.values))
    assert all((val in expected_full_results) for val in list(dst.values))


@pytest.mark.timeout(15)
def test_pipe_multiple_flows_and_multiple_middle_routines():
    data = [
        "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"
    ]

    src = SourceGeneratingRoutine(data)
    mid1 = MiddleBufferingRoutine("A", 10, "mid1", 0.5)
    mid2 = MiddleBufferingRoutine("B", 10, "mid2")
    dst = DestinationSavingRoutine()

    pipe = Pipe()

    pipe.create_flow("F1", False, src)
    pipe.create_flow("F2", False, mid1)
    pipe.create_flow("F3", False, mid2)
    pipe.create_flow("F4", False, dst)

    pipe.link(Wire(source=src, destinations=(mid1, mid2)))
    pipe.link(Wire(source=mid1, destinations=(dst,)))
    pipe.link(Wire(source=mid2, destinations=(dst,)))

    pipe.build()

    pipe.notify_event(START_EVENT_NAME)

    time.sleep(3)

    pipe.join(True)

    expected_mid1_buffer = ["1A", "2A", "3A", "4A", "5A", "6A", "7A", "8A", "9A", "10A"]
    expected_mid2_buffer = ["1B", "2B", "3B", "4B", "5B", "6B", "7B", "8B", "9B", "10B"]

    expected_full_results = expected_mid1_buffer + expected_mid2_buffer

    assert len(list(dst.values)) > 0
    assert any((val in expected_mid1_buffer) for val in list(dst.values))
    assert any((val in expected_mid2_buffer) for val in list(dst.values))
    assert all((val in expected_full_results) for val in list(dst.values))
