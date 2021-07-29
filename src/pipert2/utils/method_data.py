from dataclasses import dataclass, field


@dataclass
class Method:
    name: str
    params: dict = field(default_factory=lambda: {})
