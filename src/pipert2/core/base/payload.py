from src.pipert2.core.managers.shared_memory import SharedMemory


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
        self.date_saved_in_shared_memory_metadata = {}
        self.data = data

    @property
    def data(self) -> dict:
        return self._data

    @data.setter
    def data(self, new_data) -> None:
        self._data = new_data
        self.date_saved_in_shared_memory_metadata = {}

        for data_name, data_value in new_data.items():
            if SharedMemory.does_data_saved_in_shared_memory(data_value):
                self.date_saved_in_shared_memory_metadata[data_name] = SharedMemory.get_data_metadata(data_value)

    def decode(self) -> None:
        """Decode the payload's data

        """

        if self.encoded:
            for data_in_shared_memory_name in self.date_saved_in_shared_memory_metadata.keys():
                self._data["data_in_shared_memory_name"] = \
                    SharedMemory.get_data(data_address=self._data["data_in_shared_memory_name"],
                                          metadata=self.date_saved_in_shared_memory_metadata[data_in_shared_memory_name])

            self.encoded = False

    def encode(self) -> None:
        """Encode the payload's data

        """

        if not self.encoded:
            for data_in_shared_memory_name in self.date_saved_in_shared_memory_metadata.keys():
                data_address = SharedMemory.save_data(self._data[data_in_shared_memory_name])
                self._data[data_in_shared_memory_name] = data_address

            self.encoded = True
