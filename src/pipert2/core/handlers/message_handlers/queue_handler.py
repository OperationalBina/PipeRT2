from ..message_handler import MessageHandler
from multiprocessing import Queue
from queue import Full, Empty
from pipert2.core.base.message import Message


class QueueHandler(MessageHandler):
    """The queue message handler implements the functionality needed to get and put messages using multiprocessing
    queues.

    Args:
        input_queue: The that will be used in order to get messages.
        output_queue: The that will be used in order to push messages.
        blocking: If the queues will behave as blocking behavior detailed in each function or not.
        timeout: How long the queues will wait in seconds if blocking is true.

    """

    def __init__(self, input_queue: Queue, output_queue: Queue, blocking=True, timeout=1):
        super().__init__()
        self.input_queue = input_queue
        self.output_queue = output_queue
        self.blocking = blocking
        self.timeout = timeout

    def _get(self):
        """Get a message from the input queue.
        If blocking is true, wait the set timeout for a message to arrive,
        otherwise do nothing if the queue is empty.

        Returns:
            Return the message that came from the queue or None if the queue was empty.

        """

        message = None

        try:
            message = self.input_queue.get(block=self.blocking, timeout=self.timeout)
        except Empty:
            print("The queue is empty")  # TODO: Replace with log

        return message

    def _put(self, message: Message):
        """Put a message into the output queue.
        If blocking is true, try to push the message into the queue if it not full,
        otherwise push the message forcibly into the queue.

        Args:
            message: The given message to push.

        """

        self._safe_push_to_queue(message) if self.blocking else self._force_push_to_queue(message)

    def _force_push_to_queue(self, message: Message):
        """Forcibly push a message into the queue.

        Args:
            message: The given message to push.

        """

        try:
            self.output_queue.put(message, block=False)
        except Full:
            self.output_queue.get(block=False)
            try:
                self.output_queue.put(message, block=False)
            except Full:
                print("The queue is full!")  # TODO: Replace with log

    def _safe_push_to_queue(self, message: Message):
        """Try pushing a message into the queue.
        If the queue is full, do nothing.

        Args:
            message: The given message to push.

        """

        try:
            self.output_queue.put(message, block=True, timeout=self.timeout)
        except Full:
            print("The queue is full!")  # TODO: Replace with log