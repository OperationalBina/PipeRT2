from abc import ABCMeta, abstractmethod
from src.pipert2.core.base.message import Message
from src.pipert2.core.base.routine import Routine


class SourceRoutine(Routine, metaclass=ABCMeta):

    @abstractmethod
    def main_logic(self) -> dict:
        """Routine that starts generate data.

            Returns:
                The generated data.
        """

        raise NotImplementedError

    def _extended_run(self) -> None:
        try:
            output_data = self.main_logic()
        except Exception as error:
            self._logger.exception(f"The routine has crashed: {error}")
        else:
            message = Message(output_data, source_address=self.name)
            self.message_handler.put(message)
