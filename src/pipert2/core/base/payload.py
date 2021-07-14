from src.pipert2.core.base.shared_memory import get_data_from_shared_memory
from dataclasses import dataclass
from typing import Dict
import collections
import numpy as np


@dataclass
class ArrayMetadata:
    shape: tuple
    dtype: np.dtype
    frame_size: int
    shared_memory: bool


class Payload:
    def __init__(self, data: collections.Mapping):
        self.data: collections.Mapping = data
        self.encoded: bool = False
        self.data_metadata: Dict[str, ArrayMetadata] = {}

    def decode(self):
        if self.encoded:
            for data_key, data_metadata in self.data_metadata.items():
                if data_metadata.shared_memory:
                    decoded_data = get_data_from_shared_memory(self.data[data_key], data_metadata)
                else:
                    decoded_data = np.frombuffer(self.data[data_key], dtype=data_metadata.dtype)
                    decoded_data = decoded_data.reshape(data_metadata.shape)

                self.data[data_key] = decoded_data

            self.encoded = False

    def encode(self, generator):
        pass
