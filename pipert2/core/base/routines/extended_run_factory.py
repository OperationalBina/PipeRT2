from typing import Callable
from functools import partial
from pipert2.core.base.message import Message
from pipert2.utils.consts import GENERATOR_ROUTINE, INNER_ROUTINE, FINAL_ROUTINE


def get_runner_for_type(routine_type: str) -> Callable:
    runner_mappings = {
        GENERATOR_ROUTINE: _generator_extended_run,
        INNER_ROUTINE: _inner_extended_run,
        FINAL_ROUTINE: _final_extended_run
    }

    return runner_mappings[routine_type]


def _generator_extended_run(self):
    try:
        main_logic_callable = partial(self.main_logic, None)
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
