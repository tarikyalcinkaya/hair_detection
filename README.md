# Kıl Algılama ve Arduino Entegrasyonu Projesi

Bu proje, bir kamera akışından (örneğin ESP32-CAM veya webcam) alınan görüntüler üzerinde kıl algılama işlemi yapar ve algılama sonucuna göre bir Arduino Uno'ya sinyal gönderir.

## Özellikler

*   OpenCV kullanarak gerçek zamanlı kıl algılama.
*   ESP32-CAM veya standart USB web kameraları ile uyumlu.
*   Kıl algılandığında veya algılanmadığında Arduino'ya seri port üzerinden sinyal gönderme.
*   Yapılandırılabilir kamera çözünürlüğü.
*   Detaylı loglama.

## Kurulum

1.  **Proje Klonlama:**
    ```bash
    git clone <proje_repository_url>
    cd hair_detection
    ```

2.  **Sanal Ortam Oluşturma ve Aktifleştirme (Önerilir):**
    ```bash
    python -m venv venv
    # Windows için:
    # venv\Scripts\activate
    # macOS/Linux için:
    # source venv/bin/activate
    ```

3.  **Bağımlılıkları Yükleme:**
    Proje için gerekli Python kütüphanelerini yükleyin:
    ```bash
    pip install -r requirements.txt
    ```
    `requirements.txt` dosyası aşağıdaki temel bağımlılıkları içerir:
    *   `opencv-python`: Görüntü işleme için.
    *   `numpy`: Sayısal işlemler için.
    *   `requests`: IP kamera akışından veri almak için.
    *   `pyserial`: Arduino ile seri iletişim için.
    *   `pytest`: (Testler için, eğer yazıldıysa)

## Arduino Kurulumu

1.  Arduino IDE'nizi açın.
2.  Aşağıdaki örnek Arduino kodunu Uno'nuza yükleyin. Bu kod, seri porttan '1' geldiğinde 13. pini (dahili LED) HIGH, '0' geldiğinde LOW yapar.
    ```c++
    // Arduino Kodu
    const int outputPin = 13; // Çıkış vermek istediğiniz pin
    char incomingByte;

    void setup() {
      Serial.begin(9600); // Python kodundaki baud rate ile aynı olmalı
      pinMode(outputPin, OUTPUT);
      digitalWrite(outputPin, LOW);
      Serial.println("Arduino hazır. Python'dan sinyal bekleniyor...");
    }

    void loop() {
      if (Serial.available() > 0) {
        incomingByte = Serial.read();
        Serial.print("Alınan byte: ");
        Serial.println(incomingByte);

        if (incomingByte == '1') {
          digitalWrite(outputPin, HIGH);
          Serial.println("Çıkış AÇIK (Kıl algılandı)");
        } else if (incomingByte == '0') {
          digitalWrite(outputPin, LOW);
          Serial.println("Çıkış KAPALI (Kıl algılanmadı)");
        }
      }
    }
    ```
3.  Arduino'nuzu bilgisayarınıza USB ile bağlayın.

## Yapılandırma

*   **Kamera Kaynağı:**
    *   `main.py` dosyasında, `stream = CameraStreamReader(...)` satırını kendi kamera kaynağınıza göre düzenleyin.
        *   Webcam için: `CameraStreamReader(0)` veya `CameraStreamReader(1)`
        *   ESP32-CAM için: `CameraStreamReader("http://ESP32_IP_ADRESI/capture")`
*   **Arduino Seri Portu:**
    *   `main.py` dosyasında, `arduino_port_name = "/dev/cu.usbmodem1301"` satırını Arduino'nuzun bağlı olduğu doğru seri port ile güncelleyin.
        *   Windows: "COM3", "COM4" vb.
        *   Linux: "/dev/ttyUSB0", "/dev/ttyACM0" vb.
        *   macOS: "/dev/cu.usbserial-XXXX" veya "/dev/cu.usbmodemXXXX"
*   **Bağımsız Test (IP Kamera):**
    *   `hair_detection_from_url.py` betiğini kullanıyorsanız, `CAMERA_URL` değişkenini kendi IP kamera akış URL'niz ile güncelleyin.

## Kullanım

1.  Gerekli yapılandırmaları (kamera kaynağı, Arduino portu) yaptığınızdan emin olun.
2.  Arduino'nun bilgisayara bağlı ve doğru kodun yüklü olduğundan emin olun.
3.  Ana uygulamayı çalıştırmak için:
    ```bash
    python main.py
    ```
4.  Uygulama çalışırken, kıl algılama sonuçları ekranda gösterilecek ve Arduino'ya ilgili sinyaller gönderilecektir.
5.  Çıkmak için 'q' tuşuna basın.

## `.gitignore` Dosyası

Proje, sanal ortam dosyaları, Python byte kodları, IDE yapılandırma dosyaları gibi gereksiz dosyaların Git repositorisine eklenmesini önlemek için bir `.gitignore` dosyası içerir.