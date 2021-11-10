from pipert2.core.base.data import Data
from pipert2.core.base.routine import Routine
from pipert2.utils.exceptions.main_logic_not_exist_error import MainLogicNotExistError


class DestinationRoutine(Routine):
    """Destination Routine is only expecting messages and doesn't send any of them out.

    Implementation example:

    >>> class MyDestinationRoutine(DestinationRoutine):
    ...
    ...     @DestinationRoutine.main_logics(expected_input_type=Data)
    ...     def process_data(self, data: Data) -> None:
    ...         self._logger.info(f"Processing the data {data}, and not sending anything")

    """

    def _extended_run(self) -> None:
        message = self.message_handler.get()
        if message is not None:
            try:
                main_logic_callback = self._get_main_logic_callback(message.get_data_type())
                main_logic_callback(self, message.get_data())
            except MainLogicNotExistError as error:
                self._logger.error(error)
            except Exception as error:
                self._logger.exception(f"The routine has crashed: {error}")
