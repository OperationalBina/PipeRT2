from pipert2.core.base.data import Data


class Payload:
    """The payload object is what actually stores the data.
    It is responsible for encoding and decoding the data itself.

    """

    def __init__(self, data: Data):
        """
        Args:
            data: Data that the payload will hold.

        Attributes:
            data (Data): The data that the payload will hold.
            encoded (bool): Whether the data is encoded or not.

        """

        self.encoded = False
        self.data = data

    @property
    def data(self) -> Data:
        return self._data

    @data.setter
    def data(self, new_data) -> None:
        self.encoded = False

        self._data = new_data

    def decode(self) -> None:
        """Decode the payload's data

        """

        if self.encoded:
            # self._data = decoder.decode(self._data)  # TODO - Add data encoding logic

            self.encoded = False

    def encode(self) -> None:
        """Encode the payload's data

        """

        if not self.encoded:
            # self._data = encoder.encode(self._data)

            self.encoded = True
