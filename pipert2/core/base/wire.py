from typing import Tuple
from pipert2.core.base.routine import Routine
from pipert2.core.base.data_transmitter import DataTransmitter


class Wire:
    def __init__(self, source: Routine, destinations: Tuple[Routine, ...],
                 data_transmitter: DataTransmitter = None):
        self.source = source
        self.destinations = destinations
        self.data_transmitter = data_transmitter
