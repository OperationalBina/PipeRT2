from src.pipert2.core import DataTransmitter


class BasicTransmitter(DataTransmitter):
    """Simple implementation for data transmitters.

    """

    def transmit(self):
        """A simple transmit function.

        Returns:
            A lambda function that does nothing.

        """

        return lambda data: data

    def receive(self):
        """A simple receive function.

        Returns:
            A lambda function that does nothing.

        """

        return lambda data: data
