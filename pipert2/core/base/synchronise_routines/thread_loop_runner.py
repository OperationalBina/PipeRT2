import threading

from pipert2.utils.dummy_object import Dummy


class ThreadLoopRunner:
    def __init__(self, target):
        self.target = target
        self.stop_event = threading.Event()
        self.current_thread = Dummy()

    def start(self):
        self.stop_event.clear()
        self.current_thread = threading.Thread(target=self._start_loop)
        self.current_thread.start()

    def stop(self):
        self.stop_event.set()

    def _start_loop(self):
        while not self.stop_event.is_set():
            self.target()