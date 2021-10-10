import os
import mmap
import posix_ipc
from typing import Optional
from pipert2.utils.shared_memory.shared_memory import SharedMemory
from pipert2.utils.shared_memory.memory_id_iterator import MemoryIdIterator


def get_shared_memory_object(name: str) -> Optional[SharedMemory]:
    """Get a SharedMemory object that correlates to the name given.

    Args:
        name: The name of a shared memory.

    Returns:
        A SharedMemory object.

    """

    memory = posix_ipc.SharedMemory(name)
    semaphore = posix_ipc.Semaphore(name)
    mapfile = mmap.mmap(memory.fd, memory.size)
    memory.close_fd()
    semaphore.release()
    shared_memory = SharedMemory(memory, semaphore, mapfile)

    return shared_memory


class SharedMemoryGenerator:
    """Generates a set 'max_segment_count' amount of shared memories with each being as large as 'segment_size' to be
    used.

    """

    def __init__(self, max_segment_count: int, segment_size: int):
        self.memory_id_gen = MemoryIdIterator(os.getpid(), max_segment_count)
        self.max_segment_count = max_segment_count
        self.shared_memories = {}
        self.segment_size = segment_size

    def create_memories(self):
        """Creates the maximum segment count of shared memories.

        """

        for _ in range(self.max_segment_count):
            next_name = self.memory_id_gen.get_next()
            memory = posix_ipc.SharedMemory(next_name, posix_ipc.O_CREAT,
                                            size=self.segment_size)
            semaphore = posix_ipc.Semaphore(next_name, posix_ipc.O_CREAT)
            mapfile = mmap.mmap(memory.fd, memory.size)
            memory.close_fd()

            semaphore.release()
            self.shared_memories[next_name] = SharedMemory(memory, semaphore,
                                                           mapfile)

    def get_next_shared_memory_name(self) -> str:
        return self.memory_id_gen.get_next()

    def cleanup(self):
        """Cleans all of the allocated shared memories to free up the ram.

        """

        for _ in range(self.max_segment_count):
            name_to_unlink = self.memory_id_gen.get_next()
            if name_to_unlink in self.shared_memories:
                self._destroy_memory(name_to_unlink)

    def _destroy_memory(self, memory_to_destroy: str):
        """Destroys a specified shared memory.

        Args:
            memory_to_destroy: The name of the existing shared memory.

        """

        self.shared_memories[memory_to_destroy].free_memory()
        self.shared_memories.pop(memory_to_destroy)
