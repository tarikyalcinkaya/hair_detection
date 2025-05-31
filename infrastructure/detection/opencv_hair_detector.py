import cv2
import numpy as np
from domain.entities import DetectionResult, HairPresence
from application.interfaces import IHairDetector


class OpenCVHairDetector(IHairDetector):
    def detect(self, frame: np.ndarray) -> DetectionResult:
        # 1. Grayscale + Gaussian Blur
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (3, 3), 0)

        # 2. Canny edge detection (düşük eşiklerle)
        edges = cv2.Canny(blur, threshold1=30, threshold2=80)

        # 3. Morfolojik genişletme (ince çizgileri vurgulamak için)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
        dilated = cv2.dilate(edges, kernel, iterations=1)

        # 4. Görüntünün sadece merkezi (ROI)
        h, w = dilated.shape
        roi = dilated[h // 4:h * 3 // 4, w // 4:w * 3 // 4]

        # 5. Edge yoğunluğu
        edge_density = np.sum(roi > 0) / roi.size

        # DEBUG GÖRÜNTÜLER
        cv2.imshow("Edges", edges)
        cv2.imshow("Dilated", dilated)
        cv2.imshow("ROI", roi)

        # 6. Eşik kontrolü
        if edge_density > 0.01:
            return DetectionResult(HairPresence.HAIR, edge_density)
        else:
            return DetectionResult(HairPresence.NO_HAIR, edge_density)
