from threading import Thread
from multiprocessing import Queue as mpQueue
from queue import Queue as thQueue, Full, Empty
from src.pipert2.utils.publish_queue import force_push_to_queue


class QueueWrapper:
    th_queue = None
    mp_queue = None
    out_queue = None
    threads = {'threading': None, 'multiprocessing': None}

    def get_queue(self, process_safe: bool):
        if process_safe:
            in_queue = self._get_mp_queue()
        else:
            in_queue = self._get_th_queue()

        return in_queue

    def get(self, block: bool, timeout: int):
        try:
            message = self.out_queue.get(block=block, timeout=timeout)
        except Empty:
            raise Empty

        return message

    def _get_mp_queue(self):
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
        if self.th_queue is None:
            self.th_queue = thQueue(maxsize=1)

            if self.out_queue is None:
                self.out_queue = thQueue(maxsize=1)

            self.threads['threading'] = Thread(target=queue_worker, args=(self.th_queue, self.out_queue))
            self.threads['threading'].start()

        return self.th_queue


def queue_worker(in_queue, out_queue):
    for item in iter(in_queue.get, None):
        try:
            out_queue.put(item)
        except Full:
            pass
