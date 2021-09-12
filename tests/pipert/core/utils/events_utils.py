import pytest
from pytest_mock import MockerFixture

from src.pipert2.utils.consts.event_names import START_EVENT_NAME, KILL_EVENT_NAME, STOP_EVENT_NAME
from src.pipert2.utils.method_data import Method

EVENT1_NAME = "event1"
EVENT1 = Method(event_name=EVENT1_NAME)

START_EVENT = Method(event_name=START_EVENT_NAME)
STOP_EVENT = Method(event_name=STOP_EVENT_NAME)
KILL_EVENT = Method(event_name=KILL_EVENT_NAME)


