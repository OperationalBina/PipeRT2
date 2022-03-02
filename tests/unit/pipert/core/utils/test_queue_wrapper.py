import time
import pytest
from queue import Queue as thQueue, Empty
from multiprocessing import Queue as mpQueue

from pipert2 import Data

from pipert2.core import Message

from pipert2.utils.queue_utils.queue_wrapper import QueueWrapper


@pytest.fixture()
def dummy_queue_wrapper():
    dummy_queue_wrapper = QueueWrapper()

    return dummy_queue_wrapper


def test_get_queue_process_safe(dummy_queue_wrapper):
    return_queue = dummy_queue_wrapper.get_queue(process_safe=True)

    assert isinstance(return_queue, type(mpQueue()))

    dummy_queue_wrapper.kill_queue_worker()


def test_get_queue_not_process_safe(dummy_queue_wrapper):
    return_queue = dummy_queue_wrapper.get_queue(process_safe=False)

    assert isinstance(return_queue, type(thQueue()))


def test_get_from_threading_and_processing_queue(dummy_queue_wrapper):
    thread_queue = dummy_queue_wrapper.get_queue(process_safe=False)
    process_queue = dummy_queue_wrapper.get_queue(process_safe=True)

    test_message = Message("message", source_address="test")

    thread_queue.put(test_message)
    time.sleep(0.1)
    assert dummy_queue_wrapper.get(block=False, timeout=1).payload.data == test_message.payload.data

    process_queue.put(Message.encode(test_message))
    time.sleep(0.1)
    assert dummy_queue_wrapper.get(block=True, timeout=1).payload.data == test_message.payload.data

    with pytest.raises(Empty):
        dummy_queue_wrapper.get(block=True, timeout=1)

    dummy_queue_wrapper.kill_queue_worker()
