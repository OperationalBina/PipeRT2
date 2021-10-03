import pytest
from queue import Queue as thQueue
from multiprocessing import Queue as mpQueue
from src.pipert2.utils.queue_wrapper import QueueWrapper


@pytest.fixture()
def dummy_queue_wrapper():
    dummy_queue_wrapper = QueueWrapper()

    return dummy_queue_wrapper


def test_get_queue_process_safe(dummy_queue_wrapper):
    return_queue = dummy_queue_wrapper.get_queue(process_safe=True)

    assert isinstance(return_queue, type(mpQueue()))

    dummy_queue_wrapper.mp_queue.put(None)


def test_get_queue_not_process_safe(dummy_queue_wrapper):
    return_queue = dummy_queue_wrapper.get_queue(process_safe=False)

    assert isinstance(return_queue, type(thQueue()))

    dummy_queue_wrapper.th_queue.put(None)



