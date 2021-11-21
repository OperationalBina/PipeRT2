import pytest
import collections
from multiprocessing import Manager
from pipert2.core.base.message import Message
from pipert2.core.base.transmitters import BasicTransmitter
from pipert2.core.handlers.message_handlers import QueueHandler


@pytest.fixture()
def input_queue():
    input_queue = Manager().Queue(maxsize=1)
    return input_queue


@pytest.fixture()
def output_queue():
    output_queue = Manager().Queue(maxsize=1)
    return output_queue


@pytest.fixture()
def blocking_queue_handler(input_queue, output_queue):
    blocking_queue_handler = QueueHandler("dummy", put_block=True, get_block=True, timeout=1)
    blocking_queue_handler.input_queue = input_queue
    blocking_queue_handler.output_queue = output_queue
    blocking_queue_handler.transmit = BasicTransmitter().transmit()
    blocking_queue_handler.receive = BasicTransmitter().receive()

    return blocking_queue_handler


@pytest.fixture()
def non_blocking_queue_handler(input_queue, output_queue):
    non_blocking_queue_handler = QueueHandler("dummy", put_block=True, get_block=True)
    non_blocking_queue_handler.input_queue = input_queue
    non_blocking_queue_handler.output_queue = output_queue
    non_blocking_queue_handler.transmit = BasicTransmitter().transmit()
    non_blocking_queue_handler.receive = BasicTransmitter().receive()

    return non_blocking_queue_handler


def test_put(blocking_queue_handler, non_blocking_queue_handler, output_queue):
    message = StrMessage("Test Message", "dummy")
    blocking_queue_handler.put(message)
    assert Message.decode(output_queue.get()) == message
    non_blocking_queue_handler.put(message)
    assert Message.decode(output_queue.get()) == message


def test_get(blocking_queue_handler, non_blocking_queue_handler, input_queue):
    message = StrMessage("Test Message", "dummy")
    input_queue.put(Message.encode(message))
    assert blocking_queue_handler.get() == message
    input_queue.put(Message.encode(message))
    assert non_blocking_queue_handler.get() == message
    assert blocking_queue_handler.get() is None
    assert non_blocking_queue_handler.get() is None


def test_force_push(non_blocking_queue_handler, output_queue):
    assert output_queue.empty()
    non_blocking_queue_handler.put(StrMessage("Test Message", "dummy"))
    assert output_queue.full()

    my_msg = StrMessage("Test Message", "dummy")
    non_blocking_queue_handler.put(my_msg)

    assert Message.decode(output_queue.get()) == my_msg


def test_sequential_writing_to_queue(non_blocking_queue_handler, output_queue):
    assert output_queue.empty()

    for index in range(1000):
        new_msg = StrMessage(f"Test Message: {index}", "dummy")
        non_blocking_queue_handler.put(new_msg)
        assert Message.decode(output_queue.get()) == new_msg


def test_safe_push(blocking_queue_handler, output_queue):
    message1 = StrMessage("Test Message 1", "dummy")
    message2 = StrMessage("Test Message 2", "dummy")
    blocking_queue_handler.put(message1)
    blocking_queue_handler.put(message2)
    assert Message.decode(output_queue.get()) == message1


def test_record_entry(blocking_queue_handler, non_blocking_queue_handler, input_queue):
    blocking_message = StrMessage("Blocking Message", "blocking")
    non_blocking_message = StrMessage("Non Blocking Message", "non blocking")
    input_queue.put(Message.encode(blocking_message))
    assert blocking_queue_handler.get().history["dummy"]
    input_queue.put(Message.encode(non_blocking_message))
    assert non_blocking_queue_handler.get().history["dummy"]


def test_put_no_transmit_method(blocking_queue_handler, non_blocking_queue_handler, output_queue):
    message = StrMessage("Test Message", "dummy")
    blocking_queue_handler.transmit = None
    non_blocking_queue_handler.transmit = None
    blocking_queue_handler.put(message)
    assert Message.decode(output_queue.get()) == message
    non_blocking_queue_handler.put(message)
    assert Message.decode(output_queue.get()) == message


def test_get_no_receive_method(blocking_queue_handler, non_blocking_queue_handler, input_queue):
    message = StrMessage("Test Message", "dummy")
    blocking_queue_handler.receive = None
    non_blocking_queue_handler.receive = None
    input_queue.put(Message.encode(message))
    assert blocking_queue_handler.get() == message
    input_queue.put(Message.encode(message))
    assert non_blocking_queue_handler.get() == message
    assert blocking_queue_handler.get() is None
    assert non_blocking_queue_handler.get() is None


class StrMessage(Message):
    def __init__(self, data: collections.Mapping, source_address: str):
        super().__init__(data, source_address)

    def __eq__(self, other):
        return self.payload.data == other.payload.data
