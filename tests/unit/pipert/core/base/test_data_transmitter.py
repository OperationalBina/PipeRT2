import sys
import pytest
import numpy as np
from pipert2.core.base.data import Data
from pipert2.core.base.transmitters import BasicTransmitter


@pytest.fixture
def dummy_shared_memory_transmitter():
    from pipert2.core.base.transmitters import SharedMemoryTransmitter
    if sys.version_info.minor <= 7:
        dummy_shared_memory_transmitter = SharedMemoryTransmitter()
    else:
        dummy_shared_memory_transmitter = SharedMemoryTransmitter()  # TODO: Change to multiprocessing

    return dummy_shared_memory_transmitter


@pytest.fixture
def dummy_basic_data_transmitter():
    dummy_basic_data_transmitter = BasicTransmitter()
    return dummy_basic_data_transmitter


def test_shared_memory_transmit_receive(dummy_shared_memory_transmitter):
    if sys.version_info.minor <= 7:  # TODO: Add multiprocessing test
        transmit_func = dummy_shared_memory_transmitter.transmit()
        receive_func = dummy_shared_memory_transmitter.receive()

        data = Data()
        data.additional_data = {"data": b"AAA" * 5000, "short_data": b"AAA"}

        return_data = transmit_func(data)
        assert data == receive_func(return_data)

        data_to_transmit = np.ones((dummy_shared_memory_transmitter.data_size_threshold,), dtype=np.uint8)
        data.additional_data = {"test": data_to_transmit}

        return_data = transmit_func(data)
        assert data == receive_func(return_data)

        data.additional_data = {"data": b"AAA" * 100, "short_data": b"AAA", "address": "Makabim"}
        return_data = transmit_func(data)
        assert data == receive_func(return_data)


def test_basic_transmit_receive(dummy_basic_data_transmitter):
    transmit_func = dummy_basic_data_transmitter.transmit()
    receive_func = dummy_basic_data_transmitter.receive()

    data = {"data": b"AAA" * 5000, "short_data": b"AAA"}
    return_data = transmit_func(data)
    assert data == receive_func(return_data)
