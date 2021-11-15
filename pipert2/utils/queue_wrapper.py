from threading import Thread
from multiprocessing import Queue as mpQueue
from queue import Queue as thQueue, Full, Empty


class QueueWrapper:
    """The `QueueWrapper` is a class that enables the usage of both multiprocessing queue and threading queue with the
    `PublishQueue` class.
    It listens to both of its queues with thread and push to a designated out_queue all of the messages received in both
    queues.

    Attributes:
        mp_queue: A multiprocessing queue. Will be initiated once necessary.
        out_queue: Either a multiprocessing or a multithreading queue according to which queues exist.
        multiprocess_thread: A thread listening to the multiprocessing queue if it exists.

    """

    def __init__(self, max_queue_size=1):
        self.mp_queue: mpQueue = None
        self.max_queue_size = max_queue_size
        self.out_queue = thQueue(maxsize=max_queue_size)
        self.multiprocess_thread = Thread(target=self.queue_worker)

    def get(self, block: bool, timeout: int):
        """Return whatever is in the out_queue.

        Args:
            block: Whether to wait for the queue to have something in it or not.
            timeout: How long to wait if block is true.

        Returns:
            A message passed through the queue.

        """

        if self.mp_queue is not None:
            if not self.multiprocess_thread.is_alive():
                self.restart_queue_worker()

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
            in_queue = self.out_queue

        return in_queue

    def _get_mp_queue(self):
        """Start listening to the multiprocessing queue and change the out_queue to work with multiprocessing.

        Returns:
            A multiprocessing queue.

        """

        if self.mp_queue is None:
            self.mp_queue = mpQueue(maxsize=self.max_queue_size)

        return self.mp_queue

    def queue_worker(self):
        """A worker that pushes messages forward to the out_queue.
        If the input queue (`self.mp_queue`) receives None, exit the loop.

        """

        for item in iter(self.mp_queue.get, None):
            try:
                self.out_queue.put(item, block=True, timeout=1)
            except Full:
                pass

    def restart_queue_worker(self):
        """Restarts the queue worker.

        """

        self.multiprocess_thread = Thread(target=self.queue_worker)
        self.multiprocess_thread.start()

    def kill_queue_worker(self):
        """Kills the queue worker.

        """

        if self.mp_queue is not None:
            while self.multiprocess_thread.is_alive():
                self.mp_queue.put(None)
                self.multiprocess_thread.join(timeout=0.1)
