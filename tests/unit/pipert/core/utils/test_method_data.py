import pytest

from pipert2.utils.consts import START_EVENT_NAME
from pipert2.utils.method_data import Method


@pytest.fixture()
def method_without_specific_flows():
    return Method(event_name=START_EVENT_NAME)


@pytest.fixture()
def method_with_specific_flow():
    return Method(event_name=START_EVENT_NAME, specific_flow_routines={'flow1': []})


@pytest.fixture()
def method_with_specific_flow_and_routines():
    return Method(event_name=START_EVENT_NAME, specific_flow_routines={'flow1': ['r1', 'r2']})


def test_is_flow_valid_without_specific_flow(method_without_specific_flows: Method):
    assert method_without_specific_flows.is_applied_on_flow("flow1")


def test_is_flow_valid_with_another_flow_in_method(method_with_specific_flow: Method):
    assert not method_with_specific_flow.is_applied_on_flow("flow2")


def test_is_flow_valid_with_same_flow_in_method(method_with_specific_flow: Method):
    assert method_with_specific_flow.is_applied_on_flow("flow1")


def test_is_contain_routines_without_specific_flows(method_without_specific_flows: Method):
    assert not method_without_specific_flows.is_applied_on_specific_routines("flow1")


def test_is_contain_routines_with_specific_flow_without_routines(method_without_specific_flows: Method):
    assert not method_without_specific_flows.is_applied_on_specific_routines("flow1")


def test_is_contain_routines_with_specific_flow_with_routines(method_with_specific_flow_and_routines: Method):
    assert method_with_specific_flow_and_routines.is_applied_on_specific_routines("flow1")
