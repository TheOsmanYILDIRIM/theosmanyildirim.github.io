İlk oynanabilir test.

- Arka plan: düz/boş koyu renk
- Kontrol: ekrana dokun / Space / yukarı ok
- Kuş: hazırlanan uçuş animasyonu
- Engel: üst-alt heykeller
- Heykeli geçince: ölüm animasyonu
- Skor ve en iyi skor tutulur

Android/Termux:
cd ozlem_flappy_test
python3 -m http.server 8080
Tarayıcı: http://127.0.0.1:8080


V2 değişiklikleri:
- assetler lossy WEBP'ye çevrildi
- kuş biraz daha içeri alındı
- heykel yüksekliği sabit tutulup kalan mesafe platform tabanı uzatılarak dolduruluyor


V3:
- kuş x=280'e taşındı; başarılı geçişte heykel hâlâ ekranda
- ölüm animasyonu 24 FPS ve çok yavaş yatay sürükleniyor
- dikdörtgen çarpışma kaldırıldı; heykelin gerçek alpha silueti kullanılıyor
- kuş assetlerindeki küçük kopuk pixel/artifact parçaları temizlendi
- platform uzatma korunuyor; heykel en-boy oranı bozulmuyor


V4:
- ölüm animasyonu artık kuşun küçük hitbox'ı geçince değil, görünen sprite tamamen geçince başlıyor
- ölüm animasyonu V3'e göre 1.3x hızlı: 24 -> 31.2 FPS
- ölüm animasyonu sırasında heykel sabitlenmiyor; sola 68 px/sn kaymaya devam ediyor
- animasyon süresi/fade buna göre yeniden ayarlandı


V5:
- ölüm animasyonu artık engel geçildikten sonra değil, heykelin merkezi kuşun X çizgisine geldiği anda başlıyor
- animasyon sırasında heykel sola kaymaya devam ediyor (110 px/sn)
- 31.2 FPS ölüm animasyonu korunuyor


V6:
- skor 10'u geçtiğinde (11 olduğunda) Q9XmJf0hKOY videosunun sesi bir kez oynatılır
- her yeni oyunda bir kez tetiklenebilir
- ses YouTube kaynağından çevrimiçi oynatılır; oyun asset paketine üçüncü taraf video sesi kopyalanmamıştır


V7:
- skor 10 ve üstü için yeni oturan heykel seti eklendi
- bu yeni setin idle sprite'ı yüklediğin görselden üretildi
- yeni setin death animasyonu yüklediğin 116611.mp4 videosundan üretildi
- 10'dan sonra doğan engeller yeni seti kullanır; ekrandaki eski engeller olduğu gibi devam eder


V8:
- cehennem harabeleri parallax arka planı oyuna eklendi
- arka plan 4 ayrı katman gibi farklı hızlarda kayıyor
- skor 10 sonrası faz II etiketi beliriyor
- skor 10 sonrası engel hızı artıyor ve gap biraz daralıyor
- skor 20 sonrası zorluk bir kademe daha artıyor


V9:
- parallax katmanları artık üst üste binmiyor; her biri kendi clip bölgesinde çiziliyor
- 10+ oturan heykel death animasyonu yeniden işlendi; tam sandalye/gövde silueti korunuyor
- idle ve death için aynı genel çerçeve kullanıldı, böylece animasyon görselle daha tutarlı hizalanıyor


V10:
- 10+ heykel idle pozu artık death videosunun ilk karesiyle birebir eşitlendi; idle -> animasyon geçişinde zıplama/pop azalır


V11:
- kuleler 2x büyütüldü (genişlik 138 -> 276)
- yatay spawn mesafesi artırıldı ve ilk kule daha uzaktan başlıyor
- dikey gap büyütüldü; 10+ ve 20+ fazlarda buna göre yeniden ayarlandı
- alttan/üstten uzatma artık sert biçimde doldurmuyor; platform uzatma miktarı sınırlandı
- kuleler ekranı tamamen doldurmak zorunda değil; gerekirse uç kısımlarda daha fazla boşluk kalabiliyor


V12:
- düz uzatma yerine ayri silindirik kaide asseti eklendi: assets/pedestal.webp
- 10 öncesi ayakta heykeller artık kaideyi altlarına alıyor
- kaide, segmente göre gerektiği kadar görünür; eski gibi taş platform dokusu esnetilmiyor
- çarpışma hesabına kaidenin alpha silueti de eklendi


