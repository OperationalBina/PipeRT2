import numpy as np


class Payload:
    def __init__(self, data: dict):
        self.encoded = False
        self.numpy_data_metadata = {}
        self.data = data

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, new_data):  # Remember, we might reassign the shared memory value to the data !!
        self._data = new_data
        self.numpy_data_metadata = {}

        for data_name, data_value in new_data.items():
            if isinstance(data_value, np.ndarray):
                self.numpy_data_metadata[data_name] = {
                    "shape": data_value.shape,
                    "dtype": data_value.dtype,
                }

    def decode(self):
        if self.encoded:
            pass

    def encode(self):
        if not self.encoded:
            pass