from src.pipert2.core.base.data_transmitter import DataTransmitter
from pipert2.utils.shared_memory_manager import SharedMemoryManager


class PosixIpcTransmitter(DataTransmitter):
    def transmit(self) -> callable:
        def func(data: dict, size_threshold: int = 5000) -> dict:
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
        def func(data: dict) -> dict:
            return_dict = {}

            for key, value in data.items():
                if type(value) == dict:
                    mem_name = value.get("address", "")
                    bytes_to_read = value.get("size", 0)
                    return_dict[key] = SharedMemoryManager().read_from_mem(mem_name=mem_name,
                                                                           bytes_to_read=bytes_to_read)
                else:
                    return_dict[key] = value

            return return_dict

        return func
