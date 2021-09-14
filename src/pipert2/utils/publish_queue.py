import os
from queue import Full
from functools import wraps
from multiprocessing import Manager, Queue
from typing import Optional


def ensure_parent(func):
    @wraps(func)
    def inner(self, *args, **kwargs):
        if os.getpid() != self._creator_pid:
            raise RuntimeError("{} can only be called in the "
                               "parent.".format(func.__name__))
        return func(self, *args, **kwargs)

    return inner


class PublishQueue(object):
    """A class that wraps multiprocessing queue to make it possible to publish a single object to multiple queues.

    """

    def __init__(self):
        self._queues = []
        self._creator_pid = os.getpid()

    @ensure_parent
    def register(self, queue: Optional[Queue]):
        """Register a new queue to publish to.

        Returns:
            A multiprocessing queue object.

        """

        if queue is not None:
            q = queue
        else:
            q = Manager().Queue(maxsize=1)
        self._queues.append(q)

        return q

    @ensure_parent
    def put(self, value, block=False, timeout=1):
        """Publish a value to every registered queue.

        Args:
            value: The value to push to every registered queue.
            block: Whether or not to block each queue when putting a message.
            timeout: How long to wait for each queue if block is true.

        """

        for q in self._queues:
            if not block:
                force_push_to_queue(q, value)
            else:
                try:
                    q.put(value, block, timeout)
                except Full as e:
                    raise e


def force_push_to_queue(queue: Queue, value):
    """Forcibly push a message into the queue.

    Args:
        queue: The queue to push the value into.
        value: The given message to push.

    """

    try:
        queue.put(value, block=False)
    except Full:
        queue.get(block=False)
        try:
            queue.put(value, block=False)
        except Full as e:
            raise e
