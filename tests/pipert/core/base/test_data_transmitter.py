import sys
import pytest
from src.pipert2.core.base.data_transmitter import DataTransmitter  # TODO: remove
from src.pipert2.core.base.basic_transmitter import BasicTransmitter


@pytest.fixture
def dummy_shared_memory_transmitter():
    if sys.version_info.minor <= 7:
        from src.pipert2.core.base.shared_memory_transmitter import SharedMemoryTransmitter
        dummy_shared_memory_transmitter = SharedMemoryTransmitter()
    else:
        dummy_shared_memory_transmitter = DataTransmitter()  # TODO: Change to multiprocessing

    return dummy_shared_memory_transmitter


@pytest.fixture
def dummy_basic_data_transmitter():
    dummy_basic_data_transmitter = BasicTransmitter()
    return dummy_basic_data_transmitter


def test_shared_memory_transmit_receive(dummy_shared_memory_transmitter):
    transmit_func = dummy_shared_memory_transmitter.transmit()
    receive_func = dummy_shared_memory_transmitter.receive()

    if sys.version_info.minor <= 7:  # TODO: Add multiprocessing test
        data = {"data": b"AAA" * 5000, "short_data": b"AAA"}
        return_data = transmit_func(data)
        assert data == receive_func(return_data)


def test_basic_transmit_receive(dummy_basic_data_transmitter):
    transmit_func = dummy_basic_data_transmitter.transmit()
    receive_func = dummy_basic_data_transmitter.receive()

    data = {"data": b"AAA" * 5000, "short_data": b"AAA"}
    return_data = transmit_func(data)
    assert data == receive_func(return_data)
