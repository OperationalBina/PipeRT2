import pytest
from pipert2 import Wire
from pytest_mock import MockerFixture
from pipert2.core.base.validators import flow_validator
from pipert2.utils.exceptions import FloatingRoutine, UniqueRoutineName


def test_validate_flow(mocker: MockerFixture):
    dummy_routine1 = mocker.MagicMock()
    dummy_routine1.name = "routine1"

    dummy_flow1 = mocker.MagicMock()
    dummy_flow1.name = "flow1"
    dummy_flow1.routines = {dummy_routine1.name: dummy_routine1}

    dummy_routine2 = mocker.MagicMock()
    dummy_routine2.name = "routine2"

    dummy_flow2 = mocker.MagicMock()
    dummy_flow2.name = "flow2"
    dummy_flow2.routines = {dummy_routine2.name: dummy_routine2}

    dummy_wires = {
        (dummy_flow1.name, dummy_routine1.name): Wire(source=dummy_routine1, destinations=(dummy_routine2,))
    }

    flows = {
        dummy_flow1.name: dummy_flow1,
        dummy_flow2.name: dummy_flow2
    }

    flow_validator.validate_flow(flows=flows, wires=dummy_wires)


def test_validate_flows_routines_are_linked_with_valid_flow(mocker: MockerFixture):
    dummy_routine1 = mocker.MagicMock()
    dummy_routine1.name = "r1"

    dummy_routine2 = mocker.MagicMock()
    dummy_routine2.name = "r2"

    dummy_flow1 = mocker.MagicMock()
    dummy_flow1.name = "flow1"
    dummy_flow1.routines = {dummy_routine1.name: dummy_routine1,
                            dummy_routine2.name: dummy_routine2}

    dummy_routine3 = mocker.MagicMock()
    dummy_routine3.name = "r3"

    dummy_routine4 = mocker.MagicMock()
    dummy_routine4.name = "r4"

    dummy_routine5 = mocker.MagicMock()
    dummy_routine5.name = "r5"

    dummy_flow2 = mocker.MagicMock()
    dummy_flow2.name = "flow2"
    dummy_flow2.routines = {dummy_routine3.name: dummy_routine3,
                            dummy_routine4.name: dummy_routine4,
                            dummy_routine5.name: dummy_routine5}

    flows = {"flow1": dummy_flow1, "flow2": dummy_flow2}

    wires = {
        ("flow1", "r1"): Wire(source=dummy_routine1, destinations=(dummy_routine2, dummy_routine3,)),
        ("flow_2", "r3"): Wire(source=dummy_routine3, destinations=(dummy_routine4, dummy_routine5)),
    }

    flow_validator.validate_flows_routines_are_linked(flows, wires)


def test_validate_routines_unique_names(mocker: MockerFixture):
    dummy_routine1 = mocker.MagicMock()
    dummy_routine1.name = "r1"

    dummy_flow1 = mocker.MagicMock()
    dummy_flow1.name = "flow1"
    dummy_flow1.routines = {dummy_routine1.name: dummy_routine1}

    dummy_routine3 = mocker.MagicMock()
    dummy_routine3.name = "r3"

    dummy_routine4 = mocker.MagicMock()
    dummy_routine4.name = "r4"

    dummy_flow2 = mocker.MagicMock()
    dummy_flow2.name = "flow2"
    dummy_flow2.routines = {
        dummy_routine3.name: dummy_routine3,
        dummy_routine4.name: dummy_routine4
    }

    flows = {"flow1": dummy_flow1, "flow2": dummy_flow2}

    flow_validator.validate_routines_unique_names(flows)


def test_validate_routines_unique_names_existing_names(mocker: MockerFixture):
    dummy_routine1 = mocker.MagicMock()
    dummy_routine1.name = "r1"

    dummy_flow1 = mocker.MagicMock()
    dummy_flow1.name = "flow1"
    dummy_flow1.routines = {dummy_routine1.name: dummy_routine1}

    dummy_routine3 = mocker.MagicMock()
    dummy_routine3.name = "r1"

    dummy_routine4 = mocker.MagicMock()
    dummy_routine4.name = "r4"

    dummy_flow2 = mocker.MagicMock()
    dummy_flow2.name = "flow2"
    dummy_flow2.routines = {
        dummy_routine3.name: dummy_routine3,
        dummy_routine4.name: dummy_routine4
    }

    flows = {"flow1": dummy_flow1, "flow2": dummy_flow2}

    with pytest.raises(UniqueRoutineName) as error:
        flow_validator.validate_routines_unique_names(flows)

    assert "r1" in str(error)


def test_validate_flows_routines_are_linked_floating_routine_build_raises_error(mocker: MockerFixture):
    dummy_routine1 = mocker.MagicMock()
    dummy_routine1.name = "r1"

    dummy_routine2 = mocker.MagicMock()
    dummy_routine2.name = "r2"

    dummy_flow1 = mocker.MagicMock()
    dummy_flow1.name = "flow1"
    dummy_flow1.routines = {dummy_routine1.name: dummy_routine1,
                            dummy_routine2.name: dummy_routine2}

    dummy_routine3 = mocker.MagicMock()
    dummy_routine3.name = "r3"

    dummy_routine4 = mocker.MagicMock()
    dummy_routine4.name = "r4"

    dummy_routine5 = mocker.MagicMock()
    dummy_routine5.name = "r5"

    dummy_flow2 = mocker.MagicMock()
    dummy_flow2.name = "flow2"
    dummy_flow2.routines = {dummy_routine3.name: dummy_routine3,
                            dummy_routine4.name: dummy_routine4,
                            dummy_routine5.name: dummy_routine5}

    flows = {"flow1": dummy_flow1, "flow2": dummy_flow2}

    wires = {
        ("flow1", "r1"): Wire(source=dummy_routine1, destinations=(dummy_routine2, dummy_routine3,)),
        ("flow_2", "r3"): Wire(source=dummy_routine3, destinations=(dummy_routine4,)),
    }

    with pytest.raises(FloatingRoutine) as error:
        flow_validator.validate_flows_routines_are_linked(flows=flows, wires=wires)

    assert "r5" in str(error)
