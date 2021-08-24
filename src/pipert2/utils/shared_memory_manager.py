from pipert2.utils.singleton import Singleton
from pipert2.utils.shared_memory.shared_memory_generator import SharedMemoryGenerator, get_shared_memory_object


class SharedMemoryManager(metaclass=Singleton):
    def __init__(self):
        self.shared_memory_generator = SharedMemoryGenerator()
        self.shared_memory_generator.create_memories()

    def write_to_mem(self, data: bytes) -> str:
        memory_name = self.shared_memory_generator.get_next_shared_memory_name()
        memory = get_shared_memory_object(memory_name)

        memory.acquire_semaphore()
        memory.write_to_memory(data)
        memory.release_semaphore()

        return memory_name

    def read_from_mem(self, mem_name: str, bytes_to_read: int) -> bytes:
        memory = get_shared_memory_object(mem_name)

        memory.acquire_semaphore()
        data = memory.read_from_memory(size=bytes_to_read)
        memory.release_semaphore()

        return data
