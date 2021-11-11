import pytest
from mock import patch
from pipert2.utils.dummy_object import Dummy
from pipert2.core.managers.event_board import EventBoard
from tests.unit.pipert.core.utils.events_utils import EVENT1, START_EVENT, KILL_EVENT, STOP_EVENT

EVENTS = [START_EVENT, EVENT1, STOP_EVENT, KILL_EVENT]


@pytest.fixture()
def dummy_event_board():
    dummy_event_board = EventBoard()
    return dummy_event_board


@pytest.fixture()
def dummy_event_board_no_thread():
    with patch('pipert2.core.managers.event_board.Thread', return_value=Dummy()):
        dummy_event_board = EventBoard()
        yield dummy_event_board


def test_event_notifier(dummy_event_board_no_thread: EventBoard):
    event_notifier = dummy_event_board_no_thread.get_event_notifier()
    event_notifier(EVENT1.event_name)

    assert dummy_event_board_no_thread.new_events_queue.get() == EVENT1


def test_notify_event(dummy_event_board_no_thread: EventBoard):
    dummy_event_board_no_thread.notify_event(EVENT1.event_name)

    assert dummy_event_board_no_thread.new_events_queue.get() == EVENT1


def test_build_join(dummy_event_board: EventBoard):
    dummy_event_board.build()
    dummy_event_board.notify_event(KILL_EVENT.event_name)
    dummy_event_board.join()


def test_event_loop(dummy_event_board: EventBoard):
    event_handler = dummy_event_board.get_event_handler(
        {EVENT1.event_name, START_EVENT.event_name, STOP_EVENT.event_name, KILL_EVENT.event_name}
    )

    dummy_event_board.build()

    for event in EVENTS:
        dummy_event_board.notify_event(event.event_name)
        executed_event = event_handler.wait()
        assert executed_event == event

    dummy_event_board.join()
