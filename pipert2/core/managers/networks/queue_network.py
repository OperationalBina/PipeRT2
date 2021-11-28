from typing import Tuple
from pipert2.core.base.routine import Routine
from pipert2.core.managers.network import Network
from pipert2.core.base.data_transmitter import DataTransmitter
from pipert2.core.handlers.message_handlers.queue_handler import QueueHandler
from pipert2.utils.publish_queue import PublishQueue


class QueueNetwork(Network):
    """The queue network generates queue handlers to manage communication using multiprocessing queues within the pipe.

    """

    def __init__(self, max_queue_sizes=1, put_block=False, get_block=True, timeout=1):
        super().__init__()
        self.max_queue_sizes = max_queue_sizes
        self.put_block = put_block
        self.get_block = get_block
        self.timeout = timeout

    def get_message_handler(self, routine_name: str) -> QueueHandler:
        """Generate/Retrieve a queue handler.

        Args:
            routine_name: The name of the routine to retrieve the queue handler for.

        Returns:
            A QueueHandler object relevant to the routine.

        """

        if routine_name in self.message_handlers:
            message_handler = self.message_handlers[routine_name]
        else:
            message_handler = QueueHandler(routine_name,
                                           max_queue_len=self.max_queue_sizes,
                                           put_block=self.put_block,
                                           get_block=self.get_block,
                                           timeout=self.timeout)

            self.message_handlers[routine_name] = message_handler

        return message_handler

    def link(self, source: Routine, destinations: Tuple[Routine], data_transmitter: DataTransmitter):
        """Links between two QueueHandlers of the given routines.

        Args:
            source: The source routine that generates data.
            destinations: Destination routines that receive the data.
            data_transmitter: The data transmitter that indicates how to transfer the data.

        """

        publish_queue = PublishQueue()

        for destination_routine in destinations:
            if source.flow_name == destination_routine.flow_name:
                publish_queue.register(destination_routine.message_handler.input_queue.get_queue(process_safe=False))
            else:
                publish_queue.register(destination_routine.message_handler.input_queue.get_queue(process_safe=True))

            destination_routine.message_handler.receive = data_transmitter.receive()

        source.message_handler.output_queue = publish_queue
        source.message_handler.transmit = data_transmitter.transmit()
