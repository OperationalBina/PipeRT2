from abc import abstractmethod
from pipert2.utils.singleton_abs import SingletonABCMeta


class AbsSharedMemoryManager(metaclass=SingletonABCMeta):
    """Abstract shared memory manager class that specifies what functions need to be implemented.

    """

    @abstractmethod
    def write_to_mem(self, data: bytes) -> str:
        raise NotImplementedError

    @abstractmethod
    def read_from_mem(self, mem_name: str, bytes_to_read: int) -> [bytes, None]:
        raise NotImplementedError

    @abstractmethod
    def cleanup_memory(self):
        raise NotImplementedError
