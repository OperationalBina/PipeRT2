import cv2
from src.pipert2.core.base.routine import Routine


class FaceDetection(Routine):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.face_cascade = None

    def main_logic(self, data):
        frame = data["frame"]
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.1, 4)

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

        return data

    def setup(self):
        self.face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    def cleanup(self):
        pass
