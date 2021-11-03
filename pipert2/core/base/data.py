from pipert2 import dataclass, field


@dataclass
class Data:
    additional_data: dict = field(default_factory=dict, init=False)
