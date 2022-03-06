import time
from queue import Full, Empty, Queue
from pipert2.core.base.message import Message


class PublishQueue(object):
    """A class that wraps multiprocessing queue to make it possible to publish a single object to multiple queues.

    """

    def __init__(self):
        self.transmit = None
        self._queues_by_name = {}
        self._mp_queues = []
        self._queues = []

    def register(self, name: str, queue: Queue):
        """Register a new queue to publish to.

        Args:
            name: The name of the queue.
            queue: The registered queue.

        """

        if isinstance(queue, Queue):
            self._queues.append(queue)
        else:
            self._mp_queues.append(queue)

        self._queues_by_name[name] = queue

    def unregister(self, name: str):
        """Unregister queue by it's name from the queue lists.

        Args:
            name: The name of the mapped queue.

        """

        queue = self._queues_by_name.get(name)

        if queue is not None:
            if isinstance(queue, Queue):
                self._queues.remove(queue)
            else:
                self._mp_queues.remove(queue)

    def put(self, message, block=False, timeout=1):
        """Publish a value to every registered queue.

        Args:
            message: The value to push to every registered queue.
            block: Whether or not to block each queue when putting a message.
            timeout: How long to wait for each queue if block is true.

        """

        for q in self._queues:
            _push_to_queue(q, message, block, timeout)

        if len(self._mp_queues) > 0:
            transmitted_value = self.transmit(message.payload.data)
            message.update_data(transmitted_value)
            multiprocessing_message = Message.encode(message)

            for q in self._mp_queues:
                _push_to_queue(q, multiprocessing_message, block, timeout)


def _push_to_queue(q, value, block, timeout):
    if not block:
        force_push_to_queue(q, value)
    else:
        try:
            q.put(value, block, timeout)
        except Full as e:
            raise e

    # Without this line fps drops tremendously
    time.sleep(0.000001)


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
        except Full:
            pass
