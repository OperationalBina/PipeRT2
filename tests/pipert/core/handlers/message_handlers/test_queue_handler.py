import pytest
from multiprocessing import Manager
from src.pipert2.core.handlers.message_handlers.queue_handler import QueueHandler
from src.pipert2.core.base.message import Message


@pytest.fixture()
def dummy_message():
    return Message()


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
    blocking_queue_handler = QueueHandler(input_queue, output_queue, blocking=True, timeout=1)

    return blocking_queue_handler


@pytest.fixture()
def non_blocking_queue_handler(input_queue, output_queue):
    non_blocking_queue_handler = QueueHandler(input_queue, output_queue, blocking=False)

    return non_blocking_queue_handler


def test_put(blocking_queue_handler, non_blocking_queue_handler, output_queue):
    blocking_queue_handler.put(dummy_message)
    assert output_queue.get() == dummy_message
    non_blocking_queue_handler.put(dummy_message)
    assert output_queue.get() == dummy_message


def test_get(blocking_queue_handler, non_blocking_queue_handler, input_queue):
    input_queue.put(dummy_message)
    assert blocking_queue_handler.get() == dummy_message
    input_queue.put(dummy_message)
    assert non_blocking_queue_handler.get() == dummy_message
    assert blocking_queue_handler.get() is None
    assert non_blocking_queue_handler.get() is None


def test_force_push(non_blocking_queue_handler, output_queue, dummy_message):
    assert output_queue.empty()
    non_blocking_queue_handler.put(StrMessage("Test Message"))
    assert output_queue.full()

    my_msg = StrMessage("Test Message")
    non_blocking_queue_handler.put(my_msg)

    assert output_queue.get() == my_msg


def test_sequential_writing_to_queue(non_blocking_queue_handler, output_queue):
    assert output_queue.empty()

    for index in range(1000):
        new_msg = StrMessage(f"Test Message: {index}")
        non_blocking_queue_handler.put(new_msg)
        assert output_queue.get() == new_msg


def test_safe_push(blocking_queue_handler, output_queue):
    message1 = StrMessage("Test Message 1")
    message2 = StrMessage("Test Message 2")
    blocking_queue_handler.put(message1)
    blocking_queue_handler.put(message2)
    assert output_queue.get() == message1


class StrMessage(Message):
    def __init__(self, content):
        self.content = content

    def __eq__(self, other):
        return self.content == other.content
