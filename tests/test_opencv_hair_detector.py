import cv2
import numpy as np
import pytest
from infrastructure.detection.opencv_hair_detector import OpenCVHairDetector
from domain.entities import HairPresence


@pytest.fixture
def hair_detector():
    return OpenCVHairDetector()


def test_no_hair_image(hair_detector):
    # Beyaz boş bir resim (kıl yok)
    blank_image = np.ones((480, 640, 3), dtype=np.uint8) * 255
    result = hair_detector.detect(blank_image)
    assert result.presence == HairPresence.NO_HAIR
    assert 0 <= result.confidence <= 1


def test_fake_hair_image(hair_detector):
    # Siyah çizgiler içeren yapay kıl görüntüsü
    image = np.ones((480, 640), dtype=np.uint8) * 255
    for y in range(50, 400, 10):
        cv2.line(image, (100, y), (540, y), 0, 1)
    image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    result = hair_detector.detect(image)
    assert result.presence == HairPresence.HAIR
    assert 0 <= result.confidence <= 1
