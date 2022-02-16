from pipert2.utils.shared_memory.general.shared_memory_manager import AbsSharedMemoryManager
from pipert2.utils.shared_memory.multiprocessing.shared_memory_generator import SharedMemoryGenerator, \
    get_shared_memory_object


class SharedMemoryManager(AbsSharedMemoryManager):
    """The shared memory manager interacts with an implementation of a shared memory library, and simplifies user usage.

    """

    def __init__(self, max_segment_count: int = 50, segment_size: int = 5000000):
        self.shared_memory_generator = SharedMemoryGenerator(max_segment_count=max_segment_count)

    def write_to_mem(self, data: bytes) -> str:
        """Writes given bytes to the shared memory.

        Args:
            data: Bytes to write to shared memory.

        Returns:
            The name of the shared memory segment written to.

        """

        memory = self.shared_memory_generator.get_next_shared_memory(size=len(data))

        if memory:
            memory.buf[:] = data

        return memory.name

    def read_from_mem(self, mem_name: str, bytes_to_read: int) -> [bytes, None]:
        """Reads from a given shared memory segment.

        Args:
            mem_name: The name of the shared memory segment.
            bytes_to_read: How many bytes to read from the shared memory.

        Returns:
            The bytes stored on the shared memory.

        """

        memory = get_shared_memory_object(mem_name)

        if memory:
            data = bytes(memory.buf[:bytes_to_read])
        else:
            data = None

        return data

    def cleanup_memory(self):
        """Call the cleanup method of the shared_memory_generator to release all of the memory held.

        """

        self.shared_memory_generator.cleanup()
