import posix_ipc
import mmap
import os
from pipert2.utils.shared_memory.memory_id_iterator import MemoryIdIterator
from pipert2.utils.shared_memory.shared_memory import SharedMemory


def get_shared_memory_object(name):
    """
    Get a SharedMemory object that correlates to the name given.
    Args:
        name: The name of a shared memory.
    Returns: A SharedMemory object.
    """
    try:
        memory = posix_ipc.SharedMemory(name)
        semaphore = posix_ipc.Semaphore(name)
    except posix_ipc.ExistentialError:
        return None
    except Exception:
        return None

    mapfile = mmap.mmap(memory.fd, memory.size)

    memory.close_fd()

    semaphore.release()

    return SharedMemory(memory, semaphore, mapfile)


class SharedMemoryGenerator:
    """
    Generates a set 'max_count' amount of shared memories to be used.
    """
    def __init__(self, max_segment_count, segment_size):
        self.memory_id_gen = MemoryIdIterator(os.getpid(), max_segment_count)
        self.max_segment_count = max_segment_count
        self.shared_memories = {}
        self.segment_size = segment_size

    def create_memories(self):
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

    def get_next_shared_memory_name(self):
        return self.memory_id_gen.get_next()

    def cleanup(self):
        """
        Cleans all of the allocated shared memories to free up the ram.
        """
        for _ in range(self.max_segment_count):
            name_to_unlink = self.memory_id_gen.get_next()
            if name_to_unlink in self.shared_memories:
                self._destroy_memory(name_to_unlink)

    def _destroy_memory(self, memory_to_destroy):
        """
        Destroys a specified shared memory.
        Args:
            memory_to_destroy: The name of the existing shared memory.
        """
        self.shared_memories[memory_to_destroy].free_memory()
        self.shared_memories.pop(memory_to_destroy)
