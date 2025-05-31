from dataclasses import dataclass
from enum import Enum

# Bu dosya, projenin temel veri yapılarını ve varlıklarını tanımlar.
# "Domain Entities" olarak adlandırılan bu yapılar, iş mantığının temel taşlarıdır.


class HairPresence(Enum):
    """
    Kıl algılama sonucunun durumunu temsil eden enum sınıfı.
    Bu, algılama sonucunun "Kıl Var" mı yoksa "Kıl Yok" mu olduğunu belirtir.
    Enum kullanmak, bu durumları sabit ve güvenli bir şekilde temsil etmeyi sağlar.
    """
    HAIR = "Hair"
    NO_HAIR = "No Hair"


@dataclass
class DetectionResult:
    """
    Kıl algılama işleminin sonucunu tutan veri sınıfı (dataclass).
    Bu sınıf, algılanan durumu (HairPresence) ve algılamanın güven skorunu içerir.
    Dataclass kullanmak, basit veri tutucularını hızlı ve okunaklı bir şekilde oluşturmayı sağlar.
    """
    presence: HairPresence
    confidence: float  # Güven skoru, genellikle 0 ile 1 arasında bir değer alır.
                       # Bu değer, algılamanın ne kadar kesin olduğunu gösterir.
