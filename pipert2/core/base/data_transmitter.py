from abc import ABC, abstractmethod
from pipert2.core.base.data import Data


class DataTransmitter(ABC):
    """The data transmitter provides functions that indicate how data will flow through a connection between 2 routines.

    """

    @abstractmethod
    def transmit(self) -> callable:
        """The transmit function returns a function that manages the data transfer of a message payload data.

        Returns:
            A function that parses and transmits the given data from a payload.

        """

        def func(data: Data):
            raise NotImplementedError

        return func

    @abstractmethod
    def receive(self) -> callable:
        """The receive function returns a function that can manage to read data in the reverse fashion of the transmit
        method.

        Returns:
            A function that parses and receives the given data from a payload.

        """

        def func(data: Data):
            raise NotImplementedError

        return func
