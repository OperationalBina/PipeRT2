import pytest
from pytest_mock import MockerFixture
from pipert2 import MiddleRoutine, DestinationRoutine, SourceRoutine
from pipert2 import Wire
from pipert2.core.base.validators import wires_validator
from pipert2.utils.exceptions import WiresValidation


@pytest.fixture()
def valid_wires(mocker: MockerFixture):
    source_routine = mocker.MagicMock(spec=SourceRoutine)
    source_routine.name = "source_routine"

    middle1_routine = mocker.MagicMock(spec=MiddleRoutine)
    middle1_routine.name = "middle1_routine"

    middle2_routine = mocker.MagicMock(spec=MiddleRoutine)
    middle2_routine.name = "middle2_routine"

    middle3_routine = mocker.MagicMock(spec=MiddleRoutine)
    middle3_routine.name = "middle3_routine"

    middle4_routine = mocker.MagicMock(spec=MiddleRoutine)
    middle4_routine.name = "middle4_routine"

    destination_routine = mocker.MagicMock(spec=DestinationRoutine)
    destination_routine.name = "destination_routine"

    wires = [
        Wire(source=source_routine, destinations=(middle1_routine,)),
        Wire(source=middle1_routine, destinations=(middle2_routine, middle3_routine,)),
        Wire(source=middle3_routine, destinations=(destination_routine,)),
        Wire(source=middle2_routine, destinations=(destination_routine, middle4_routine)),
        Wire(source=middle4_routine, destinations=(destination_routine,)),
    ]

    return wires


def test_validate_existing_source_and_destination_routines_valid_wires(valid_wires):
    wires_validator.validate_existing_source_and_destination_routines(valid_wires)


def test_validate_existing_source_and_destination_routines_missing_source_routine_raises_error(mocker: MockerFixture):
    middle_routine = mocker.MagicMock(spec=MiddleRoutine)
    destination_routine = mocker.MagicMock(spec=DestinationRoutine)

    wires = [
        Wire(source=middle_routine, destinations=(destination_routine,)),
    ]

    with pytest.raises(WiresValidation):
        wires_validator.validate_existing_source_and_destination_routines(wires)


def test_validate_existing_source_and_destination_routines_missing_destination_routine_raises_error(mocker: MockerFixture):
    source_routine = mocker.MagicMock(spec=SourceRoutine)
    middle_routine = mocker.MagicMock(spec=MiddleRoutine)

    wires = [
        Wire(source=source_routine, destinations=(middle_routine,)),
    ]

    with pytest.raises(WiresValidation):
        wires_validator.validate_existing_source_and_destination_routines(wires)


def test_validate_order_links_valid_wires(valid_wires):
    wires_validator.validate_routines_place_properly(valid_wires)


def test_validate_order_links_connect_destination_to_middle_routine_raises_error(mocker: MockerFixture):
    source_routine = mocker.MagicMock(spec=SourceRoutine)
    source_routine.name = "source"

    middle_routine = mocker.MagicMock(spec=MiddleRoutine)
    middle_routine.name = "middle"

    destination_routine = mocker.MagicMock(spec=DestinationRoutine)
    destination_routine.name = "destination"

    wires = [
        Wire(source=source_routine, destinations=(middle_routine,)),
        Wire(source=destination_routine, destinations=(middle_routine,)),
    ]

    with pytest.raises(WiresValidation):
        wires_validator.validate_routines_place_properly(wires)


def test_validate_order_links_connect_middle_to_source_routine_raises_error(mocker: MockerFixture):
    source_routine = mocker.MagicMock(spec=SourceRoutine)
    source_routine.name = "source"

    middle1_routine = mocker.MagicMock(spec=MiddleRoutine)
    middle1_routine.name = "m1"

    middle2_routine = mocker.MagicMock(spec=MiddleRoutine)
    middle2_routine.name = "m2"

    wires = [
        Wire(source=source_routine, destinations=(middle1_routine,)),
        Wire(source=middle1_routine, destinations=(middle2_routine,)),
        Wire(source=middle2_routine, destinations=(source_routine,)),
    ]

    with pytest.raises(WiresValidation):
        wires_validator.validate_routines_place_properly(wires)


def test_validate_middle_routines_valid_wires(valid_wires):
    wires_validator.validate_consume_and_produce_on_middle_routines(valid_wires)


def test_validate_middle_routines_without_producing_middle_routine_routine_raises_error(mocker: MockerFixture):
    source_routine = mocker.MagicMock(spec=SourceRoutine)
    source_routine.name = "source"

    middle1_routine = mocker.MagicMock(spec=MiddleRoutine)
    middle1_routine.name = "middle"

    destination_routine = mocker.MagicMock(spec=DestinationRoutine)
    destination_routine.name = "destination"

    wires = [
        Wire(source=source_routine, destinations=(middle1_routine,)),
        Wire(source=source_routine, destinations=(destination_routine,)),
    ]

    with pytest.raises(WiresValidation):
        wires_validator.validate_consume_and_produce_on_middle_routines(wires)


def test_validate_middle_routines_without_consuming_middle_routine_routine_raises_error(mocker: MockerFixture):
    source_routine = mocker.MagicMock(spec=SourceRoutine)
    source_routine.name = "source"

    middle1_routine = mocker.MagicMock(spec=MiddleRoutine)
    middle1_routine.name = "middle"

    destination_routine = mocker.MagicMock(spec=DestinationRoutine)
    destination_routine.name = "destination"

    wires = [
        Wire(source=source_routine, destinations=(destination_routine,)),
        Wire(source=middle1_routine, destinations=(destination_routine,)),
    ]

    with pytest.raises(WiresValidation):
        wires_validator.validate_consume_and_produce_on_middle_routines(wires)


def test_validate_wires_valid_wires(valid_wires):
    wires_validator.validate_wires(valid_wires)
