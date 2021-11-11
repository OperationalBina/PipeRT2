import numpy as np
from pipert2 import fields
from pipert2.core.base.data import Data
from pipert2.core.base.data_transmitter import DataTransmitter
from pipert2.utils.shared_memory_manager import SharedMemoryManager


class SharedMemoryTransmitter(DataTransmitter):
    """A shared memory implementation of a data transmitter.

    """
    def __init__(self, data_size_threshold: int = 5000):
        """

        Args:
            data_size_threshold: The minimum size for a value to be saved in the shared memory.

        """

        self.data_size_threshold = data_size_threshold

    def transmit(self) -> callable:
        """Shared memory transmit implementation.

        Returns:
            A function that parses the payload data and saves necessary values in shared memory.
        """

        def func(data: Data) -> Data:
            """Parse a given dict and if necessary save a value in shared memory.

            Args:
                data: A dictionary to be parsed.

            Returns:
                A dictionary containing the same values as before, other than values saved in shared memory.
                In the format of: given dict: {"x": 1, "y":2, "z": [5]*size_threshold}
                                  returned_dict: {"x": 1, "y":2, "z": {"address": "{process_id}_{shared_mem_id}",
                                                                       "size": {size_threshold}}}

            """

            for field in fields(data.__class__):
                if field.type == dict:
                    modified_dict = {}

                    for key, value in getattr(data, field.name).items():
                        modified_dict[key] = save_value_in_shared_memory(value, self.data_size_threshold)

                    setattr(data, field.name, modified_dict)

                else:
                    value = getattr(data, field.name)
                    setattr(data, field.name, save_value_in_shared_memory(value, self.data_size_threshold))

            return data

        return func

    def receive(self) -> callable:
        """Shared memory receive implementation.

        Returns:
            A function that parses the payload data and reads necessary values from shared memory.

        """

        def func(data: Data) -> Data:
            """Parses a given dict and tries to read data from shared memory if a value is a dictionary.

            Args:
                data: A given dict with possible shared memory indications.

            Returns:
                A dictionary with generic python objects.

            """

            for field in fields(data.__class__):
                if field.type == dict and "address" not in getattr(data, field.name):  # Check for dict values
                    for outer_key, outer_value in getattr(data, field.name).items():
                        if type(outer_value) == dict:

                            value_from_shared_memory = get_data_in_shared_memory(outer_value)

                            if value_from_shared_memory is not None:
                                getattr(data, field.name)[outer_key] = value_from_shared_memory

                elif field.type == dict:  # The field is saved in shared memory
                    value_from_shared_memory = get_data_in_shared_memory(getattr(data, field.name))

                    if value_from_shared_memory is not None:
                        setattr(data, field.name, value_from_shared_memory)

            return data

        return func


def get_data_in_shared_memory(data_dict: dict):
    """Expects dictionary and returns its value if it stored in the shared memory
    If its not stored in the shared memory returns None

    """

    mem_name = data_dict.get("address", None)
    bytes_to_read = data_dict.get("size", None)

    if (mem_name is None) or (bytes_to_read is None):
        returned_value = None
    else:
        returned_value = SharedMemoryManager().read_from_mem(mem_name=mem_name,
                                                             bytes_to_read=bytes_to_read)

        if "shape" in data_dict:
            returned_value = np.frombuffer(returned_value, dtype=data_dict["dtype"])
            returned_value = returned_value.reshape(data_dict["shape"])

    return returned_value


def save_value_in_shared_memory(value, threshold_for_saving_in_shared_memory):
    """Save given value in shared memory.
    If the value size is not over the threshold it will not be saved.
    Returns the value address metadata if it saved, otherwise returns the value itself.

    """

    try:
        new_val = bytes(value)
    except TypeError:
        value_address_metadata = value
    else:
        if len(new_val) >= threshold_for_saving_in_shared_memory:
            address = SharedMemoryManager().write_to_mem(new_val)

            if type(value) == np.ndarray:
                value_address_metadata = {"address": address, "size": len(new_val),
                                          "shape": value.shape, "dtype": value.dtype}
            else:
                value_address_metadata = {"address": address, "size": len(new_val)}
        else:
            value_address_metadata = value

    return value_address_metadata
