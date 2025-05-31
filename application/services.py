import cv2
from application.interfaces import IHairDetector
from domain.entities import HairPresence
from shared.logger import get_logger


# Bu modül için özel bir logger (kayıt tutucu) oluşturuluyor.
# __name__ kullanılarak logger'a modülün adı verilir, bu da log kayıtlarında kaynağın kolayca belirlenmesini sağlar.
logger = get_logger(__name__)


class HairDetectionService:
    """
    Kamera akışından görüntüleri alarak kıl algılama işlemini yürüten ve
    sonuçlara göre Arduino'ya sinyal gönderen servis sınıfı.
    Bu sınıf, uygulamanın ana iş mantığını koordine eder.
    """
    def __init__(self, detector: IHairDetector, stream, arduino_serial=None):
        """
        HairDetectionService sınıfının başlatıcı metodu.

        Args:
            detector (IHairDetector): Kıl algılama mantığını içeren dedektör nesnesi.
                                      Bu, IHairDetector arayüzünü implemente eden herhangi bir sınıf olabilir.
            stream: Kamera akışını sağlayan nesne (örn: CameraStreamReader).
                    Bu nesne, 'open', 'read', 'release' ve 'cap' (çözünürlük ayarı için)
                    gibi metotlara/özelliklere sahip olmalıdır.
            arduino_serial (serial.Serial, optional): Arduino ile seri iletişim için
                                                     kullanılacak PySerial nesnesi.
                                                     Eğer None ise, Arduino iletişimi yapılmaz.
                                                     Varsayılan olarak None'dır.
        """
        self.detector = detector
        self.stream = stream
        self.arduino_serial = arduino_serial

    def run(self):
        """
        Kıl algılama döngüsünü başlatır. Kamera akışından sürekli olarak frame alır,
        kıl algılama işlemi yapar, sonucu ekranda gösterir ve (eğer ayarlandıysa) Arduino'ya sinyal gönderir.
        Kullanıcı 'q' tuşuna basana kadar veya bir hata oluşana kadar çalışmaya devam eder.
        """
        self.stream.open()
        self._set_resolution(640, 480)  # Kamera çözünürlüğünü QVGA (640x480) olarak ayarla (performans için)

        while True:
            # Kamera akışından bir sonraki frame'i oku
            ret, frame = self.stream.read()
            if not ret:
                logger.error("Frame okunamadı veya kamera akışı sonlandı.")
                break # Frame okunamadıysa döngüden çık

            # Alınan frame üzerinde kıl algılama işlemini gerçekleştir
            result = self.detector.detect(frame)
            
            # Algılama sonucuna göre Arduino'ya sinyal gönder ve log kaydı tut
            if result.presence == HairPresence.NO_HAIR:
                logger.info("Hair detected")
                if self.arduino_serial and self.arduino_serial.is_open:
                    try:
                        self.arduino_serial.write(b'1') # Arduino'ya '1' byte'ını gönder (kıl var)
                        logger.info("Arduino'ya '1' sinyali gönderildi (Kıl algılandı).")
                    except Exception as e:
                        logger.error(f"Arduino'ya yazma hatası: {e}")
            elif result.presence == HairPresence.HAIR:
                logger.info("No hair detected")
                if self.arduino_serial and self.arduino_serial.is_open:
                    try:
                        self.arduino_serial.write(b'0') # Arduino'ya '0' byte'ını gönder (kıl yok)
                        logger.info("Arduino'ya '0' sinyali gönderildi (Kıl algılanmadı).")
                    except Exception as e:
                        logger.error(f"Arduino'ya yazma hatası: {e}")
            else:
                # Beklenmedik bir algılama durumuyla karşılaşılırsa uyar
                logger.warning(f"Bilinmeyen algılama durumu: {result.presence}")

            # Algılama sonucunu (kıl varlığı/yokluğu) ve güven skorunu frame üzerine yazdır
            label = f"{result.presence.value} ({result.confidence:.2f})"
            cv2.putText(frame, label, (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.imshow("Hair Detection", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        # Döngü bittikten sonra kullanılan kaynakları serbest bırak
        self.stream.release()
        cv2.destroyAllWindows()

    def _set_resolution(self, width, height):
        """
        Kamera akışının çözünürlüğünü ayarlar (eğer destekleniyorsa).
        Bu metod, stream nesnesinin OpenCV'nin VideoCapture nesnesini
        (genellikle 'cap' olarak adlandırılır ve stream_reader içinde bulunur)
        içerdiğini ve bu nesne üzerinden çözünürlük ayarının yapılabileceğini varsayar.

        Args:
            width (int): İstenen genişlik piksel cinsinden.
            height (int): İstenen yükseklik piksel cinsinden.
        """
        # Stream nesnesinin 'cap' adında bir özelliği olup olmadığını ve dolu olup olmadığını kontrol et
        if hasattr(self.stream, "cap") and self.stream.cap:
            # OpenCV VideoCapture nesnesinin set metodu ile genişlik ve yükseklik ayarlarını yap
            self.stream.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
            self.stream.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
            logger.info(f"Kamera çözünürlüğü {width}x{height} olarak ayarlanmaya çalışıldı.")
        else:
            logger.warning("Kamera çözünürlüğü ayarlanamadı: 'cap' özelliği bulunamadı veya stream kapalı.")
