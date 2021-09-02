from typing import Optional
from src.pipert2.utils.consts.event_format import EVENT_SEPARATOR, EVENT_INDEX, FLOW_INDEX, EVENT_CONTAIN_ROUTINE_LENGTH, \
    ROUTINE_INDEX


class Method:
    """The method class uses for describing event command and his parameters.
    Using methods we notify on events through the pipeline components.
    """

    def __init__(self, name: str, params: dict = {}):
        """
        Args:
            name (str): The method name in format - { event-flow_name-routine_name }.
            params (dict): Dictionary of method parameters, default is empty dictionary.
        """

        self.name = name
        self.params = params

    def is_valid_by_flow(self, flow_to_validate: str) -> bool:
        """Determine if a specific flow can run the current method.

        Args:
            flow_to_validate: Flow name to validate.

        Returns:
            True if there is no specific flow mentioned or if the specific flow mentioned equals to parameter,
            False if flows aren't match.
        """

        if self._is_contain_specific_flow():
            flow_name = self.name.split(EVENT_SEPARATOR)[FLOW_INDEX]
            is_flow_valid = flow_to_validate == flow_name
        else:
            is_flow_valid = True

        return is_flow_valid

    def create_base_method(self):
        """Create base method if flow mentioned specific flow/routine.

        Returns:
            If the current method represented by the format (name: { event-flow_name-routine_name }, params),
            then return the base format as (name: {event}, params)
        """

        event = self.name.split(EVENT_SEPARATOR)[EVENT_INDEX]

        return Method(name=event, params=self.params)

    def get_routine_name(self) -> Optional[str]:
        """Get the routine name from the method name if existed.

        Returns:
            Routine name if mentioned, None if didn't.
        """

        if len(self.name.split(EVENT_SEPARATOR)) == EVENT_CONTAIN_ROUTINE_LENGTH:
            routine_name = self.name.split(EVENT_SEPARATOR)[ROUTINE_INDEX]
        else:
            routine_name = None

        return routine_name

    def _is_contain_specific_flow(self) -> bool:
        event_commands = len(self.name.split(EVENT_SEPARATOR))

        return event_commands > 1

    def __eq__(self, other) -> bool:
        return other.name == self.name and other.params == self.params
