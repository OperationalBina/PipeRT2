from typing import Tuple

from src.pipert2.core.base.routines.routine import Routine
from src.pipert2.core.base.data_transmitter import DataTransmitter
from src.pipert2.core.base.basic_transmitter import BasicTransmitter


class Wire:
    def __init__(self, source: Routine, destinations: Tuple[Routine, ...],
                 data_transmitter: DataTransmitter = None):
        self.source = source
        self.destinations = destinations
        self.data_transmitter = data_transmitter
