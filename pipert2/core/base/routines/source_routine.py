from functools import partial
from abc import ABCMeta, abstractmethod
from pipert2.core.base.data import Data
from pipert2.core.base.message import Message
from pipert2.core.base.routines.fps_routine import FPSRoutine


class SourceRoutine(FPSRoutine, metaclass=ABCMeta):

    @abstractmethod
    def main_logic(self) -> Data:
        """Routine that starts generate data.

            Returns:
                The generated data.
        """

        raise NotImplementedError

    def _extended_run(self) -> None:
        """Wrapper method for executing the entire routine logic

        """

        try:
            main_logic_callable = partial(self.main_logic)
            output_data = self._run_main_logic_with_durations_updating(main_logic_callable)
        except Exception as error:
            self._logger.exception(f"The routine has crashed: {error}")
        else:
            if output_data is not None:
                message = Message(output_data, source_address=self.name)
                self.message_handler.put(message)
