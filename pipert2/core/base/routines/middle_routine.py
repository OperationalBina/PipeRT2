from pipert2.core.base.data import Data
from pipert2.core.base.routine import Routine
from pipert2.utils.exceptions.main_logic_not_exist_error import MainLogicNotExistError


class MiddleRoutine(Routine):
    """Middle Routine is expecting messages processing them and sending them out to the next routine.

    Implementation example:

    >>> class MyMiddleRoutine(MiddleRoutine):
    ...
    ...     @MiddleRoutine.main_logics(Data)
    ...     def process_data(self, data: Data) -> Data:
    ...         self._logger.info(f"Processing the data {data}")
    ...         data.additional_data = {"Processed": True}
    ...         return data

    """

    def _extended_run(self) -> None:
        message = self.message_handler.get()
        if message is not None:
            try:
                main_logic_callback = self._get_main_logic_callback(message.get_data_type())
                output_data = main_logic_callback(self, message.get_data())
            except MainLogicNotExistError as error:
                self._logger.error(error)
            except Exception as error:
                self._logger.exception(f"The routine has crashed: {error}")
            else:
                if output_data is not None:
                    message.update_data(output_data)
                    self.message_handler.put(message)
