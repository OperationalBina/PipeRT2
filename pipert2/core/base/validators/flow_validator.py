from typing import Dict, List
from pipert2.core.base.wire import Wire
from pipert2.core.base.flow import Flow
from pipert2.utils.exceptions import FloatingRoutine, UniqueRoutineName


def validate_flow(flows: Dict[str, Flow], wires: Dict[tuple, Wire]):
    """Validate flow and raise an exception if not valid.

    Args:
        flows: The flows to validate.
        wires: The wires to validate.
    Raises:
        UniqueRoutineName: Raises in two or more routines have the same name.
        FloatingRoutine: If a routine contained in flow but not link to any other routines.
    """

    validate_routines_unique_names(flows)
    validate_flows_routines_are_linked(flows, wires)


def validate_routines_unique_names(flows: Dict[str, Flow]):
    """Validate all routines in the flows has unique names.

    Args:
        flows: The flow to validate.
    Raises:
        UniqueRoutineName: Raises in two or more routines have the same name.
    """

    routine_names = []

    for flow in flows.values():
        for routine in flow.routines.values():
            if routine.name in routine_names:
                raise UniqueRoutineName(f"The routine name {routine.name} isn't unique, please choose a unique name.")

            routine_names.append(routine.name)


def validate_flows_routines_are_linked(flows: Dict[str, Flow], wires: Dict[tuple, Wire]):
    """Validate that all routines flows are linked to other routines.

    Raises:
        FloatingRoutine: If a routine contained in flow but not link to any other routines.

    """

    for flow in flows.values():
        for routine in flow.routines.values():
            routine_contained = False
            for wire in wires.values():
                if wire.source.name == routine.name or routine in wire.destinations:
                    routine_contained = True
                    break

            if not routine_contained:
                raise FloatingRoutine(f"The routine {routine.name} "
                                      f"in flow {flow.name} isn't linked to any other routine.")
