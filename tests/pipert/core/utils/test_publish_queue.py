from queue import Full

import pytest
from src.pipert2.utils.publish_queue import PublishQueue


@pytest.fixture()
def dummy_publish_queue():
    dummy_publish_queue = PublishQueue()

    return dummy_publish_queue


def test_single_consumer(dummy_publish_queue):
    single_queue = dummy_publish_queue.register(None)
    dummy_publish_queue.put("message")

    assert single_queue.get() == "message"


def test_multiple_consumer(dummy_publish_queue):
    queue1 = dummy_publish_queue.register(None)
    queue2 = dummy_publish_queue.register(None)
    queue3 = dummy_publish_queue.register(None)
    dummy_publish_queue.put("message")

    assert queue1.get() == queue2.get() == queue3.get() == "message"


def test_force_push(dummy_publish_queue):
    queue = dummy_publish_queue.register(None)
    dummy_publish_queue.put("1")
    dummy_publish_queue.put("2")

    assert queue.get() == "2"


def test_blocking_put(dummy_publish_queue):
    queue = dummy_publish_queue.register(None)
    dummy_publish_queue.put("1", block=True)

    with pytest.raises(Full):
        dummy_publish_queue.put("2", block=True)

    assert queue.get() == "1"
