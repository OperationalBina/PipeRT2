import os
from typing import Optional
from queue import Full, Empty
from multiprocessing import Manager, Queue


class PublishQueue(object):
    """A class that wraps multiprocessing queue to make it possible to publish a single object to multiple queues.

    """

    def __init__(self):
        self._queues = []
        self._creator_pid = os.getpid()
        self.manager = Manager()

    def register(self, queue: Optional[Queue]):
        """Register a new queue to publish to.

        Returns:
            A multiprocessing queue object.

        """

        if queue is not None:
            q = queue
        else:
            q = self.manager.Queue(maxsize=1)
        self._queues.append(q)

        return q

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
        try:
            queue.get(block=False)
        except Empty:
            pass
        try:
            queue.put(value, block=False)
        except Full as e:
            pass
