import pytest
from mock import Mock, call
from pytest_mock import MockerFixture

from pipert2.utils.queue_utils.publish_queue import PublishQueue
from pipert2.utils.queue_utils.queue_wrapper import QueueWrapper
from pipert2.core.managers.networks.queue_network import QueueNetwork


@pytest.fixture
def dummy_queue_network():
    dummy_queue_network = QueueNetwork()

    return dummy_queue_network


def test_get_message_handler(dummy_queue_network):
    message_handler = dummy_queue_network.get_message_handler("dummy")

    assert message_handler.routine_name == "dummy"

    message_handler2 = dummy_queue_network.get_message_handler("dummy")

    assert message_handler == message_handler2


def test_link_mix_process_safe_and_thread_safe_multiple_destinations(dummy_queue_network, mocker: MockerFixture):
    source_routine = Mock()
    source_routine.flow_name = "dummy1"
    source_routine.message_handler.output_queue = PublishQueue()

    des1_routine = mocker.MagicMock()
    des1_msg_handler = mocker.MagicMock()
    des1_input_queue = mocker.MagicMock()
    des1_routine.name = "des1"
    des1_routine.message_handler = des1_msg_handler
    des1_msg_handler.get_receiver.return_value = des1_input_queue

    des2_routine = mocker.MagicMock()
    des2_msg_handler = mocker.MagicMock()
    des2_input_queue = mocker.MagicMock()
    des2_routine.name = "des2"
    des2_routine.message_handler = des2_msg_handler
    des2_msg_handler.get_receiver.return_value = des2_input_queue

    destination_routines = (des1_routine, des2_routine)

    for destination_routine in destination_routines:
        destination_routine.input_queue = QueueWrapper()

    destination_routines[0].flow_name = "dummy1"
    destination_routines[1].flow_name = "dummy2"
    data_transmitter = Mock()

    dummy_queue_network.link(source_routine, destination_routines, data_transmitter)

    assert type(source_routine.message_handler.output_queue) == PublishQueue
    assert source_routine.message_handler.link.call_args_list == [call("des1", des1_input_queue), call("des2", des2_input_queue)]
    des1_msg_handler.get_receiver.assert_called_with(False)
    des2_msg_handler.get_receiver.assert_called_with(True)


def test_link_multiple_process_safe_multiple_destinations(dummy_queue_network, mocker: MockerFixture):
    source_routine = Mock()
    source_routine.flow_name = "dummy1"
    source_routine.message_handler.output_queue = PublishQueue()

    des1_routine = mocker.MagicMock()
    des1_msg_handler = mocker.MagicMock()
    des1_input_queue = mocker.MagicMock()
    des1_routine.name = "des1"
    des1_routine.message_handler = des1_msg_handler
    des1_msg_handler.get_receiver.return_value = des1_input_queue

    des2_routine = mocker.MagicMock()
    des2_msg_handler = mocker.MagicMock()
    des2_input_queue = mocker.MagicMock()
    des2_routine.name = "des2"
    des2_routine.message_handler = des2_msg_handler
    des2_msg_handler.get_receiver.return_value = des2_input_queue

    destination_routines = (des1_routine, des2_routine)

    for destination_routine in destination_routines:
        destination_routine.input_queue = QueueWrapper()

    destination_routines[0].flow_name = "dummy2"
    destination_routines[1].flow_name = "dummy2"
    data_transmitter = Mock()

    dummy_queue_network.link(source_routine, destination_routines, data_transmitter)

    assert type(source_routine.message_handler.output_queue) == PublishQueue
    assert source_routine.message_handler.link.call_args_list == [call("des1", des1_input_queue), call("des2", des2_input_queue)]
    des1_msg_handler.get_receiver.assert_called_with(True)
    des2_msg_handler.get_receiver.assert_called_with(True)


def test_link_multiple_thread_safe_multiple_destinations(dummy_queue_network, mocker: MockerFixture):
    source_routine = Mock()
    source_routine.flow_name = "dummy1"
    source_routine.message_handler.output_queue = PublishQueue()

    des1_routine = mocker.MagicMock()
    des1_msg_handler = mocker.MagicMock()
    des1_input_queue = mocker.MagicMock()
    des1_routine.name = "des1"
    des1_routine.message_handler = des1_msg_handler
    des1_msg_handler.get_receiver.return_value = des1_input_queue

    des2_routine = mocker.MagicMock()
    des2_msg_handler = mocker.MagicMock()
    des2_input_queue = mocker.MagicMock()
    des2_routine.name = "des2"
    des2_routine.message_handler = des2_msg_handler
    des2_msg_handler.get_receiver.return_value = des2_input_queue

    destination_routines = (des1_routine, des2_routine)

    for destination_routine in destination_routines:
        destination_routine.input_queue = QueueWrapper()

    destination_routines[0].flow_name = "dummy1"
    destination_routines[1].flow_name = "dummy1"
    data_transmitter = Mock()

    dummy_queue_network.link(source_routine, destination_routines, data_transmitter)

    assert type(source_routine.message_handler.output_queue) == PublishQueue
    assert source_routine.message_handler.link.call_args_list == [call("des1", des1_input_queue), call("des2", des2_input_queue)]
    des1_msg_handler.get_receiver.assert_called_with(False)
    des2_msg_handler.get_receiver.assert_called_with(False)

