import sys

if sys.version_info.minor >= 7:
    from dataclasses import dataclass, field
else:
    from pipert2.utils.data_class.dataclasses import dataclass, field


@dataclass
class Data:
    additional_data: dict = field(default_factory=dict, init=False)