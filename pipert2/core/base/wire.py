from typing import Tuple
from pipert2.core import Routine
from pipert2.core import DataTransmitter


class Wire:
    def __init__(self, source: Routine, destinations: Tuple[Routine, ...],
                 data_transmitter: DataTransmitter = None):
        self.source = source
        self.destinations = destinations
        self.data_transmitter = data_transmitter
