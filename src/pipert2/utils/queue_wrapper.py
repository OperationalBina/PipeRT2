from threading import Thread
from multiprocessing import Queue as mpQueue
from queue import Queue as thQueue, Full, Empty
from src.pipert2.utils.publish_queue import force_push_to_queue


class QueueWrapper:
    """The `QueueWrapper` is a class that enables the usage of both multiprocessing queue and threading queue with the
    `PublishQueue` class.
    It listens to both of its queues with thread and push to a designated out_queue all of the messages received in both
    queues.

    Attributes:
        th_queue: A multithreading queue. Will be initiated once necessary.
        mp_queue: A multiprocessing queue. Will be initiated once necessary.
        out_queue: Either a multiprocessing or a multithreading queue according to which queues exist.
        threads: A dictionary of the threads listening to the queues.

    """

    th_queue = None
    mp_queue = None
    out_queue = None
    threads = {'threading': None, 'multiprocessing': None}

    def get(self, block: bool, timeout: int):
        """Return whatever is in the out_queue.

        Args:
            block: Whether to wait for the queue to have something in it or not.
            timeout: How long to wait if block is true.

        Returns:
            A message passed through the queue.

        """

        try:
            message = self.out_queue.get(block=block, timeout=timeout)
        except Empty:
            raise Empty

        return message

    def get_queue(self, process_safe: bool):
        """Get a queue according to necessity.

        Args:
            process_safe: Indicate if the queue needs to be process safe or not.

        Returns:
            If process_safe is true, return a multiprocessing queue, otherwise return a multithreading queue.

        """

        if process_safe:
            in_queue = self._get_mp_queue()
        else:
            in_queue = self._get_th_queue()

        return in_queue

    def _get_mp_queue(self):
        """Start listening to the multiprocessing queue and change the out_queue to work with multiprocessing.

        Returns:
            A multiprocessing queue.

        """

        if self.mp_queue is None:
            self.mp_queue = mpQueue(maxsize=1)
            self.out_queue = mpQueue(maxsize=1)

            if self.threads['threading'] is not None:
                force_push_to_queue(self.th_queue, None)
                self.threads['threading'] = Thread(target=queue_worker, args=(self.th_queue, self.out_queue))
                self.threads['threading'].start()

            self.threads['multiprocessing'] = Thread(target=queue_worker, args=(self.mp_queue, self.out_queue))
            self.threads['multiprocessing'].start()

        return self.mp_queue

    def _get_th_queue(self):
        """Start listening to the multithreading queue and create the out_queue to work with multithreading if it
        doesn't exist.

        Returns:
            A multithreading queue.

        """

        if self.th_queue is None:
            self.th_queue = thQueue(maxsize=1)

            if self.out_queue is None:
                self.out_queue = thQueue(maxsize=1)

            self.threads['threading'] = Thread(target=queue_worker, args=(self.th_queue, self.out_queue))
            self.threads['threading'].start()

        return self.th_queue


def queue_worker(in_queue, out_queue):
    """A worker that pushes messages forward to the out_queue.

    Args:
        in_queue: The queue to listen to until None is received.
        out_queue: The queue to forward the messages into.

    """

    for item in iter(in_queue.get, None):
        try:
            out_queue.put(item)
        except Full:
            pass
