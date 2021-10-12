import numpy as np
from pytest_mock import MockerFixture
from pipert2 import SharedMemoryTransmitter
from pipert2 import QueueNetwork, QueueHandler
from pipert2.utils.shared_memory_manager import SharedMemoryManager


def test_link_shared_memory_transmitter_to_destination_routines_message_handlers(mocker: MockerFixture):

    queue_network = QueueNetwork()

    source_routine = mocker.MagicMock()
    source_routine.message_handler = QueueHandler("source")

    first_destination_routine = mocker.MagicMock()
    first_destination_routine.message_handler = QueueHandler("first_destination")

    second_destination_routine = mocker.MagicMock()
    second_destination_routine.message_handler = QueueHandler("second_destination")

    queue_network.link(source=source_routine,
                       destinations=(first_destination_routine, second_destination_routine,),
                       data_transmitter=SharedMemoryTransmitter())

    input_sentence_in_bytes = b"test"

    address = SharedMemoryManager().write_to_mem(input_sentence_in_bytes)

    requested_data = {
        "test": {
            "address": address,
            "size": len(input_sentence_in_bytes)
        }
    }

    expected_value = {"test": input_sentence_in_bytes}

    assert first_destination_routine.message_handler.receive(requested_data) == expected_value
    assert second_destination_routine.message_handler.receive(requested_data) == expected_value


def test_link_shared_memory_transmitter_to_source_routine_message_handlers(mocker: MockerFixture):

    source_routine = mocker.MagicMock()
    source_routine.message_handler = QueueHandler("source")

    shared_memory_transmitter = SharedMemoryTransmitter()

    queue_network = QueueNetwork()
    queue_network.link(source=source_routine,
                       destinations=(mocker.MagicMock(),),
                       data_transmitter=shared_memory_transmitter)

    data_to_transmit = np.ones((shared_memory_transmitter.data_size_threshold,), dtype=np.uint8)
    memory_name = source_routine.message_handler.transmit({"test": data_to_transmit})

    expected_data_in_memory = bytes(data_to_transmit)

    assert SharedMemoryManager().read_from_mem(memory_name["test"]["address"],
                                               memory_name["test"]["size"]) == expected_data_in_memory
