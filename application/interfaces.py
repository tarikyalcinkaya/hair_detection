from abc import ABC, abstractmethod
from domain.entities import DetectionResult
import numpy as np

# Bu dosya, uygulama katmanındaki servislerin ve diğer bileşenlerin
# uyması gereken soyut arayüzleri (abstract interfaces) tanımlar.
# Arayüzler, sistemin farklı parçaları arasında gevşek bağlılık (loose coupling)
# ve daha iyi test edilebilirlik sağlar.


class IHairDetector(ABC):
    """
    Kıl algılama işlemini gerçekleştirecek olan dedektörler için soyut temel sınıf (arayüz).
    Bu arayüzü implemente eden her sınıf, bir 'detect' metodu sağlamalıdır.
    ABC (Abstract Base Class) kullanmak, bu arayüzün doğrudan örneğinin oluşturulmasını engeller
    ve alt sınıfların belirli metotları implemente etmesini zorunlu kılar.
    """
    @abstractmethod
    def detect(self, frame: np.ndarray) -> DetectionResult:
        """
        Verilen bir görüntü çerçevesi (frame) üzerinde kıl algılama işlemini gerçekleştirir.

        Args:
            frame (np.ndarray): İşlenecek olan görüntü çerçevesi (NumPy dizisi formatında).

        Returns:
            DetectionResult: Algılama sonucunu (kıl varlığı ve güven skoru) içeren bir nesne.
        """
        pass
