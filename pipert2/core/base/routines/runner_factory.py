from functools import partial
import types
from typing import Callable
from pipert2.core.base.message import Message
from pipert2.core.base.routine import Routine


GENERATOR_EXTENDED_RUN = "generator_extended_run"
INNER_EXTENDED_RUN = "inner_extended_run"
FINAL_EXTENDED_RUN = "final_extended_run"


class RunnerFactory:
    def __init__(self) -> None:
        self.runner_mappings = {
            GENERATOR_EXTENDED_RUN: _generator_extended_run,
            INNER_EXTENDED_RUN: _inner_extended_run,
            FINAL_EXTENDED_RUN: _final_extended_run
        }

    def get_runner_for_type(self, type: str, routine: Routine) -> Callable:
        # Bounding method to class instance
        return types.MethodType(self.runner_mappings[type], routine)


def _generator_extended_run(self):
    try:
        main_logic_callable = partial(self.main_logic)
        output_data = self._run_main_logic_with_durations_updating(
            main_logic_callable)

    except Exception as error:
        self._logger.exception(f"The routine has crashed: {error}")
    else:
        if output_data is not None:
            message = Message(output_data, source_address=self.name)
            self.message_handler.put(message)


def _inner_extended_run(self):
    message = self.message_handler.get()
    if message is not None:
        try:
            main_logic_callable = partial(self.main_logic, message.get_data())
            output_data = self._run_main_logic_with_durations_updating(
                main_logic_callable)
        except Exception as error:
            self._logger.exception(f"The routine has crashed: {error}")
        else:
            if output_data is not None:
                message.update_data(output_data)
                self.message_handler.put(message)


def _final_extended_run(self):
    message = self.message_handler.get()
    if message is not None:
        try:
            main_logic_callable = partial(self.main_logic, message.get_data())
            self._run_main_logic_with_durations_updating(main_logic_callable)
        except Exception as error:
            self._logger.exception(f"The routine has crashed: {error}")
