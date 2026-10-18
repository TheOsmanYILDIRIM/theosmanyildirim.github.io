# Başparmak Atlası — Türkçe mobil klavye deney laboratuvarı

**Durum: Yerel prototip ve tekrarlanabilir matematiksel simülasyon hazır.**
Gerçek Android/iOS katılımcı verisi **henüz yoktur**. Çıktılar gerçek yazım hızı,
ergonomik üstünlük veya klinik yorgunluk kanıtı değildir.

## Kullanım

- Telefonda tek başına çalışan [`index.html`](index.html) dosyasını tarayıcıda aç veya site üzerinde HTTPS'den sun.
- **01 · Karşılaştır**: Q32, F32, V29, K29, S29 dizilimlerinin *bağımsız* korpus üzerindeki proxy skorlarını göster.
- **02 · Erişim haritası**: Sol ve sağ başparmak için 30 hedefe ayrı ayrı bas. Böylece kişisel harita oluşturulur. İstersen P29 kişisel dizilimi oluştur; gerçek insan verileri olmadan P29'in avantajı kanıtlanmaz.
- **03 · Yazma testi**: Her dizilim için aynı kelime bloğunu (10 sözcük) yaz. Deneme süresi, WPM, KSPC, geri silmeler / hata ve aynı yarı–farklı yarı geçişlerini kaydet. Özet CSV veya ham JSON indir.
- Sayfa **veriyi otomatik hiçbir sunucuya yüklemez**; kayıtlar sayfa belleğindedir, yenilemeden önce dışa aktar.

## Kaynak ve örneklem

