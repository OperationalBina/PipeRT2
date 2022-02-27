import pytest
from queue import Full, Queue
from pipert2.utils.queue_utils.publish_queue import PublishQueue
from multiprocessing import Queue as mpQueue


@pytest.fixture()
def dummy_publish_queue():
    dummy_publish_queue = PublishQueue()

    return dummy_publish_queue


def test_single_consumer(dummy_publish_queue):
    single_queue = Queue(maxsize=1)
    dummy_publish_queue.register("name", single_queue)
    dummy_publish_queue.put("message")

    assert single_queue.get() == "message"

    dummy_publish_queue._queues = []


def test_multiple_consumer(dummy_publish_queue):
    queue1 = Queue(maxsize=1)
    queue2 = Queue(maxsize=1)
    queue3 = Queue(maxsize=1)
    dummy_publish_queue.register("name1", queue1)
    dummy_publish_queue.register("name2", queue2)
    dummy_publish_queue.register("name3", queue3)
    dummy_publish_queue.put("message")

    assert queue1.get() == queue2.get() == queue3.get() == "message"

    dummy_publish_queue._queues = []


def test_force_push(dummy_publish_queue):
    queue = Queue(maxsize=1)
    dummy_publish_queue.register("name1", queue)
    dummy_publish_queue.put("1")
    dummy_publish_queue.put("2")

    assert queue.get() == "2"

    dummy_publish_queue._queues = []


def test_blocking_put(dummy_publish_queue):
    queue = Queue(maxsize=1)
    dummy_publish_queue.register("name1", queue)
    dummy_publish_queue.put("1", block=True)

    with pytest.raises(Full):
        dummy_publish_queue.put("2", block=True)

    assert queue.get() == "1"

    dummy_publish_queue._queues = []


def test_unlink_thread_queue(dummy_publish_queue):
    queue = Queue(maxsize=1)
    dummy_publish_queue._queues.append(queue)
    dummy_publish_queue._queues_by_name["name1"] = queue
    dummy_publish_queue.unregister("name1")

    assert len(dummy_publish_queue._queues) == 0


def test_unlink_multiprocessing_queue(dummy_publish_queue):
    queue = mpQueue(maxsize=1)
    dummy_publish_queue._mp_queues.append(queue)
    dummy_publish_queue._queues_by_name["name1"] = queue
    dummy_publish_queue.unregister("name1")

    assert len(dummy_publish_queue._mp_queues) == 0


def test_unlink_not_existing_queue(dummy_publish_queue):
    queue = mpQueue(maxsize=1)
    dummy_publish_queue._mp_queues.append(queue)
    dummy_publish_queue._queues_by_name["name1"] = queue
    dummy_publish_queue.unregister("name2")

    assert len(dummy_publish_queue._mp_queues) == 1