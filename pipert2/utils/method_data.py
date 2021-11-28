from typing import Dict, Optional
from collections import defaultdict
from pipert2 import dataclass, field


@dataclass
class Method:
    event_name: str
    specific_flow_routines: Dict[str, Optional[list]] = field(default_factory=lambda: defaultdict(list))
    params: dict = field(default_factory=lambda: {})

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
