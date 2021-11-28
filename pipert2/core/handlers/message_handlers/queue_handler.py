from queue import Full, Empty
from pipert2.utils.queue_wrapper import QueueWrapper
from pipert2.core.handlers.message_handler import MessageHandler
from pipert2.utils.exceptions.queue_not_initialized import QueueNotInitialized


class QueueHandler(MessageHandler):
    """The queue message handler implements the functionality needed to get and put messages using multiprocessing
    queues.

    Args:
        block: If the queues will behave as blocking behavior detailed in each function or not.
        timeout: How long the queues will wait in seconds if blocking is true.

    """

    def __init__(self, routine_name: str, max_queue_len=1, put_block=False, get_block=True, timeout=1):
        super().__init__(routine_name)
        self.input_queue = QueueWrapper(max_queue_len)
        self.output_queue = None
        self.put_block = put_block
        self.get_block = get_block
        self.timeout = timeout

    def _get(self) -> bytes:
        """Get a message from the input queue.
        If blocking is true, wait the set timeout for a message to arrive,
        otherwise do nothing if the queue is empty.

        Returns:
            Return the message that came from the queue or None if the queue was empty.

        """

        message = None

        try:
            message = self.input_queue.get(block=self.get_block, timeout=self.timeout)
        except Empty:
            pass

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
            self.output_queue.put(message, block=self.put_block, timeout=self.timeout)
        except Full:
            self.logger.exception("The queue is full!")

    def teardown(self):
        self.input_queue.kill_queue_worker()
