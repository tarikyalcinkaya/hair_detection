import cv2
import numpy as np
import requests


class CameraStreamReader:
    def __init__(self, source: str | int):
        self.source = source
        self.cap = None
        self.session = None

    def open(self):
        if isinstance(self.source, int):
            self.cap = cv2.VideoCapture(self.source)
        else:
            self.session = requests.Session()  # HTTP oturumu başlat

    def read(self):
        if isinstance(self.source, int):
            return self.cap.read()

        try:
            response = self.session.get(self.source, timeout=50)
            if response.status_code == 200:
                img_array = np.frombuffer(response.content, np.uint8)
                frame = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
                return True, frame
            else:
                return False, None
        except Exception as e:
            print(f"ESP32 connection error: {e}")
            return False, None

    def release(self):
        if self.cap:
            self.cap.release()
        if self.session:
            self.session.close()
