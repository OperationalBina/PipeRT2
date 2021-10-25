import logging
import time

from demos.end_demo import EndDemo
from demos.r1_demo import R1
from demos.r2_demo import R2
from demos.start_demo import StartDemo
from src.pipert2 import Pipe
from src.pipert2 import QueueNetwork

network = QueueNetwork()

pipe = Pipe(network=network, logger=logging.getLogger())

start = StartDemo()
end = EndDemo()
r1 = R1()
r2 = R2()

pipe.create_flow("test", True, start, r1, r2)

pipe.build()

pipe.notify_event("start")

time.sleep(5)

pipe.notify_event("kill")
pipe.join()