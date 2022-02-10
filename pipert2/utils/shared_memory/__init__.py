import sys

if sys.version_info.minor <= 7:
    from pipert2.utils.shared_memory.posix_ipc.shared_memory_manager import SharedMemoryManager
else:
    pass