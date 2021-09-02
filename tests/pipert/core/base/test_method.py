import pytest
from src.pipert2.core.base.method import Method
from src.pipert2.utils.consts.event_names import START_EVENT_NAME
from tests.pipert.core.utils.events_utils import START_EVENT


FLOW_NAME = "flow1"
ROUTINE_NAME = "routine1"


@pytest.fixture()
def base_method():
    return Method(name=START_EVENT_NAME)


@pytest.fixture()
def method_with_specific_flow_and_routine():
    return Method(name=f"{START_EVENT_NAME}-{FLOW_NAME}-{ROUTINE_NAME}")


def test_is_flow_valid_method_with_specific_flow_and_routine(method_with_specific_flow_and_routine):
    assert method_with_specific_flow_and_routine.is_valid_by_flow(FLOW_NAME)


def test_is_flow_valid_method_only_with_event(base_method):
    assert base_method.is_valid_by_flow("random_name")


def test_create_base_method_with_specific_flow_and_routine(method_with_specific_flow_and_routine, base_method):
    assert method_with_specific_flow_and_routine.create_base_method() == START_EVENT


def test_create_base_method_only_with_event(base_method):
    assert base_method.create_base_method() == START_EVENT


def test_get_routine_name_with_contained_routine(method_with_specific_flow_and_routine):
    assert method_with_specific_flow_and_routine.get_routine_name() == ROUTINE_NAME


def test_get_routine_name_without_routine(base_method):
    assert not base_method.get_routine_name()
