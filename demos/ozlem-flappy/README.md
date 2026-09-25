# Özlem Flappy Test (v25)

HTML5 Canvas tabanlı, gelişmiş animasyonlu, dinamik boss/heykel geçişli ve parallax arka planlı Flappy tarzı arcade web oyunu.

🎮 **Canlı Oyna (GitHub Pages):** [https://theosmanyildirim.github.io/ozlem-flappy-test/](https://theosmanyildirim.github.io/ozlem-flappy-test/)

---

## 🕹️ Oyun Kontrolleri

| Cihaz | Kontrol |
|---|---|
| **Mobil / Tablet** | Ekrana Dokunma (Tap) |
| **Masaüstü / Klavye** | `Space` (Boşluk) veya `Yukarı Ok` (`↑`) tuşu |
| **Fare** | Sol Tık |

---

## ✨ Özellikler

- **Özel Karakter & Animasyon:** Akıcı kanat çırpma ve ölüm animasyonları.
- **Faz / Kademe Mekaniği:**
  - **Faz 1 (0-10 Skor):** Ayakta duran heykeller, kaideli engeller ve hafif tempo.
  - **Faz 2 (10+ Skor):** Oturan heykeller, yeni ölüm animasyonu, hız artışı ve görsel faz banner'ı.
- **Parallax Cehennem Harabeleri:** 4 bağımsız katmandan oluşan derinlik hissi veren arka plan (`fog`, `near`, `mid`, `far`).
- **Game Juice & Polish:** Flap squash/stretch, kamera sarsıntısı, skor pop-up'ları, geçiş partikülleri.
- **WebP & Atlas Optimizasyonu:** Hızlı yükleme için optimize edilmiş hafif grafik atlasları.
- **Duyarlı / Responsive:** Masaüstü ve mobil ekran boyutlarına otomatik uyum sağlayan dinamik canvas ölçekleme.

---

## 🛠️ Yerel Çalıştırma

Termux veya yerel terminal üzerinden:

```bash
# Proje dizinine geçiş
cd ~/projects/ozlem-flappy-test

# Yerel HTTP sunucusu başlat
python3 -m http.server 8080
```

Tarayıcıdan açın: `http://localhost:8080` veya `http://127.0.0.1:8080`
