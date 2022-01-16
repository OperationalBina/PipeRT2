import json
from typing import Dict, Optional
from collections import defaultdict
from pipert2 import dataclass, field


@dataclass
class Method:
    def __init__(self, event_name, specific_flow_routines=None, params=None):
        self.event_name = event_name

        if specific_flow_routines is None:
            self.specific_flow_routines = defaultdict(list)
        elif isinstance(specific_flow_routines, str):
            self.specific_flow_routines = json.loads(specific_flow_routines)
        else:
            self.specific_flow_routines = specific_flow_routines

        if params is None:
            self.params = {}
        else:
            self.params = params

    def is_applied_on_flow(self, flow_name_to_validate: str):
        """Check if current method apply on the given flow.

        Args:
            flow_name_to_validate: The flow name to validate.

        Returns:
            True if flow can run, false otherwise.
        """

        if self.specific_flow_routines is not None and any(self.specific_flow_routines):
            return flow_name_to_validate in self.specific_flow_routines
        else:
            return True

    def is_applied_on_specific_routines(self, flow_name_to_validate: str):
        """Check if current method applies on specific routines.

        Args:
            flow_name_to_validate: The flow name to validate.

        Returns:
            True if method applies on specific routines, false otherwise.
        """

        if self.specific_flow_routines is not None and any(self.specific_flow_routines):
            return flow_name_to_validate in self.specific_flow_routines and \
                   self.specific_flow_routines.get(flow_name_to_validate)
        else:
            return False
