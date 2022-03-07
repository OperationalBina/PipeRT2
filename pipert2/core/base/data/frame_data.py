import numpy as np
from abc import abstractmethod
from pipert2.core.base.data.data import Data


class FrameData(Data):
    """Base class used for transferring frames while using the cockpit system (Refer to docs).
    In order to use the cockpit properly you MUST implement the get_frame method. Example usage:
    >>>class Frame(FrameData):
    >>>     def __init__(self, frame, frame_number):
    >>>         super().__init__()
    >>>         self.frame = frame
    >>>         self.frame_number = frame_number
    >>>
    >>>     def get_frame(self) -> np.array:
    >>>         return self.frame

    """

    @abstractmethod
    def get_frame(self) -> np.array:
        pass
