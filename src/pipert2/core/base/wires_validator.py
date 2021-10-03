from typing import List
from .wire import Wire
from .routines import DestinationRoutine
from .routines import MiddleRoutine
from .routines import SourceRoutine
from ...utils.exceptions.pipe_validation_failed import PipeValidationError


def validate_wires(wires: List[Wire]):
    """Validate wires by logical rules: contain source and destination,
                                        link source to middle/end and source/middle to end,
                                        each middle routine is consumed and produced by another routines.

        Throws a pipe_validation_failed if validation failed.

    Args:
        wires: Wires to validate.
    """

    validate_existing_source_and_destination_routines(wires)
    validate_routines_place_properly(wires)
    validate_consume_and_produce_on_middle_routines(wires)


def validate_routines_place_properly(wires: List[Wire]):
    """Validate the source and destination routines - Raise a PipeValidationError if source placed as middle or
    destination routine placed as source routine.

    Args:
        wires: Wires to validate.
    """

    for wire in wires:
        if isinstance(wire.source, DestinationRoutine):
            raise PipeValidationError("Can't link any destination routine to any routine")
        else:
            for destination_routine in wire.destinations:
                if isinstance(destination_routine, SourceRoutine):
                    raise PipeValidationError("Can't link any routine to source routine")


def validate_existing_source_and_destination_routines(wires: List[Wire]):
    """Validate existing source routine and destination routine - Raise a PipeValidationError if doesn't exist.

    Args:
        wires: Wires to validate.
    """

    source_routine_exists = False
    destination_routine_exists = False

    for wire in wires:
        if isinstance(wire.source, SourceRoutine):
            source_routine_exists = True

        for destination_routine in wire.destinations:
            if isinstance(destination_routine, DestinationRoutine):
                destination_routine_exists = True

    if not source_routine_exists:
        raise PipeValidationError("Source routine doesn't exist")
    if not destination_routine_exists:
        raise PipeValidationError("Destination routine doesn't exist")


def validate_consume_and_produce_on_middle_routines(wires: List[Wire]):
    """Validate each middle routine consume data from another routine and consumed by another routine.
    Raise a PipeValidationError if doesn't consume or consumed by.

    Args:
        wires: Wires to validate.
    """

    middle_routines = {}

    for wire in wires:
        if isinstance(wire.source, MiddleRoutine):
            middle_routines.setdefault(wire.source.name, {"source": True, "destination": False})
            middle_routines[wire.source.name].update({"source": True})

        for destination_routine in wire.destinations:
            if isinstance(destination_routine, MiddleRoutine):
                middle_routines.setdefault(destination_routine.name, {"destination": True, "source": False})
                middle_routines[destination_routine.name].update({"destination": True})

    for routine_name, middle_routine in middle_routines.items():
        if not middle_routine["source"]:
            raise PipeValidationError(f"{routine_name} doesn't have a source routine")
        if not middle_routine["destination"]:
            raise PipeValidationError(f"{routine_name} doesn't have a destination routine")
