from abc import ABCMeta, abstractmethod
from pipert2.core.base.data import Data
from pipert2.core.base.routine import Routine


class DestinationRoutine(Routine, metaclass=ABCMeta):

    def main_logic(self, data: Data) -> None:
        """Main logic of the routine.

            Args:
                data: The main logic parameter.
        """

        raise NotImplementedError("No logic for the Base Data class input was implemented")

    def _extended_run(self) -> None:
        message = self.message_handler.get()
        if message is not None:
            try:
                self.main_logic(message.get_data())
                main_logic_callbacks = self.main_logics.all(self.__class__)[message.get_data_type()]
                # for main_logic_callbacks
            except Exception as error:
                self._logger.exception(f"The routine has crashed: {error}")
