import pytest
from src.pipert2.core.managers.event_board import EventBoard
from tests.pipert.core.utils.events_utils import EVENT1, START_EVENT, KILL_EVENT, STOP_EVENT

EVENTS = [START_EVENT, EVENT1, STOP_EVENT, KILL_EVENT]


@pytest.fixture()
def dummy_event_board():
    dummy_event_board = EventBoard()
    return dummy_event_board


def test_event_notifier(dummy_event_board: EventBoard):
    event_notifier = dummy_event_board.get_event_notifier()
    event_notifier(EVENT1.name)

    assert dummy_event_board.new_events_queue.get() == EVENT1


def test_notify_event(dummy_event_board: EventBoard):
    dummy_event_board.notify_event(EVENT1.name)

    assert dummy_event_board.new_events_queue.get() == EVENT1


def test_event_loop(dummy_event_board: EventBoard):
    event_handler = dummy_event_board.get_event_handler([EVENT1.name])

    dummy_event_board.build()

    for event in EVENTS:
        dummy_event_board.notify_event(event.name)
        executed_event = event_handler.wait()
        assert executed_event == event

