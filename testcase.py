import threading
import time


def func():
    t = thread.currentThread()
    while(True):
        print("a")
        time.sleep(1)


thread = threading.Thread(target=func)
thread.start()

time.sleep(3)

thread.join(timeout=0.5)