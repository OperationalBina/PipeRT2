from functools import partial
from abc import ABCMeta, abstractmethod
from pipert2.core.base.data import Data
from pipert2.core.base.routines.fps_routine import FPSRoutine


class DestinationRoutine(FPSRoutine, metaclass=ABCMeta):

    @abstractmethod
    def main_logic(self, data: Data) -> None:
        """Main logic of the routine.

            Args:
                data: The main logic parameter.
        """

        raise NotImplementedError

    def _extended_run(self) -> None:
        message = self.message_handler.get()
        if message is not None:
            try:
                main_logic_callable = partial(self.main_logic, message.get_data())
                self._run_main_logic_with_durations_updating(main_logic_callable)
            except Exception as error:
                self._logger.exception(f"The routine has crashed: {error}")
