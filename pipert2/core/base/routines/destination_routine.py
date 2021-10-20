from abc import ABCMeta, abstractmethod
from pipert2.core.base.routine import Routine


class DestinationRoutine(Routine, metaclass=ABCMeta):

    @abstractmethod
    def main_logic(self, data: dict) -> None:
        """Main logic of the routine.

            Args:
                data: The main logic parameter.
        """

        raise NotImplementedError

    def _extended_run(self) -> None:
        message = self.message_handler.get()
        if message is not None:
            try:
                self.main_logic(message.get_data())
            except Exception as error:
                self._logger.exception(f"The routine has crashed: {error}")
