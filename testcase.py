import time

from pipert2.core.base.synchronise_routines.thread_loop_runner import ThreadLoopRunner


def run():
    print("5")
    time.sleep(0.5)

t = ThreadLoopRunner(run)

t.start()

time.sleep(2)

t.stop()