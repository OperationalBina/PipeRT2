import time
from abc import ABCMeta, abstractmethod
from pipert2.core.base.data import Data
from pipert2.core.base.routine import Routine


class MiddleRoutine(Routine, metaclass=ABCMeta):

    @abstractmethod
    def main_logic(self, data) -> Data:
        """Process the given data to the routine.

        Args:
            data: The data that the routine processes and sends.

        Returns:
            The main logic result.
        """

        raise NotImplementedError

    def _extended_run(self) -> None:
        message = self.message_handler.get()
        if message is not None:

            duration = None

            try:
                output_data, duration = self.run_main_logic_with_durations_updating(self.main_logic, message.get_data())
            except Exception as error:
                self._logger.exception(f"The routine has crashed: {error}")
            else:
                if output_data is not None:
                    message.update_data(output_data)
                    self.message_handler.put(message)
            finally:
                return duration
