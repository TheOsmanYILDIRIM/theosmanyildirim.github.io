---
name: efficient-subagent-orchestration
description: ChatGPT'de çok sohbetli/çok ajanlı proje çalışmalarını planlar; gerçek araç yeteneğine göre iş bölüştürür, her ajana bağımsız kaynak ve dosya sahipliği sınırı verir, sonuçları kanıtla doğrular ve güvenli şekilde bütünleştirir. Çok parçalı geliştirme, araştırma, GitHub branch entegrasyonu, "ajanları ayır", "alt ajan planla", "devam" ve devir işleri için kullan; küçük tek görevlerde gereksiz ajan açmaz.
---

# ChatGPT için Verimli Alt Ajan Orkestrasyonu

**Hedef:** Kullanıcıya daha hızlı değil, *kanıtlanmış ve birbirini bozmayan* bir bütünleşik çıktı sun. ChatGPT'nin mevcut oturumunun ve araçlarının gerçek sınırları her zaman video örneklerinden daha önceliklidir.

## 1. Hangi çalışma biçimi gerçekten mümkün?

Önce mevcut oturumun yeteneklerini doğrula. Gerçekte olmayan alt ajan / terminal / arka plan oturumu icat etme.

- **Tek ChatGPT sohbeti:** Sen koordinatörsün; ilgili analiz ve uygulanabilir işi bizzat araçlarla yap. Paralel bağımsız *araç çağrıları* mümkünse kullanabilirsin, ama bunlara bağımsız model ajanları deme.
- **Kullanıcı ayrı ChatGPT sohbetleri açıyorsa:** Her alt sohbet için kendi başına anlaşılır bir görev brifi hazırla. Bunlar otomatik senkronize olmaz. Aynı veriye ve depoya eriştiklerini varsayma; sonuçları ilgili repo dalından veya kullanıcının geri bildirdiği kanıtlardan oku.
- **Gerçek delege/Work/Codex/bağlı yürütücü varsa:** Sadece araç gerçekten sunuluyorsa çağır. İşin arka planda sürdüğünü ancak başarılı başlatma/otomasyon kaydıyla söyle; gelen sonuçları ayrıca oku. Work/Computer Use özelliği ile bağımsız alt ajan yeteneğini birbirine karıştırma.
- **Yazma/CI erişimi yoksa:** Uygulanabilir, kopyalanabilir bağımsız brifler ve entegrasyon sırası üret; işin uygulandığını iddia etme.

Gerçek çalışma seçenekleri ve örnek mesajlar: [ChatGPT çalışma biçimleri](references/chatgpt-modes.md).

## 2. Bölüştürmeden önce kapsamı doğrula

1. **İş türünü ayır:** Sıradan sohbet, öneri veya salt okunur incelemede otomatik görev/dal/dosya oluşturma. Geliştirmede güncel depo kuralları, README, görev ve karar kayıtları, branch/HEAD ve ilgili kod/testleri aç.
2. **Tek kaynak seç:** Proje kayıtlarının gerçek yeri, kabul kriterleri ve korunan kaynaklar. Var olan görevi ve dalı kullan; tamamlanmış işi tekrarlama. Yetkisiz yeni kayıt düzeni oluşturma.
3. **İş grafı oluştur:** Her parçanın girdisini, çıktısını ve bağımlılığını belirle. Aynı sözleşmeye dayanan işler önce sözleşmeyi kararlaştırmadan paralelleşmesin.
4. **Delege etmeye değer mi?** Tek dosya, küçük hata, çok yüksek bağımlılık, tek onay gerektiren karar veya entegrasyon ağırlıklı işlerde **tek koordinatör yeterlidir**. Çok ajan sayısı başarı ölçütü değildir.
5. **Ortak kırmızı çizgiler:** Public API, veri/saveler, kimlikler, dosya sahipliği, test/CI, üretim dalı, gizli bilgiler, kullanıcı onayları.

## 3. Gerçekten bağımsız görevler için ajan sözleşmesi

Her alt ajan brifi şu alanları içermelidir; kısa ve sınanabilir tut, hayali beceri/izin yazma:

- **HEDEF:** Son kullanıcıda gözlenebilir çıktı ve *neden*.
- **KAYNAK:** Tam repo/klasör, mevcut dal, son *doğrulanmış* HEAD ve yeniden doğrulama talimatı.
- **SAHİPLİK:** Yalnız değiştirilebilen dosyalar; diğer ajanlara ait dosyalar *salt okunur*; ortak config/API için tek yazıcı.
- **SÖZLEŞME:** Stabil ID, şema, dosya formatı, bağımlı ajan çıktısı, uyulacak eski kararlar.
- **BİTTİ:** Gerçek test komutları, CI tetikleyicisi, beklenen artifact ve olumsuz/regresyon senaryoları.
- **DUR/ENGEL:** Eksik kaynak/izin, sözleşme çakışması, tekrarlayan hata, veri riski, bilinmeyen varsayım.
- **TESLİM:** Commit/branch, değişen dosyalar, yapılan gerçek test/run linki, karar, eksik, sonraki adım. Raporu kendi yetkili dalında tut; koordinatör oradan okur.

