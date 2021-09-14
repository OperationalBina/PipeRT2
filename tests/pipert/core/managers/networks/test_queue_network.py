import pytest
from mock import Mock
from src.pipert2.utils.publish_queue import PublishQueue
from src.pipert2.core.managers.networks.queue_network import QueueNetwork


@pytest.fixture
def dummy_queue_network():
    dummy_queue_network = QueueNetwork()

    return dummy_queue_network


def test_get_message_handler(dummy_queue_network):
    message_handler = dummy_queue_network.get_message_handler("dummy")

    assert message_handler.routine_name == "dummy"

    message_handler2 = dummy_queue_network.get_message_handler("dummy")

    assert message_handler == message_handler2


def test_link_single_destination(dummy_queue_network):
    source_routine = Mock()
    destination_routine = (Mock(),)
    data_transmitter = Mock()

    dummy_queue_network.link(source_routine, destination_routine, data_transmitter)

    assert type(source_routine.message_handler.output_queue) == PublishQueue
    assert source_routine.message_handler.output_queue._queues[0] == destination_routine[0].message_handler.input_queue


def test_link_multiple_destinations(dummy_queue_network):
    source_routine = Mock()
    destination_routines = (Mock(), Mock())
    data_transmitter = Mock()

    dummy_queue_network.link(source_routine, destination_routines, data_transmitter)

    assert type(source_routine.message_handler.output_queue) == PublishQueue

    for index, routine in enumerate(destination_routines):
        assert source_routine.message_handler.output_queue._queues[index] == routine.message_handler.input_queue


def test_link_multiple_sources(dummy_queue_network):
    source_routine1 = Mock()
    source_routine2 = Mock()
    destination_routines = (Mock(),)
    data_transmitter = Mock()

    dummy_queue_network.link(source_routine1, destination_routines, data_transmitter)
    dummy_queue_network.link(source_routine2, destination_routines, data_transmitter)

    for index, routine in enumerate(destination_routines):
        assert source_routine1.message_handler.output_queue._queues[index] == routine.message_handler.input_queue
        assert source_routine2.message_handler.output_queue._queues[index] == routine.message_handler.input_queue
