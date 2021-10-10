from logging import Logger
from typing import Optional
from abc import ABC, abstractmethod
from pipert2.utils.dummy_object import Dummy
from pipert2.core.base.message import Message


class MessageHandler(ABC):
    """The message handler is responsible for receiving messages
    and relaying them onward if needed.
    The message handler communicates only with the network object
    and not with other routines directly.

    """

    def __init__(self, routine_name: str):
        self.routine_name = routine_name
        self.transmit = None
        self.receive = None
        self.logger: Logger = Dummy()

    @abstractmethod
    def _get(self) -> Optional[bytes]:
        """Returns the message from the input object. If the input object is not initialized return None.

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

    @abstractmethod
    def teardown(self):
        """Teardown resources used by the message handler.

        """

        raise NotImplementedError

    def put(self, message: Message):
        """Encodes a given message and calls the implemented put method.

        Args:
            message: The message to be sent.

        """

        if callable(self.transmit):
            transmitted_data = self.transmit(message.payload.data)
            message.update_data(transmitted_data)

        self._put(Message.encode(message))

    def get(self) -> Message:
        """Decodes the message received from the implemented get method.

        Returns:
            A decoded message object.

        """

        message = self._get()

        if message is not None:
            message = Message.decode(message)

            if callable(self.receive):
                received_data = self.receive(message.payload.data)
                message.update_data(received_data)

            message.record_entry(self.routine_name)

        return message
