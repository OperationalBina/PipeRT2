from typing import Dict, List, Set
from pipert2.core.base.wire import Wire
from pipert2.core.base.routine import Routine
from pipert2.utils.consts import GENERATOR_ROUTINE, INNER_ROUTINE, FINAL_ROUTINE


def infer_routines_types(wires: List[Wire]) -> Dict[str, Set[Routine]]:
    """
    Group routines by their inferred type.
    Types:
        GENERATOR_ROUTINE - Routine that only produces data and send via queue
        INNER_ROUTINE - Routine that receives data from another source, produces new data and send it via queue
        FINAL_ROUTINE - Routine that receives data from another source, performs manipulation and doesn't send
        it to another routine.

    Args:
        wires: List of wires which describes connections in the Pipeline

    Returns:
        Dictionary of key-string and value-Set[Routine] where key is one of three:
            GENERATOR_ROUTINE
            INNER_ROUTINE
            FINAL_ROUTINE
        and value is a unique set of routines that matches that key by method conditions.

    """
    sources = set()
    destinations = set()

    for wire in wires:
        sources.add(wire.source)

        for routine in wire.destinations:
            destinations.add(routine)

    generator = sources - destinations
    inner = sources.intersection(destinations)
    final = destinations - sources

    return {GENERATOR_ROUTINE: generator,
            INNER_ROUTINE: inner,
            FINAL_ROUTINE: final}
