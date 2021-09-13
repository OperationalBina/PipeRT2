from abc import ABCMeta, abstractmethod
from src.pipert2.core.base.routines.routine_wrapper import RoutineWrapper


class EndRoutine(RoutineWrapper, metaclass=ABCMeta):

    @abstractmethod
    def main_logic(self, param) -> None:
        """Main logic of the routine.

            Args:
                param: The main logic parameter.
        """

        raise NotImplementedError

    def _extended_run(self) -> None:
        self.setup()

        while not self.stop_event.is_set():
            message = self.message_handler.get()
            try:
                self.main_logic(message.get_payload())
            except Exception as error:
                self._logger.exception(f"The routine has crashed: {error}")

        self.cleanup()
