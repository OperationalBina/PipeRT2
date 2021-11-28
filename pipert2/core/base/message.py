import time
import pickle
import collections
from pipert2.core.base.data import Data
from pipert2.core.base.payload import Payload


class Message:
    """The Message is a wrapper for information that passes through the pipe.
    The information cannot pass alone, it passes inside the Message object during its entire stay.
    The Message is not exposed to the user and is used as a tool in the system. The Message helps route the
    information and remember its transit history (Further features in development).

    """

    counter = 0

    def __init__(self, data: Data, source_address: str):
        """
        Args:
            data: Data that the message will hold.
            source_address: Where the message was created.

        Attributes:
            payload (Payload): The payload that manages the data.
            source_address (str): Where the Message was first conceived.
            history (collections.OrderedDict): Transition history of the Message between the routines
            id (str): Unique id for the Message object.

        """

        self.payload: Payload = Payload(data)

        self.source_address = source_address
        self.history = collections.OrderedDict()
        self.id = f"{self.source_address}_{Message.counter}"

        Message.counter += 1

    def update_data(self, data: Data):
        """Update the data the message contains.

        Args:
            data (Data): dictionary containing the data.

        """

        self.payload.data = data

    def get_data(self) -> Data:
        """Get the data from the message.

        Returns:
            Dictionary with the message data.

        """

        if self.payload.encoded:
            self.payload.decode()

        return self.payload.data

    def record_entry(self, routine_name) -> None:
        """Records the timestamp of the message's entry into a routine.

        Args:
            routine_name: The name of the routine that the message entered.

        """

        self.history[routine_name] = time.time()

    def __str__(self):
        return f"{{msg id: {self.id}, " \
               f"source address: {self.source_address} }}\n"

    def full_description(self):
        return f"msg id: {self.id}, " \
               f"source address: {self.source_address}, " \
               f"history: {self.history} \n"

    @staticmethod
    def encode(msg) -> bytes:
        """Encodes the message object.
        This method compresses the message payload and then serializes the whole
        message object into bytes, using pickle.

        Args:
            msg (Message): The message to encode.

        Returns:
            Bytes containing the msg object.

        """

        msg.payload.encode()

        try:
            pickled_message = pickle.dumps(msg)
        except TypeError:  # TODO - Maybe add logs to exception
            pickled_message = msg

        return pickled_message

    @staticmethod
    def decode(encoded_msg: bytes, lazy=False):
        """Decodes the message object.
        This method deserializes the pickled message, and decodes the message
        payload if 'lazy' is False.

        Args:
            encoded_msg (Bytes): The message bytes to decode.
            lazy: If this is True, then the payload will only be decoded once it's
            accessed.

        Returns:
            Message object of the given message bytes.

        Raises:
            TypeError: if encoded_msg is None or not bytes.
        """
        
        try:
            msg = pickle.loads(encoded_msg)
        except TypeError:
            msg = encoded_msg

        if not lazy:
            msg.payload.decode()

        return msg
