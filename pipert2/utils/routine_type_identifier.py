from typing import Dict, List, Set
from pipert2.core.base.routine import Routine
from pipert2.core.base.wire import Wire
from pipert2.utils.consts import GENERATOR_ROUTINE, INNER_ROUTINE, FINAL_ROUTINE


def infer_routines_types(wires: List[Wire]) -> Dict[str, Set[Routine]]:
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

