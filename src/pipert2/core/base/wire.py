from collections import Iterable
from typing import Tuple

from src.pipert2.core.base.routine import Routine


class Wire:
    def __init__(self, source: Routine, destinations: Tuple[Routine, ...]):
        self.source = source
        self.destinations = destinations
