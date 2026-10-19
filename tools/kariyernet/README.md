# Kariyer.net — CV odaklı günlük iş ilanı arşivi

**Amaç:** Osman'ın yeni mezun makine mühendisi olarak uygun olduğu ilanları, Kariyer.net arama sonuçlarının ilk 4–5 sayfası ve izinli ek kaynaklardan kapsamlı biçimde toplamak; günlük GitHub arşivine kaydetmek. **Son değerlendirme ChatGPT tarafından kullanıcı istediğinde yapılır.** Sadece birkaç ilanı seçerek kalanları incelemeden geçmek doğru değildir.

> **Zorunlu ilk okuma:** [OSMAN_JOB_PROFILE.md](OSMAN_JOB_PROFILE.md). İş arama şehirleri, CV kanıtları, puanlama kuralları ve işveren araştırma talimatları buradadır. Kök [AGENTS.md](../../AGENTS.md) aynı politikaya yönlendirir.

## Çalışma şekli

1. GitHub Actions, uygun anahtar kelimelerle Kariyer.net listelerinin **ilk 4–5 sayfasını** hedefler. Gerekirse arama sorguları genişletilir veya değiştirilir. Gerçek erişim durumları, HTTP hataları, sayfalama doğrulaması ve URL sayıları raporlanır; başarısız sayfa başarı gibi gösterilmez.
2. Resmî/izinli kaynakların ilan metadatası da toplanır; doğrulanmamış Kariyer.net URL'leri gerçek ve açık ilan sayılmaz.
3. Günlük dosyalar deney dalında `data/kariyernet/daily/YYYY-MM-DD/` altında arşivlenir. Çıktılar: `discovered_urls.json`, `jobs.json/csv`, `report.json`, `official_jobs.json/csv`, `official_report.json`, `cv_ranked.json/csv`, `cv_ranked_report.json`, `regional_source_candidates.json` (iş akışı sürümüne göre).
4. Kullanıcı ilan incelemesi istediğinde asistan **tüm arşiv kayıtlarını**, yeni/mevcut tekrarları ve erişim durumlarını inceler; uygun olan **tüm** ilanları puan ve gerekçeleriyle sunar. Önceden seçilmiş 1, 3, 5, 10 gibi sabit adet sınırı uygulanmaz.
5. **Önerilecek her şirket için** şirketin kendi tanıtımı dışındaki kaynaklardan faaliyet alanı, büyüklük (doğrulanabilirse), piyasa/itibar ve risk değerlendirmesi yapar. Başvuru açık mı, deneyim/yabancı dil/mezuniyet koşulları neler, ayrıca kontrol edilir. Doğrulanamayan unsurlar belirtilir.

## Kapsam ve güvenlik
- Öncelik: Kahramanmaraş, Gaziantep, Osmaniye, Adana, Kayseri, Malatya; ikinci sıra Mersin, Ankara. İstanbul kapsam dışı.
- Pozisyonlar: yeni mezun makine/üretim/imalat/kalite/mekanik tasarım/CAD/Ar-Ge/proses mühendisi, 0–2 yıl deneyim önceliği. Yazılım ve AI yalnız tamamlayıcı avantajdır.
- Site kısıtlamalarına ve robots.txt'ye uyulur. Kimlik doğrulaması, cookie/proxy/CAPTCHA aşma yöntemi uygulanmaz.
- Her HTTP 200 veya URL keşfi, geçerli başvuru kanıtı değildir. Güncel ilan ve açık başvuru bilgisi kaynağında doğrulanmalıdır.
- Günlük otomatik workflow `.github/workflows/kariyernet-nightly.yml` (varsayılan dal); deney/workflow dispatch `.github/workflows/kariyernet-jobs.yml`. Otomatik çalışmanın başarılı olacağı veya her ilanı okuyacağı garanti değildir.

## Güncelleme
Tercih ve CV değişiklikleri yalnız doğrulanmış kullanıcı bilgisiyle [OSMAN_JOB_PROFILE.md](OSMAN_JOB_PROFILE.md) içinde güncellenir. Bu belgeyi ve ilgili AGENTS.md dosyasını sonraki oturumda ilk önce oku. Üretilen günlük arşivler salt okunur analizde değiştirilmez.

## Standart çıktı sözleşmesi
Kullanıcı arşivdeki ilanları incelettiğinde çıktı **tek kompakt, filtrelenebilir ve sıralanabilir karşılaştırma paneli** olmalı. Her aday satırında: CV puanı, şirket, pozisyon, şehir, deneyim, gerçek ilan/açık başvuru durumu, doğrudan ilan URL'si ve **açılır, ayrıntılı bağımsız şirket incelemesi** bulunur. Bütün uygun ilanları kapsa; keyfî 3/5/10 sınırı koyma. Tek bir uzun, parçalı şirket listesi üretme.

Şirket ayrıntısı: yapılan iş/ürün/hizmetler, fiziksel ve ticari ölçek (kanıtlı göstergeler), bağımsız resmî/medya/sector kaynakları, ekonomik ve operasyonel durum, işveren itibarına dair olumlu/olumsuz sinyaller, çalışan yorumlarının kaynak ve örneklem sınırlamaları, ücret/mesai/İSG riskleri, kritik bilinmeyenler, mülakatta sorulacak sorular, kullanıcı için gerekçeli sonuç. Kaynakları ve tarihleri açıkça göster. Şirketin kendi reklâmını bağımsız araştırma sanma. Kanıt bulunamayan konuyu uydurma. Ayrıntı panelde açılır; satır görünümü kısa kalır.
