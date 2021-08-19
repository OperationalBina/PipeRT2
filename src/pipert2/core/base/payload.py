class Payload:
    """The payload object is what actually stores the data.
    It is responsible for encoding and decoding the data itself.

    """

    def __init__(self, data: dict):
        """
        Args:
            data: Data that the payload will hold.

        Attributes:
            data (dict): The data that the payload will hold.
            encoded (bool): Whether the data is encoded or not.
            date_saved_in_shared_memory_metadata (dict):
                The metadata for the data keys that stored in the shared memory.

        """

        self.encoded = False
        self.data = data

    @property
    def data(self) -> dict:
        return self._data

    @data.setter
    def data(self, new_data) -> None:
        if self.encoded:
            self.encoded = False

        self._data = new_data

    def decode(self, decoder) -> None:
        """Decode the payload's data

        """

        if self.encoded:
            self._data = decoder.decode(self._data)

            self.encoded = False

    def encode(self, encoder) -> None:
        """Encode the payload's data

        """

        if not self.encoded:
            self._data = encoder.encode(self._data)

            self.encoded = True
