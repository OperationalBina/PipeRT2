from abc import ABC, abstractmethod
from pipert2.core.handlers.message_handler import MessageHandler
from typing import List
from collections import defaultdict


class Network(ABC):
    """The network is responsible for managing all of the communicaiton in the pipe.
    It generates the message handlers used by the routines, and can change who the routines send their messages to.

    """

    def __init__(self):
        self.message_handlers = defaultdict(str)

    @abstractmethod
    def _generate_message_handler(self) -> MessageHandler:
        """Generate a new message handler, save it, and return it to the routine.

        Returns:
            The new message handler for the routine.
        """

        raise NotImplementedError

    @abstractmethod
    def _change_communication(self, src: str, dest: List[str]):
        """Rewire the destinations of a given message handler.

        Args:
            src: The name of the routine holding the source message handler.
            dest: A list of all of the destination routines.

        """

        raise NotImplementedError

