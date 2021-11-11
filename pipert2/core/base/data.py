from pipert2 import dataclass, field


@dataclass
class Data:
    """ase class for transportation of data within the pipeline.
    User can implement Data classes for customizing types.

    Example usage:
    >>> import numpy as np
    >>> @dataclass
    ... class FrameData(Data):
    ...     frame: np.ndarray
    ...     source: str

    >>> frame = np.zeros((4,5))
    >>> data = FrameData(frame=frame, source="Doctest")

    """

    additional_data: dict = field(default_factory=dict, init=False)
