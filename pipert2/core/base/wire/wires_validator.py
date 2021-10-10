from typing import List
from pipert2.core.base.wire import Wire
from pipert2.utils.exceptions.wires_validation import WiresValidation
from pipert2.core.base.routines import DestinationRoutine, MiddleRoutine, SourceRoutine


def validate_wires(wires: List[Wire]):
    """Validate wires by logical rules: contain source and destination,
                                        link source to middle/end and source/middle to end,
                                        each middle routine is consumed and produced by another routines.

    Args:
        wires: Wires to validate.

    Raises:
        WiresValidation: If validation failed.
    """

    validate_existing_source_and_destination_routines(wires)
    validate_routines_place_properly(wires)
    validate_consume_and_produce_on_middle_routines(wires)


def validate_routines_place_properly(wires: List[Wire]):
    """Validate the source and destination routines.

    Args:
        wires: Wires to validate.

    Raises:
        WiresValidation: If source placed as middle or destination routine placed as source routine.
    """

    for wire in wires:
        if isinstance(wire.source, DestinationRoutine):
            raise WiresValidation(f"The destination routine {wire.source.name} "
                                  f"can't be a source routine to any other routine.")
        else:
            for destination_routine in wire.destinations:
                if isinstance(destination_routine, SourceRoutine):
                    raise WiresValidation(f"The source routine {destination_routine.name} "
                                          f"can't be a destination routine to any other routine.")


def validate_existing_source_and_destination_routines(wires: List[Wire]):
    """Validate existing source routine and destination routine - Raise a PipeValidationError if doesn't exist.

    Args:
        wires: Wires to validate.

    Raises:
        WiresValidation: If source and destination routines don't exist
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
        raise WiresValidation("Your pipe doesn't contain any source routine,"
                              " add a routine for consuming data.")
    if not destination_routine_exists:
        raise WiresValidation("Your pipe doesn't contain any destination routine,"
                              " add a routine for producing result.")


def validate_consume_and_produce_on_middle_routines(wires: List[Wire]):
    """Validate each middle routine consume data from another routine and consumed by another routine.
    Raise a PipeValidationError if doesn't consume or consumed by.

    Args:
        wires: Wires to validate.

    Raises:
        WiresValidation: If exists middle routine that doesn't consume or consumed by
    """

    middle_routines = {}

    for wire in wires:
        if isinstance(wire.source, MiddleRoutine):
            middle_routines.setdefault(wire.source.name, {"destination": True, "source": False})
            middle_routines[wire.source.name].update({"destination": True})

        for destination_routine in wire.destinations:
            if isinstance(destination_routine, MiddleRoutine):
                middle_routines.setdefault(destination_routine.name, {"source": True, "destination": False})
                middle_routines[destination_routine.name].update({"source": True})

    for routine_name, middle_routine in middle_routines.items():
        if not middle_routine["source"]:
            raise WiresValidation(f"The routine {routine_name} isn't link to any routine,"
                                  f"add a routine that consume current routine's result.")
        if not middle_routine["destination"]:
            raise WiresValidation(f"The routine {routine_name} isn't have a destination routine,"
                                  f"add a routine that produce data from current routine.")
