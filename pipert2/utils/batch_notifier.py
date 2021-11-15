import threading
import time
from collections import deque
from typing import Callable, Deque


class BatchNotifier:
    def __init__(self, interval: float, event_name: str, callable: Callable, source: str, data_maxlen: int):
        self.interval = interval
        self.event_name = event_name
        self.callable = callable
        self.source = source

        self.stop_notify = threading.Event()
        self.data: Deque = deque(maxlen=data_maxlen)

    def start(self):
        self.stop_notify.clear()
        threading.Thread(target=self._run).start()

    def _run(self):
        while not self.stop_notify.is_set():
            self.callable(event_name=self.event_name, source_name=self.source, data=self.data)
            time.sleep(self.interval)

    def stop(self):
        self.stop_notify.set()

    def add(self, var):
        print(f"add var {var}")
        self.data.append(var)
        print(self.data)