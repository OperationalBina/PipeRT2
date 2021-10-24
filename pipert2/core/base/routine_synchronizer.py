from abc import abstractmethod

from pipert2.utils.interfaces import EventExecutorInterface


class RoutineSynchronizer(EventExecutorInterface):

    @abstractmethod
    def build(self):
        """Build the routine synchronizer.

        """

        raise NotImplementedError

    @abstractmethod
    def join(self):
        """Join routine synchronizer process.

        """

        raise NotImplementedError

    @abstractmethod
    def run_synchronized(self, routine_callable: callable, routine_name: str):
        """Synchronizing and run the routine callable.

        Args:
            routine_callable: The routine callable.
            routine_name: The routine name.
        """

        raise NotImplementedError
