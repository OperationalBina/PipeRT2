from queue import Full, Empty
from pipert2.core.base.data import FrameData
from pipert2.core.base.message import Message
from pipert2.utils.queue_utils.publish_queue import PublishQueue
from pipert2.utils.queue_utils.queue_wrapper import QueueWrapper
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
        self.output_queue: PublishQueue = PublishQueue()
        self.put_block = put_block
        self.get_block = get_block
        self.timeout = timeout

    def _get(self) -> Message:
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

    def _put(self, message: Message):
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

    def get(self) -> Message:
        message = self._get()

        if message is not None:
            if isinstance(message, Message):
                if self.send_data and isinstance(message.payload.data, FrameData):
                    self.logger.log_frame("input", message)

                message.record_entry(self.routine_name)

        return message

    def put(self, message: Message):
        """Encodes a given message and calls the implemented put method.

        Args:
            message: The message to be sent.

        """

        if self.send_data and isinstance(message.payload.data, FrameData):
            self.logger.log_frame("output", message)

        self._put(message)

    def link(self, name, queue):
        """Link between the current output queue to destination queue.

        Args:
            name: The name of the destination.
            queue: The destination queue.

        """
        self.output_queue.register(name, queue)

    def unlink(self, name):
        """Unlink between the current output queue from destination queue.

        Args:
            name: The name of the destination.
        """
        self.output_queue.unregister(name)

    def get_receiver(self, process_safe):
        """Get the receiver queue.

        Args:
            process_safe: If the receiver should be process safe or not.

        Returns:
            Return process safe queue if process_safe is True, if it false then return not process safe.
        """
        return self.input_queue.get_queue(process_safe)

    def set_receive(self, receive):
        """Set the receive function of the message handler on the input queue.

        Args:
            receive: The receive function.

        """
        self.input_queue.receive = receive

    def set_transmit(self, transmit):
        """Set the transmit function of the message handler on the output queue.

        Args:
            transmit: The transmit function.

        """
        self.output_queue.transmit = transmit
