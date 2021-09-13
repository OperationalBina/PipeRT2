from queue import Full, Empty
from src.pipert2.core.handlers.message_handler import MessageHandler
from src.pipert2.utils.exceptions.queue_not_initialized import QueueNotInitialized


class QueueHandler(MessageHandler):
    """The queue message handler implements the functionality needed to get and put messages using multiprocessing
    queues.

    Args:
        blocking: If the queues will behave as blocking behavior detailed in each function or not.
        timeout: How long the queues will wait in seconds if blocking is true.

    """

    def __init__(self, routine_name: str, blocking=False, timeout=1):
        super().__init__(routine_name)
        self.input_queue = None
        self.output_queue = None
        self.blocking = blocking
        self.timeout = timeout

    def _get(self) -> bytes:
        """Get a message from the input queue.
        If blocking is true, wait the set timeout for a message to arrive,
        otherwise do nothing if the queue is empty.

        Returns:
            Return the message that came from the queue or None if the queue was empty.

        """

        message = None

        if self.input_queue is not None:  # TODO: If a queue doesn't exist, an exception is supposed to occur at pipe
                                                # base
            message = self.input_queue.get()

        return message

    def _put(self, message: bytes):
        """Put a message into the output queue.
        If blocking is true, try to push the message into the queue if it not full,
        otherwise push the message forcibly into the queue.

        Args:
            message: The given message to push.

        """

        if self.output_queue is None:
            raise QueueNotInitialized(f"{self.routine_name}'s output_queue was not initialized when put was called!")

        try:
            self.output_queue.put(message, block=self.blocking, timeout=self.timeout)
        except Full:
            self.logger.exception("The queue is full!")
