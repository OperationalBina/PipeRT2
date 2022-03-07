class Data:
    """Base class for transportation of data within the pipeline.
    User can implement Data classes for customizing types.

    Example usage:
    >>> import numpy as np
    >>> class DataTransferObject(Data):
    >>>     def __init__(self, name, data, additional_data):
    >>>         super().__init__(additional_data=additional_data)
    >>>         self.name = name
    >>>         self.data = data

    """

    def __init__(self, additional_data=None):
        if additional_data is None:
            additional_data = {}

        self.additional_data = additional_data
