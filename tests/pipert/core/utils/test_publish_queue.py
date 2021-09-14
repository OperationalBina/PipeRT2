from src.pipert2.utils.publish_queue import PublishQueue


def test_single_consumer():
    publish_queue = PublishQueue()

    single_queue = publish_queue.register(None)
    publish_queue.put("message")

    assert single_queue.get() == "message"


def test_multiple_consumer():
    publish_queue = PublishQueue()

    queue1 = publish_queue.register(None)
    queue2 = publish_queue.register(None)
    queue3 = publish_queue.register(None)
    publish_queue.put("message")

    assert queue1.get() == queue2.get() == queue3.get() == "message"