Kopyalanabilir kalıp: [Ajan görevi](assets/agent-brief.md).

## 4. Çalıştırma ve izleme

- **Araştırma** ve dış kaynak incelemelerini önce salt okunur paralel şeritler olarak ayır; sonuçları kısa, kaynak işaretli raporlara indir.
- **Kod yazımı** için ayrık yazma kapsamı/branch/worktree kullan. Aynı kritik dosyada birden çok yazar varsa önce seri hâle getir veya tek sahip ata.
- **Ana koordinatör** sözleşmeyi, kullanıcı kararlarını, entegrasyonu ve kalite kapısını yönetir; ama tek başına çözülebilen küçük işleri sırf “şef işçilik yapmaz” sloganı uğruna delege etmez.
- **Seyrek durum kontrolü:** Gerçek run/commit/artefact yokken görev tamamlandı deme; alt ajanlardan uzun tekrar isteme. Gelen raporlardaki iddiaları ilgili kaynak ve testle çapraz denetle.
- **Değişiklik gerekçesi:** Sahadaki kanıt plana aykırıysa planı sorgula ve güncelle; ama kullanıcı tarafından kilitlenmiş kararları tek taraflı değiştirme.
- **Yetki ve süre:** ChatGPT sohbetini başlatınca kendiliğinden geceleri çalışan bir döngü varmış gibi davranma. Gerçek bir otomasyon/Work görevi isteniyorsa ancak desteklenen araçlarla kur, sonucu kontrol et.

## 5. Birleştirme ve kalite kapısı

1. Her dalın HEAD'ini, farkını ve dosya sahipliğine uyumu oku; kör merge yapma.
2. Bağımlılık sırasıyla birleştir: **sözleşme → runtime/veri → asset/UI → sistem davranışı**.
3. **CI yeşil ≠ ürün doğru:** Yeni testlerin workflow tarafından gerçekten çalıştırıldığını doğrula. Görsel ve kullanıcı davranışı önemliyse gerçek ekran/görsel smoke sonuçlarını incele. Cihaz doğrulaması başka bir kanıttır.
4. Bağımsız dal testleri birleşik sistem testinin yerine geçmez. Son birleşimin CI/artifact/çalışan ürün kanıtını iste.
5. **Bitti ≠ ajan “bitti” dedi:** Dosya/commit/CI/artifact/gerçek test mevcut ve kabul ölçütü karşılanmış olmalı. Aksi hâlde `blocked`, `waiting` veya `unverified` şeklinde açık bırak.
6. Uygulama sonunda önceki proje görev ve karar kaydını güncelle; yeni mükerrer kayıt üretme. Kapat istenirse yeni geliştirme başlatma.

Kısa teslim şablonu: [Entegrasyon raporu](assets/integration-report.md).

## 6. Kısa karar algoritması

- **Tek küçük ve net iş?** Tek oturumda yap → doğrula → bitir.
- **Birden çok bağımsız iş, ortak sözleşme sabit?** Kapsamları ayır → brifleri ver → mümkünse paralel yürüt → ayrı doğrula → entegre et.
- **Bir iş diğerinin şemasını bekliyor?** İlk bağımlılığı bitir, sonra ikinci dalgayı başlat.
- **Kullanıcının açacağı ayrı sohbetler mi?** Ajan sırası + kopyalanabilir bağımsız görev mesajları ver; senin otomatik başka sohbet yönettiğini iddia etme.
- **Salt okunur / yalnız fikir?** Kod, repo, Beyin, dosya veya otomasyon yazma.
- **Engelli araç veya yarım test?** Yapılabileni teslim et; engelin kaynağını ve izlenecek somut adımı açıkla.

## Kaynakların kullanımı

Bu beceri eski skill'in özetinden değil, **Forn AI ve Avenox altyazı arşivinin yeniden taranması ve odaklı kaynak incelemesinden** üretildi. [Kaynak değerlendirmesi ve karşıt bulgular](references/caption-reassessment.md) içindeki ayrımı koru: *kanalda söylenen*, *videoda gösterilen*, *ChatGPT için burada önerilen* ve *bağımsızca doğrulanan* aynı şey değildir. Güncel platform özellikleri için resmî dokümantasyon ve gerçek araç durumunu esas al. Uzun rol promptları, sabit model sıralamaları veya videoya özel CLI komutlarını evrensel kural yapma.