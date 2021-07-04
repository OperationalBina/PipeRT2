import pytest

from src.pipert2.core.base.routine import Routine


def test_routine_has_base_events():
    BASE_EVENTS = ["start", "stop"]

    assert all(event in Routine.events.all for event in BASE_EVENTS)


def test_routine_has_base_runners():
    BASE_RUNNERS = ["thread"]

    assert all(runner in Routine.runners.all for runner in BASE_RUNNERS)
