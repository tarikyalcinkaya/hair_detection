from application.services import HairDetectionService
from infrastructure.detection.opencv_hair_detector import OpenCVHairDetector
from infrastructure.camera_stream_reader import CameraStreamReader
import serial
import time

# Bu dosya, kıl algılama uygulamasının ana giriş noktasıdır.
# Gerekli bileşenleri (dedektör, kamera akışı, seri iletişim) başlatır
# ve ana servis olan HairDetectionService'i çalıştırır.


def main():
    """
    Uygulamanın ana işlevlerini yürüten ana fonksiyon.
    Bu fonksiyon, kıl dedektörünü, kamera akışını ve Arduino ile seri bağlantıyı
    ayarlar, ardından kıl algılama servisini başlatır.
    """
    # Kıl algılama için kullanılacak dedektör nesnesi oluşturuluyor.
    # OpenCVHairDetector, OpenCV kütüphanesini kullanarak kıl algılama işlemini gerçekleştirir.
    detector = OpenCVHairDetector()

    # Kamera akışını okumak için kullanılacak nesne oluşturuluyor.
    # Kullanılacak kamera kaynağına göre aşağıdaki satırlardan biri seçilmelidir:
    # - Dahili/USB Webcam için: CameraStreamReader(0) veya CameraStreamReader(1)
    #   (0 genellikle dahili kameradır, harici kameralar için 1, 2... deneyin)
    # - ESP32-CAM veya IP Kamera için: CameraStreamReader("http://ESP32_IP_ADRESI/capture")
    #   (ESP32-CAM'in IP adresini ve yakalama (capture) endpoint'ini girin)
    stream = CameraStreamReader("http://192.168.4.1/capture")

    arduino_serial_port = None
    try:
        # Arduino ile seri iletişim kurmak için bağlantı ayarları.
        # Arduino'nuzun bilgisayarınıza bağlı olduğu doğru seri portu ve
        # Arduino kodunuzda belirlediğiniz baud rate'i (genellikle 9600) girin.
        #
        # Windows için: "COM3", "COM4" vb.
        # Linux için: "/dev/ttyUSB0", "/dev/ttyACM0" vb.
        # macOS için: "/dev/cu.usbserial-XXXX" veya "/dev/cu.usbmodemXXXX"
        # ÖNEMLİ: Aşağıdaki 'arduino_port_name' değişkenini kendi sisteminize göre güncelleyin!
        arduino_port_name = "/dev/cu.usbmodem1301"  # <<<--- ARDUINO PORTUNUZU BURAYA GİRİN
        baud_rate = 9600
        # Belirtilen port ve baud rate ile seri bağlantıyı açmaya çalış
        arduino_serial_port = serial.Serial(arduino_port_name, baud_rate, timeout=1)
        print(f"Arduino'ya {arduino_port_name} portundan {baud_rate} baud rate ile bağlanıldı.")
        # Arduino'nun seri iletişime başlaması ve kendini hazırlaması için kısa bir bekleme süresi.
        # Bu, Arduino'nun resetlenmesinden sonra veri kaybını önleyebilir.
        time.sleep(2)
    except serial.SerialException as e:
        # Seri bağlantı kurulamadıysa hata mesajı yazdır ve seri iletişim olmadan devam et.
        print(f"Arduino'ya bağlanılamadı: {e}")
        print("Seri iletişim olmadan devam edilecek. Arduino'nun bağlı olduğundan ve doğru portu girdiğinizden emin olun.")

    # Kıl algılama servisini, oluşturulan dedektör, kamera akışı ve
    # (başarılıysa) Arduino seri port nesnesi ile başlat.
    service = HairDetectionService(detector, stream, arduino_serial=arduino_serial_port)
    try:
        # Ana algılama döngüsünü başlat.
        service.run()
    finally:
        # Program sonlandığında (normal veya hata ile), açık olan seri portu kapat.
        # Bu, portun başka uygulamalar tarafından kullanılabilir kalmasını sağlar.
        if arduino_serial_port and arduino_serial_port.is_open:
            print("Seri port kapatılıyor.")
            arduino_serial_port.close()

# Bu betik doğrudan çalıştırıldığında (import edilmek yerine), main() fonksiyonunu çağır.
if __name__ == "__main__":
    main()