V13:
- kaide assetinin siyah arka planı temizlendi ve transparan hale getirildi
- ayakta heykellerde kaide artık önde değil arkada çiziliyor; heykel kaidenin önünde birleşik görünüyor
- tek kaide yerine birden fazla kaide alt alta stack ediliyor; uzunluk yetmezse arkada devam ediyor
- çarpışma hesabı, tekrarlanan kaide stackine göre güncellendi


V14:
- 1) oynanış hissi polishlendi: flap squash/stretch, yumuşak rotasyon, kamera sarsıntısı ve iz partikülleri
- 2) çarpışma daha adil hale getirildi: kuş hitbox'ı küçültüldü ve örnekleme sıklaştırıldı
- 4) difficulty director / pattern sistemi eklendi: faz bazlı hız-gap-spawn ve tasarlanmış pattern dizileri
- 5) game juice eklendi: skor pop-up'ları, geçiş partikülleri, flash, faz banner'ı ve death burst


V16:
- menu, game over ve parallax PNG assetleri alpha koruyan lossy WebP'ye dönüştürüldü
- dosya referansları .webp olarak güncellendi
- amaç paket boyutunu düşürmek ve açılış/yüklemeyi hızlandırmak


V17:
- parallax katmanları yeniden hizalandı
- artık yükseklikten türeyen dar tile'lar yerine genişlik bazlı büyük katmanlar kullanılıyor
- katmanlar alt çizgiden hizalanıyor ve üst üste daha bütünleşik görünüyor
- yatay kopukluk/seam etkisi azaltıldı


V18:
- 13) score 10/20 faz geçişlerinde gerçek transition state, kararma/kızarma, banner ve yeni heykel önizlemesi
- 14) bird/death animasyonları spritesheet atlaslarına taşındı
- 16) load sayısı azaltıldı, obstacle pooling ve particle/popup cap eklendi, DPR 1.75 ile sınırlandı


V19:
- atlas frameleri için assetReady eklendi; ölüm animasyonu sırasında kulelerin görünmemesi düzeltildi
- parallax katmanları daha geniş, daha alttan hizalı ve daha fazla üst üste binecek şekilde ayarlandı


V20 SFX:
- Web Audio procedural SFX sistemi eklendi; ekstra ses dosyası yok
- flap: kısa hava/kanat + düşük ton
- near pass: hafif whoosh
- score: kısa yükselen chime
- statue death: taş kırılma + düşük impact
- phase transition: drone + yükselen motif
- player death: ağır impact
- game over: üç notalı düşen motif
- start/restart: kısa UI tonu
- master SFX gain: 0.58


V21 RUBBLE ACCUMULATION:
- her heykel ölüm animasyonu başladığında taş/parça kümesi oluşuyor
- parçalar yerçekimiyle aşağı düşüp ekran tabanında yığılıyor
- aynı yığın içinde kolon/layer mantığıyla parçalar birbirinin üstüne oturuyor
- yığın dünya ile birlikte sola akıyor; ekrandan çıkana kadar kalıcı
- performans için aynı anda en fazla 10 rubble pile tutuluyor


V22 INTRO VIDEO:
- kullanıcı videosundan transparan intro atlas üretildi
- near-white arkaplan temizlendi
- 72 frame, 12 fps, atlas 6x12, frame 380x676
- oyun açılınca intro bir kez oynuyor; dokunarak skip edilebiliyor


V24 INTRO FLOW:
- intro artık oyun açılır açılmaz oynamıyor
- önce normal ana menü/ready ekranı geliyor
- DOKUN / SPACE ile Oyunu Başlat denince intro animasyonu oynuyor
- intro boyunca input kilitli; intro bitince gameplay otomatik başlıyor
- game over sonrası dokununca önce menüye dönüyor; yeni oyun başlatılırsa intro tekrar oynuyor


V25 PERFORMANCE:
- devasa tek atlaslar kaldırıldı; animasyonlar küçük paged atlaslara bölündü
- bird atlas frame 640x432 -> 180x122
- statue death frame 288x512 -> 144x256
- intro frame 380x676 -> 300x533 ve 6-frame sayfalara bölündü
- tüm sayfalar loading ekranında decode + prewarm ediliyor, ilk animasyon geçişinde decode takılması azaltıldı
- parallax 2172x724 -> 1200x400, UI 1122x1402 -> 600x750, pedestal 1122x1402 -> 256x320
- DPR üst sınırı 1.5 yapıldı
