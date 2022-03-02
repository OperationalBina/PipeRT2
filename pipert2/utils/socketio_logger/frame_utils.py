try:
    import cv2
except ImportError:
    print(
        "Seems like opencv isn't installed...\nIn order to use the cockpit and its features run pip install PipeRT["
        "cockpit]")
    cv2 = None

import base64
import numpy as np


def create_log_record_of_extra_frame(name: str, numpy_frame: np.array):
    base64_frame = numpy_frame_to_base64(numpy_frame)

    extra_image = {
        'name': name,
        'image_base64': base64_frame
    }

    return f"extra_image: {extra_image}"


if cv2:
    def numpy_frame_to_base64(numpy_frame: np.array):
        ret, encoded_frame = cv2.imencode('.jpg', numpy_frame, [cv2.IMWRITE_JPEG_QUALITY, 60])

        if ret:
            jpg_as_base64 = base64.b64encode(encoded_frame)
            base64_encode = f"{jpg_as_base64}"[2:]
            base64_encode = base64_encode[:len(base64_encode) - 1]

            return base64_encode
