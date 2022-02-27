import time
import threading
from collections import deque
from typing import Callable, Deque


class BatchNotifier:
    def __init__(self, interval: float, callable: Callable, data_maxlen: int):
        self.interval = interval
        self.callable = callable

        self.stop_notify = threading.Event()
        self.data: Deque = deque(maxlen=data_maxlen)

    def start(self):
        """Start batch notifier process.

        """

        self.stop_notify.clear()
        threading.Thread(target=self._run).start()

    def stop(self):
        """Stop batch notifier process.

        """

        self.stop_notify.set()

    def add_record(self, record):
        """Add record to data.

        Args:
            record: One record to add the data.

        """

        self.data.append(record)

    def _run(self):
        """Notify each time interval the data.

        """

        while not self.stop_notify.is_set():
            self.callable(data=self.data)
            time.sleep(self.interval)
