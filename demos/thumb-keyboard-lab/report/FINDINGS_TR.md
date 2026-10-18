# İlk sonuçlar — 18 Ekim 2026

## Kapsam

Model: 14.811 sözcük biçimi / 11.912 eğitim + 2.899 bağımsız örneklem.
Aynı korpus ve boyutsuz fizik varsayımları tüm dizilimlere uygulandı.
Bu karşılaştırma **gerçek kişilerin yazım performansı değildir**.

| Düzen | Satır 1 / 2 / 3 | Hareket indeksi ↓ | Erişim indeksi ↓ | Tek parmak mesafesi ↓ | Yarısı değişen digraf |
|---|---|---:|---:|---:|---:|
| Q32 | `qwertyuıopğü` / `asdfghjklşi` / `zxcvbnmöç` | 1.664399 | 0.581907 | 0.505382 | %49.861 |
| F32 | `fgğıodrnhpqw` / `uieaütkmlyş` / `xjövcçzsb` | 1.205192 | 0.545255 | 0.480665 | %78.147 |
| V29 | `jfövücgzğş` / `puhaedrkst` / `çoıinlmyb` | 1.000775 | 0.458230 | 0.442483 | %82.205 |
| K29 | `jüövfczğpç` / `goetubrnds` / `hiaıylmkş` | 1.064227 | 0.403364 | 0.493860 | %80.560 |
| S29 | `fçjgözşücğ` / `vtumelinıd` / `hboyraksp` | 1.381120 | 0.461358 | 0.373122 | %45.115 |

## Matematiksel çıkarım (kanıt düzeyi: simülasyon)

- **V29**: Q32'ye göre hareket *proxy* indeksi %39.87 düşük;
  F32'ye göre %16.96 düşük. Bu, %39.87 daha hızlı yazım değildir.
- **K29**: Q32'ye göre reach *proxy* indeksi %30.68 düşük;
  29 tuşlu model altında konfor optimizasyonuna ayrılmış alternatiftir.
- **S29**: Q32'ye göre parmak yol uzunluğu %26.16 düşük;
  canlı swipe tahmini veya gerçek swipe uygulaması yoktur.
- **F32/Q32 swipe iddiasına karşı örnek:** Aynı corpus üzerinde F32'nin
  tek parmak geometrik mesafesi Q32'den %4.89 daha düşüktür. F'nin mutlaka
  daha fazla zigzag mesafesi yarattığı iddiası **genelleştirilemez**.
- **0.34 başparmak değişim katsayısının keyfiliği:** 0.25, 0.65, 1.0
  duyarlılıkları `results.json` içinde kaydedildi. Model kazananları
  katsayı seçimi ve cihaz/grip ile yeniden sınanmalıdır.

## Açık deneysel soru

V29 mı yoksa F32 mi, gerçekten en düşük KSPC ve en yüksek *alışma sonrası*
WPM sağlıyor? Hangi başparmak konumları daha az isabetsiz tıklanıyor?
**Bunların cevabı için henüz gerçek katılımcı ölçümü bulunmuyor.**

Değerlendirme sırası: gerçek erişim verisi → kişisel P29 → çapraz dizilim
yazma testleri → katılımcı içi değerlendirme → nihai karar.
