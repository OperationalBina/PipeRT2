import sys

if sys.version_info.minor <= 7:
    from .posix_ipc.shared_memory_manager import SharedMemoryManager
else:
    from .multiprocessing.shared_memory_manager import SharedMemoryManager
from .general import MemoryIdIterator, AbsSharedMemoryManager
