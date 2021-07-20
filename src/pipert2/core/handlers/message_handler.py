from abc import ABC, abstractmethod
from pipert2.core.base.message import Message


class MessageHandler(ABC):
    """The message handler is responsible for receiving messages
    and relaying them onward if needed.
    The message handler communicates only with the network object
    and not with other routines directly.
    """

    def __init__(self, input_obj, output_obj):
        self.input = input_obj
        self.output = output_obj

    @abstractmethod
    def get(self):
        """Returns the message from the input object.

        Returns:
            A message object.
        """

        raise NotImplementedError

    @abstractmethod
    def put(self, message: Message):
        """Puts a given message into the output object.

        Args:
            message: The message to be sent.

        """

        raise NotImplementedError
