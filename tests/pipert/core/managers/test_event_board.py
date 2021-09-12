import pytest

from src.pipert2.utils.consts.event_names import START_EVENT_NAME, STOP_EVENT_NAME, KILL_EVENT_NAME
from src.pipert2.utils.method_data import Method
from src.pipert2.core.managers.event_board import EventBoard

EVENT1_NAME = "event1"
EVENT1 = Method(event_name=EVENT1_NAME)


START_EVENT = Method(event_name=START_EVENT_NAME)
STOP_EVENT = Method(event_name=STOP_EVENT_NAME)
KILL_EVENT = Method(event_name=KILL_EVENT_NAME)


EVENTS = [START_EVENT, EVENT1, STOP_EVENT, KILL_EVENT]


@pytest.fixture
def dummy_event_board():
    dummy_event_board = EventBoard()
    return dummy_event_board


def test_event_notifier(dummy_event_board: EventBoard):
    event_notifier = dummy_event_board.get_event_notifier()
    event_notifier(EVENT1.event_name)

    assert dummy_event_board.new_events_queue.get() == EVENT1


def test_event_notifier_specific_flow(dummy_event_board: EventBoard):

    TEST_EVENT = Method("test", {"flow1": None})

    event_notifier = dummy_event_board.get_event_notifier()
    event_notifier(TEST_EVENT.event_name, routines_by_flow={"flow1": None})

    assert dummy_event_board.new_events_queue.get() == TEST_EVENT


def test_notify_event(dummy_event_board: EventBoard):
    dummy_event_board.notify_event(EVENT1.event_name)

    assert dummy_event_board.new_events_queue.get() == EVENT1


def test_notify_event_with_specific_flow(dummy_event_board: EventBoard):
    dummy_event_board.notify_event(EVENT1.event_name)

    assert dummy_event_board.new_events_queue.get() == EVENT1


def test_event_loop(dummy_event_board: EventBoard):
    event_handler = dummy_event_board.get_event_handler([EVENT1.event_name])

    dummy_event_board.build()

    for event in EVENTS:
        dummy_event_board.notify_event(event.event_name)
        executed_event = event_handler.wait()
        assert executed_event == event
