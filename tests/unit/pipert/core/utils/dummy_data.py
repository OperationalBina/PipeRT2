from pipert2 import dataclass, field
from pipert2.core.base.data import Data


@dataclass
class DummyData(Data):
    name: str = field(default="")
    my_list: list = field(default_factory=list)


data = DummyData(name="Doctest")
