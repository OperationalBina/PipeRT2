import base64
import numpy as np


def create_log_record_of_extra_frame(name: str, numpy_frame: np.array):

    base64_frame = numpy_frame_to_base64(numpy_frame)

    extra_image = {
        'name': name,
        'image_base64': base64_frame
    }

    return f"extra_image: {extra_image}"


def numpy_frame_to_base64(numpy_frame: np.array):
    jpg_as_base64 = base64.b64encode(numpy_frame)
    base64_encode = f"{jpg_as_base64}"[2:]
    base64_encode = base64_encode[:len(base64_encode) - 1]

    return base64_encode
