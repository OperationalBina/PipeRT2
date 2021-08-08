import time
from src.pipert2.core.base.pipe import Pipe
from src.pipert2.core.base.wire import Wire
from src.pipert2.contrib.routines.open_cv_capture_frame import OpenCVCaptureFrame
from src.pipert2.contrib.routines.face_detection import FaceDetection
from src.pipert2.contrib.routines.open_cv_display_frame import OpenCVDisplayFrame

pipe = Pipe()

r1 = OpenCVCaptureFrame(stream_address="")
r2 = FaceDetection()
r3 = OpenCVDisplayFrame()

pipe.create_flow("FaceDetectionFlow", True, r1, r2, r3)

# pipe.link(Wire(source=r1, destinations=(r2, r3)),
#           Wire(source=r2, destinations=(r3, )))

pipe.build()

pipe.notify_event("start")

time.sleep(20)

pipe.notify_event("kill")

pipe.join()