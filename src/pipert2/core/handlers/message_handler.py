from abc import ABC, abstractmethod
from src.pipert2.core.base.message import Message


class MessageHandler(ABC):
    """The message handler is responsible for receiving messages
    and relaying them onward if needed.
    The message handler communicates only with the network object
    and not with other routines directly.

    """

    def __init__(self, routine_name: str):
        self.routine_name = routine_name

    @abstractmethod
    def _get(self) -> bytes:
        """Returns the message from the input object.

        Returns:
            A message object.

        """

        raise NotImplementedError

    @abstractmethod
    def _put(self, message: bytes):
        """Puts a given message into the output object.

        Args:
            message: The message to be sent.

        """

        raise NotImplementedError

    def put(self, message: Message):
        """Encodes a given message and calls the implemented put method.

        Args:
            message: The message to be sent.

        """

        self._put(Message.encode(message))

    def get(self) -> Message:
        """Decodes the message received from the implemented get method.

        Returns: A decoded message object.

        """
        try:
            message = Message.decode(self._get())
        except TypeError:
            message = None
        else:
            message.record_entry(self.routine_name)

        return message
