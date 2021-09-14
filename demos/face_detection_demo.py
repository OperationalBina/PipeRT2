import time

from src.pipert2.contrib.loggers.print_logger import PrintLogger
from src.pipert2.contrib.routines.gray_scale_routine import GrayScaleRoutine
from src.pipert2.contrib.routines.open_cv_capture_frame import OpenCVCaptureFrame
from src.pipert2.contrib.routines.open_cv_display_frame import OpenCVDisplayFrame
from src.pipert2.core.base.pipe import Pipe
from src.pipert2.core.managers.networks.queue_network import QueueNetwork

network = QueueNetwork()
logger = PrintLogger(name="demo")
pipe = Pipe(network=network, logger=logger)

r1 = OpenCVCaptureFrame(name='FirstRoutine', stream_address="https://www.youtube.com/watch?v=D41rWcKGzQk")
r2 = GrayScaleRoutine()
r3 = OpenCVDisplayFrame(name='LastRoutine')

pipe.create_flow("FaceDetectionFlow", True, r1, r2, r3)

pipe.build()

pipe.notify_event("start")

time.sleep(150)

pipe.notify_event("kill")

pipe.join()
