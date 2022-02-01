from typing import Dict, List, Set, Tuple
from pipert2.core.base.routine import Routine
from pipert2.core.base.routines.extended_run_factory import FINAL_EXTENDED_RUN, GENERATOR_EXTENDED_RUN, INNER_EXTENDED_RUN
from pipert2.core.base.wire import Wire


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

    return {GENERATOR_EXTENDED_RUN: generator,
            INNER_EXTENDED_RUN: inner,
            FINAL_EXTENDED_RUN: final}
