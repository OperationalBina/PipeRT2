from src.pipert2.core.base.payload import Payload

import collections
import time
import pickle


class Message:
    counter = 0

    def __init__(self, data: collections.Mapping, source_address: str):
        self.payload: Payload = Payload(data)

        self.source_address = source_address
        self.history = collections.OrderedDict()
        self.id = f"{self.source_address}_{Message.counter}"

        Message.counter += 1

    def update_data(self, data: collections.Mapping):
        """Update the data the message containing

        Args:
            data (collections.Mapping): dictionary containing the data
        """

        self.payload.data = data

    def get_data(self) -> collections.Mapping:
        """Get the data in the message

        Returns:
            Dictionary with the message data
        """

        if self.payload.encoded:
            self.payload.decode()
        return self.payload.data

    def record_entry(self, routine_name) -> None:
        """Records the timestamp of the message's entry into a component.

        Args:
            routine_name: the name of the routine that the message entered.
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
            msg (Message): the message to encode.

        Returns:
            Bytes containing the msg object
        """

        msg.payload.encode()
        return pickle.dumps(msg)

    @staticmethod
    def decode(encoded_msg: bytes, lazy=False):
        """
        Decodes the message object.
        This method deserializes the pickled message, and decodes the message
        payload if 'lazy' is False.

        Args:
            encoded_msg (Bytes): the message bytes to decode.
            lazy: if this is True, then the payload will only be decoded once it's
            accessed.

        Returns:
            Message object of the given message bytes
        """

        msg = pickle.loads(encoded_msg)
        if not lazy:
            msg.payload.decode()
        return msg
