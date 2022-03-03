import numpy as np
from abc import abstractmethod
from pipert2.core import Data


class FrameData(Data):

    @abstractmethod
    def get_frame(self) -> np.array:
        pass
