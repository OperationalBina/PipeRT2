from typing import Tuple
from abc import ABC, abstractmethod
from collections import defaultdict
from src.pipert2.core import Routine
from src.pipert2.core import DataTransmitter
from src.pipert2.core import MessageHandler


class Network(ABC):
    """The network is responsible for managing all of the communication in the pipe.
    It generates the message handlers used by the routines, and can change who the routines send their messages to.

    """

    def __init__(self):
        self.message_handlers = defaultdict(str)

    @abstractmethod
    def get_message_handler(self, routine_name: str) -> MessageHandler:
        """Generate a new message handler, save it, and return it to the routine.

        Args:
            routine_name: The name of the routine for the message handler.

        Returns:
            The new message handler for the routine.

        """

        raise NotImplementedError

    @abstractmethod
    def link(self, source: Routine, destinations: Tuple[Routine], data_transmitter: DataTransmitter):
        """Rewire the destinations of a given routine.

        Args:
            source: The source routine to be linked.
            destinations: A list of all of the destination routines.
            data_transmitter: The DataTransmitter object that provides the methods to move data between routines.

        """

        raise NotImplementedError

