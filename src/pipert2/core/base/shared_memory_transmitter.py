from src.pipert2.core.base.data_transmitter import DataTransmitter
from pipert2.utils.shared_memory_manager import SharedMemoryManager


class SharedMemoryTransmitter(DataTransmitter):
    """A shared memory implementation of a data transmitter.

    """

    def transmit(self) -> callable:
        """Shared memory transmit implementation.

        Returns:
            A function that parses the payload data and saves necessary values in shared memory.
        """

        def func(data: dict, size_threshold: int = 5000) -> dict:
            """Parse a given dict and if necessary save a value in shared memory.

            Args:
                data: A dictionary to be parsed.
                size_threshold: The minimum size for a value to be saved in the shared memory.

            Returns:
                A dictionary containing the same values as before, other than values saved in shared memory.
                In the format of: given dict: {"x": 1, "y":2, "z": [5]*size_threshold}
                                  returned_dict: {"x": 1, "y":2, "z": {"address": "{process_id}_{shared_mem_id}",
                                                                       "size": {size_threshold}}}

            """

            return_dict = {}

            for key, value in data.items():
                try:
                    new_val = bytes(value)
                except TypeError:
                    return_dict[key] = value
                else:
                    if len(new_val) >= size_threshold:
                        address = SharedMemoryManager().write_to_mem(new_val)
                        return_dict[key] = {"address": address, "size": len(new_val)}
                    else:
                        return_dict[key] = value

            return return_dict

        return func

    def receive(self) -> callable:
        """Shared memory receive implementation.

        Returns:
            A function that parses the payload data and reads necessary values from shared memory.

        """

        def func(data: dict) -> dict:
            """Parses a given dict and tries to read data from shared memory if a value is a dictionary.

            Args:
                data: A given dict with possible shared memory indications.

            Returns:
                A dictionary with generic python objects.

            """

            return_dict = {}

            for key, value in data.items():
                if type(value) == dict:
                    mem_name = value.get("address", "")
                    bytes_to_read = value.get("size", 0)
                    returned_value = SharedMemoryManager().read_from_mem(mem_name=mem_name,
                                                                         bytes_to_read=bytes_to_read)

                    if returned_value:
                        return_dict[key] = returned_value
                    else:
                        return_dict[key] = value
                else:
                    return_dict[key] = value

            return return_dict

        return func
