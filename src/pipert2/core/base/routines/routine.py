from abc import ABCMeta, abstractmethod
from src.pipert2.core.base.routines.routine_wrapper import RoutineWrapper


class Routine(RoutineWrapper, metaclass=ABCMeta):

    @abstractmethod
    def main_logic(self, param) -> any:
        """Main logic of the routine.

        Args:
            param: The main logic parameter.

        Returns:
            The main logic result.
        """

        raise NotImplementedError

    def _extended_run(self) -> None:
        self.setup()

        while not self.stop_event.is_set():
            message = self.message_handler.get()
            try:
                output_data = self.main_logic(message.get_payload())
            except Exception as error:
                self._logger.exception(f"The routine has crashed: {error}")
            else:
                message.update_payload(output_data)
                self.message_handler.put(message)

        self.cleanup()
