from abc import ABCMeta, abstractmethod
from pipert2.core.base.message import Message
from pipert2.core.base.routine import Routine


class SourceRoutine(Routine, metaclass=ABCMeta):

    @abstractmethod
    def main_logic(self) -> dict:
        """Routine that starts generate data.

            Returns:
                The generated data.
        """

        raise NotImplementedError

    def _extended_run(self) -> None:
        """Wrapper method for executing the entire routine logic

        """

        try:
            output_data = self.main_logic()
        except Exception as error:
            self._logger.exception(f"The routine has crashed: {error}")
        else:
            if output_data is not None:
                message = Message(output_data, source_address=self.name)
                self.message_handler.put(message)
