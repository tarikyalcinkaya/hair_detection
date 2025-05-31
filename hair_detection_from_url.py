import cv2
import numpy as np
import requests

# Bu betik, bir IP kamera (örneğin ESP32-CAM) akışından görüntü alarak
# basit bir kıl algılama algoritması uygular.
# Bu, ana uygulamadan bağımsız, hızlı testler ve prototipleme için kullanılabilir.
# Temel olarak kenar algılama yoğunluğuna dayalı bir yöntem kullanır.

# ESP32-CAM veya başka bir IP kameranın video akış URL'si.
# ESP32-CAM genellikle "/capture" veya "/stream" gibi endpoint'ler kullanır.
CAMERA_URL = "http://192.168.4.1/capture"

def get_frame_from_url(url):
    """
    Belirtilen URL'den tek bir görüntü çerçevesi (frame) alır.

    Args:
        url (str): Görüntü akışının URL'si.

    Returns:
        np.ndarray or None: Başarılı olursa OpenCV formatında görüntü çerçevesi,
                            aksi takdirde None döner.
    """
    try:
        # URL'ye GET isteği gönder, timeout ile bekleme süresi sınırı koy
        resp = requests.get(url, timeout=5)
        resp.raise_for_status() # HTTP hata kodları için (4xx, 5xx) exception fırlat
        # Gelen cevabın içeriğini byte dizisine çevir
        img_array = np.asarray(bytearray(resp.content), dtype=np.uint8)
        # Byte dizisini OpenCV görüntü formatına decode et
        frame = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
        return frame
    except Exception as e:
        print(f"URL'den frame alınırken hata oluştu: {e}")
        return None

# Ana döngü: Sürekli olarak frame al, işle ve göster
while True:
    # Kamera URL'sinden güncel frame'i al
    frame = get_frame_from_url(CAMERA_URL)
    if frame is None:
        # Frame alınamadıysa bir sonraki iterasyona geç
        print("Frame alınamadı, tekrar denenecek...")
        cv2.waitKey(1000) # Kısa bir süre bekle
        continue

    # Görüntüyü renkli (BGR) formattan gri tonlamalıya çevir.
    # Kenar algılama algoritmaları genellikle gri tonlamalı görüntüler üzerinde daha iyi çalışır.
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Canny kenar algılama algoritmasını uygula.
    # 50 ve 150, düşük ve yüksek eşik değerleridir. Bu değerler,
    # hangi gradyanların kenar olarak kabul edileceğini belirler.
    edges = cv2.Canny(gray, 50, 150)

    # Kenar yoğunluğu oranı hesapla: Görüntüdeki kenar piksellerinin toplam piksel sayısına oranı.
    # Bu, görüntüde ne kadar "kenar" (dolayısıyla potansiyel kıl) olduğunu gösteren basit bir metriktir.
    edge_ratio = cv2.countNonZero(edges) / (edges.shape[0] * edges.shape[1])

    # Belirlenen eşik değerine göre kıl varlığını kontrol et.
    # Bu eşik değeri (0.02), deneysel olarak ayarlanmalıdır ve aydınlatma, kamera açısı gibi
    # faktörlere bağlı olarak değişebilir.
    if edge_ratio > 0.02:
        print("Hair detected ✅")
    else:
        print("No hair detected ❌")

    # Orijinal canlı görüntüyü ve algılanan kenarları göster (isteğe bağlı, hata ayıklama için yararlı)
    cv2.imshow("Live", frame)
    cv2.imshow("Edges", edges)

    # 'q' tuşuna basılırsa döngüden çık ve programı sonlandır
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Tüm OpenCV pencerelerini kapat
cv2.destroyAllWindows()
