import sys

from typing import Dict, Optional

if sys.version_info.minor >= 7:
    from dataclasses import dataclass, field
else:
    from src.pipert2.utils.data_class.dataclasses import dataclass, field


@dataclass
class Method:
    event_name: str
    routines_by_flow: Dict[str, Optional[list]] = None
    params: dict = field(default_factory=lambda: {})

    def is_flow_valid(self, flow_name_to_validate: str):
        if self.routines_by_flow:
            return flow_name_to_validate in self.routines_by_flow.keys()
        else:
            return True

    def is_contain_routines(self, flow_name_to_validate: str):
        if self.routines_by_flow:
            return flow_name_to_validate in self.routines_by_flow.keys() and \
                   self.routines_by_flow.get(flow_name_to_validate)
        else:
            return False
