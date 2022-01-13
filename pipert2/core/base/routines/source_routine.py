import logging
from functools import partial
from abc import ABCMeta, abstractmethod
from pipert2.core.base.data import Data
from pipert2.core.base.message import Message
from pipert2.core.base.routines.fps_routine import FPSRoutine
from pipert2.utils.exceptions.main_logic_not_exist_error import MainLogicNotExistError


class SourceRoutine(FPSRoutine, metaclass=ABCMeta):
    """Source Routine is generating messages and sending them out to the next routine.

    Implementation example:

    >>> class MySourceRoutine(SourceRoutine):
    ...
    ...     @SourceRoutine.main_logics
    ...     def generate_data(self) -> Data:
    ...         self._logger.info("Creating new data")
    ...         data = Data()
    ...         data.additional_data = {"Created at": "Now"}
    ...         return data

    """

    def _extended_run(self) -> None:
        """Wrapper method for executing the entire routine logic

        """

        try:
            main_logic_callback = self._get_main_logic_callback()
            main_logic_callable = partial(main_logic_callback)
            output_data = self._run_main_logic_with_durations_updating(main_logic_callable)
        except MainLogicNotExistError:
            self._logger.error("No method was marked as main logic !!")
        except Exception as error:
            self._logger.exception(f"The routine has crashed: {error}")
        else:
            if output_data is not None:
                message = Message(output_data, source_address=self.name)
                self.message_handler.put(message)
