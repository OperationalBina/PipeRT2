import sys

if sys.version_info.minor >= 7:
    from dataclasses import dataclass, field
else:
    from src.pipert2.utils.data_class.dataclasses import dataclass, field


@dataclass
class Method:
    event_name: str
    flow_name: str = None
    routine_name: str = None
    params: dict = field(default_factory=lambda: {})
