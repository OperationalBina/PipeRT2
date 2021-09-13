import os
from queue import Full
from functools import wraps
from multiprocessing import Queue


def ensure_parent(func):
    @wraps(func)
    def inner(self, *args, **kwargs):
        if os.getpid() != self._creator_pid:
            raise RuntimeError("{} can only be called in the "
                               "parent.".format(func.__name__))
        return func(self, *args, **kwargs)

    return inner


class PublishQueue(object):
    def __init__(self):
        self._queues = []
        self._creator_pid = os.getpid()

    def __getstate__(self):
        self_dict = self.__dict__
        self_dict['_queues'] = []

        return self_dict

    def __setstate__(self, state):
        self.__dict__.update(state)

    @ensure_parent
    def register(self):
        q = Queue(maxsize=1)
        self._queues.append(q)

        return q

    @ensure_parent
    def put(self, value, block=False, timeout=1):
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
