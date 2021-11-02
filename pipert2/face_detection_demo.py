import time

from contrib.routines.gray_scale_routine import GrayScaleRoutine
from contrib.routines.opencv_capture_frame import OpenCVCaptureFrame
from contrib.routines.opencv_display_frame import OpenCVDisplayFrame
from core.base.pipe import Pipe
from core.managers.networks.queue_network import QueueNetwork
from utils.logging_module_modifiers import create_file_logger

network = QueueNetwork()
logger = create_file_logger(name="demo")
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
