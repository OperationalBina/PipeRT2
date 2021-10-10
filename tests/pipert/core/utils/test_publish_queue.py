import pytest
from queue import Full, Queue
from pipert2.utils.publish_queue import PublishQueue


@pytest.fixture()
def dummy_publish_queue():
    dummy_publish_queue = PublishQueue()

    return dummy_publish_queue


def test_single_consumer(dummy_publish_queue):
    single_queue = Queue(maxsize=1)
    dummy_publish_queue.register(single_queue)
    dummy_publish_queue.put("message")

    assert single_queue.get() == "message"

    dummy_publish_queue._queues = []


def test_multiple_consumer(dummy_publish_queue):
    queue1 = Queue(maxsize=1)
    queue2 = Queue(maxsize=1)
    queue3 = Queue(maxsize=1)
    dummy_publish_queue.register(queue1)
    dummy_publish_queue.register(queue2)
    dummy_publish_queue.register(queue3)
    dummy_publish_queue.put("message")

    assert queue1.get() == queue2.get() == queue3.get() == "message"

    dummy_publish_queue._queues = []


def test_force_push(dummy_publish_queue):
    queue = Queue(maxsize=1)
    dummy_publish_queue.register(queue)
    dummy_publish_queue.put("1")
    dummy_publish_queue.put("2")

    assert queue.get() == "2"

    dummy_publish_queue._queues = []


def test_blocking_put(dummy_publish_queue):
    queue = Queue(maxsize=1)
    dummy_publish_queue.register(queue)
    dummy_publish_queue.put("1", block=True)

    with pytest.raises(Full):
        dummy_publish_queue.put("2", block=True)

    assert queue.get() == "1"

    dummy_publish_queue._queues = []
