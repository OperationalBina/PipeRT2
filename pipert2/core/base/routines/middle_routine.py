from functools import partial
from abc import ABCMeta, abstractmethod
from pipert2.core.base.data import Data
from pipert2.core.base.routines.fps_routine import FPSRoutine


class MiddleRoutine(FPSRoutine, metaclass=ABCMeta):

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
            try:
                main_logic_callable = partial(self.main_logic, message.get_data())
                output_data = self._run_main_logic_with_durations_updating(main_logic_callable)
            except Exception as error:
                self._logger.exception(f"The routine has crashed: {error}")
            else:
                if output_data is not None:
                    message.update_data(output_data)
                    self.message_handler.put(message)
