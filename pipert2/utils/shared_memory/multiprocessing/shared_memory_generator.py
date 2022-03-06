import os
from multiprocessing.shared_memory import SharedMemory
from pipert2.utils.shared_memory.general.memory_id_iterator import MemoryIdIterator


def get_shared_memory_object(name: str):
    """Returns a SharedMemory object that correlates to the name given.

    Args:
        name: The name of a shared memory.

    """

    try:
        memory = SharedMemory(name=name)
    except FileNotFoundError:
        memory = None

    return memory


class SharedMemoryGenerator:
    """Generates a new shared memory each time get_next_shared_memory is called
    and is responsible for cleaning up shared memories if the count that
    exists now exceeds the max or the process has ended.

    """

    def __init__(self, max_segment_count: int):
        self.memory_id_gen = MemoryIdIterator(os.getpid(), max_segment_count)
        self.max_segment_count = max_segment_count
        self.shared_memories = {}

    def get_next_shared_memory(self, size: int) -> SharedMemory:
        """Allocate a new shared memory object with the given size.

        Args:
            size: The size in bytes of the wanted shared memory segment.

        Returns:
            A multiprocessing shared memory object.

        """

        next_name = self.memory_id_gen.get_next()

        try:
            memory = SharedMemory(name=next_name, create=True, size=size)
        except FileExistsError:
            self._destroy_memory(next_name)
            memory = SharedMemory(name=next_name, create=True, size=size)

        self.shared_memories[next_name] = memory

        return memory

    def cleanup(self):
        """Deallocate all existing shared memory segments.

        """

        for _ in range(self.max_segment_count):
            name_to_unlink = self.memory_id_gen.get_next()

            if name_to_unlink:
                if name_to_unlink in self.shared_memories:
                    self._destroy_memory(name_to_unlink)

    def _destroy_memory(self, name_to_unlink):
        """Close given shared memory to free up memory.

        Args:
            name_to_unlink: The name of the shared memory segment to destroy.

        """

        self.shared_memories[name_to_unlink].close()
        self.shared_memories[name_to_unlink].unlink()
        self.shared_memories.pop(name_to_unlink)
