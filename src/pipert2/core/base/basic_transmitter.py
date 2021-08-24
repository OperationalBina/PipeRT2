from src.pipert2.core.base.data_transmitter import DataTransmitter


class BasicTransmitter(DataTransmitter):

    def transmit(self):
        return lambda data: data

    def receive(self):
        return lambda data: data