[FrequencyWords Turkish tr_50k.txt](https://github.com/hermitdave/FrequencyWords/blob/master/content/2016/tr/tr_50k.txt)
(HermitDave 2016, OpenSubtitles verisi temelli; özgün proje MIT lisansı).
Kaynak Git blob SHA-1:
`f7c73d59b5654be9b10c38a17ce65fbc82ad3a35`.
İlk 15.000 frekans sıralaması girdisi incelendi, yalnız Türkçe 29 harfli
2–25 karakterlik biçimler korundu: **14.811** sözcük biçimi.
Kararlı FNV-1a `word` hash %20 → **2.899 bağımsız değerlendirme**; kalan
**11.912** biçim → eğitim. Ağırlık `round(sqrt(freq))`; korpusun üst
sıralardaki birkaç yüksek frekanslı sözcük tarafından ele geçirilmesini azaltmak
için kullanıldı. Boşluk/punktuasyon ve sözcükler arası harf çiftleri modele
dahil değil; korpus günlük konuşma altyazısını temsil eder, tüm Türkçeyi değil.

## Yöntem

Baselines Türkçe Q32/F32; adaylar Türkçe alfabesinin tamamıyla **29 tuş**
(10+10+9). Dizilimler harflerin pozisyon permütasyonunu arayan sabit tohumlu
tavlama (`src/layout_engine.py`, hedef başına 3 × 2500 hamle) ile seçilir.
Kararların sınandığı bağımsız %20 korpus sadece son değerlendirmede kullanılır.
Bu algoritma **global optimum garantilemez**.

Boyutsuz model:
- `D` tuş merkezleri arası normalize mesafe, `W` hedef tuş genişliği.
- Aynı yarıya geçiş `log2(1+D/W)`; yarı değişiminde **0.34 ×**.
- Varsayımsal başparmak ideal noktaları normalize `(0.22,0.72)` ve `(0.78,0.72)`;
  reach cezası hareket/yorgunluk için bir *prior*, deneysel gerçek değil.
- `balance` amaç: `0.64 × motion + 0.27 × reach + 0.09 × width_penalty`.
- `comfort` amaç: `0.34 × motion + 0.55 × reach + 0.11 × width_penalty`.
- `swipe` amaç: `0.84 × glide_distance + 0.13 × reach + 0.03 × width_penalty`.
  S29 henüz **gerçek swipe tanıma arayüzüyle test edilmez**; tek-parmak
  mesafe modeli karşılaştırmasıdır.

İki başparmak kullanımının klavye yarılarıyla birebir örtüştüğü varsayılır.
Pointer event API gerçek parmak kimliğini vermez. Belirtilen `mode` seçimleri
görev yönergesidir; yazılımsal zorlaması yoktur. İnsan tepkisi ölçümü hedef
görme + karar + motor hareketi içerir, saf biyomekanik menzil değildir.
Her hücre için tek ölçüm güvenilirlik sınırıdır; P29 her ölçümü
4 gözlemlik teorik önsel ile yumuşatır. Kalibrasyon sırayla hedef seçer,
sabit sırayı rastgele tohumla karıştırır. Dokunma bölgesi = tuş merkezi sol/sağ
yarısı; gerçek başparmak değişimi doğrudan algılanmaz.

## Çalıştırma ve test

Python 3.11+, numpy ve pytest; tarayıcı testi için playwright ve Chromium
gereklidir. Çevrimdışı çalışan HTML build'i standart Python ile oluşturulur:

```bash
python src/layout_engine.py --iterations 2500 --restarts 3
python src/build.py
pytest -q
```

Eşleşen tam sözcük kaynağı mevcutsa agregatı yeniden üret:

```bash
python src/rebuild_corpus.py --input tr_50k.txt
```

İlk indirimi güvenilir ağda yapmak için `--input` yerine `--download` kullanılabilir.
Hash tutmazsa dosya kullanılmaz. Sonucu `report/results.json` ve HTML içine gömer.

## Gerçek katılımcı protokolü — henüz uygulanmadı

En az birkaç farklı el boyu, cihaz genişliği ve alışkanlığına sahip kullanıcı
ile tekrarlı ölçüm gerekir:

1. Sabit ekran genişliği, klavye yüksekliği, tutuş (iki başparmak) ve
   otomatik düzeltme kapalı koşulu tanımla.
2. Her iki başparmak için hedef haritasını **en az 3 kez** kaydet;
   30 hücre × 3 tekrar × 2 el. Hatalı hedeflerde tepki sürelerini ayrı ele al.
3. Her dizilimde **alışma denemeleri** yap; ilk denemeyi performans verisinden ayır.
4. Latin-square veya dengeli rastgele sıra ile Q/F/V/K/P düzenlerini
   karşılaştır. Aynı sözcük blokları, benzer kelime zorluğu ve farklı
   blok sırası (hafıza etkisi) kullan.
5. Her dizilim için 5–10 tekrar ve birden fazla gün sonunda WPM, KSPC,
   toplam düzeltme ve digraf gecikmesi dağılımlarını karşılaştır;
   katılımcı eşleştirilmiş istatistik ve %95 güven aralığı raporla.
6. Tek parmak modu ayrıca yürütülmeli; S29 için gerçek swipe testi yapılmadan
   dokunma verisinden swipe üstünlüğü çıkarma.

Bu v1'de **otomatik karşılaştırmalı insan analizi / istatistiksel anlamlılık**
yapılmamıştır; dışa aktarılan verilerin katılımcı bazlı analizi takip işidir.
Bu veri toplamadan "nihai en iyi klavye" demek bilimsel değildir.

## Gizlilik ve arşivleme

Parmak dokunuşlarının `clientX/Y`, süre ve cihaz viewport bilgisi kişisel
davranışsal ölçüm olabilir; bir sunucuya otomatik aktarılmaz. CSV/JSON indirme
yalnız katılımcının açık eylemiyle yapılır. **Supabase** hesabında bulunan
`github-control-plane` projesi mevcut GitHub kontrol iş akışına ait; deney
verisi için *ayrı güvenli tablo ve RLS* kurulmadan ona biyometrik veya davranış
verisi yüklenmedi. Canlı veritabanı / katılımcı girişi bu prototipin kapsamında
değildir. GitHub'a yalnız kod ve anonim **korpus agregatları** gönderilebilir.

## Kaynaklar / doğrulama sınırları

- HermitDave, FrequencyWords, `content/2016/tr/tr_50k.txt` (upstream dosya
  ve MIT LICENSE üzerinden doğrulandı).
- Türkçe Q ve F geleneksel dizilimleri: kopyalanmış sıra listesi değil,
  `src/layout_engine.py` içinde açık `Q32`/`F32` referansları.
- Fitts's law yaklaşımı bir hız sabiti ölçmez; sonuçlara *indeks* denir.
- Otomatik Playwright testi sentetik dokunma üretir. Headless Chrome
  ekran görüntüleri **Android cihaz testi değildir**, gerçek WPM göstermez.
- Kritik sınırlama: `index.html` içinde tüm JS/CSS/JSON inline üretildiğinden
  bir telefon tarayıcısında bağımsız açılabilir; gerçek cihaz açılışı yapılmadı.
