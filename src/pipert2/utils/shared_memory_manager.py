import sys
from pipert2.utils.singleton import Singleton
if sys.version_info.minor <= 7:
    from pipert2.utils.shared_memory.shared_memory_generator import SharedMemoryGenerator, get_shared_memory_object


class SharedMemoryManager(metaclass=Singleton):
    def __init__(self, max_segment_count=50, segment_size=5000000):
        self.shared_memory_generator = SharedMemoryGenerator(max_segment_count=max_segment_count,
                                                             segment_size=segment_size)
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

    def cleanup_memory(self):
        self.shared_memory_generator.cleanup()
