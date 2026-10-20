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

## Şirket dosyası: sektör ve somut faaliyet
İlan panelinde **Sektör** sütununu göster. Her açılır şirket dosyasına önce şirketin ürettiği ürünler, sunduğu hizmetler, müşteri sektörleri ve faaliyet bölgeleriyle başla. Sonra üretim teknolojileri, tesisler, makine parkı ve makine mühendisinin olası gerçek görevlerini kaynaklara dayanarak açıkla. Ardından ölçek, mali/operasyonel kanıtlar, çalışan deneyimleri, riskler, CV uyumu ve mülakat soruları gelsin. Şirketin kendi beyanlarıyla bağımsız doğrulamayı ayır; bilinmeyen bilgiyi uydurma.

## Değerlendirilen ilanlar ve engellenen şirketler
- `tools/kariyernet/reviewed_listings.json`: yalnız ilan başına `provider + listing_id` kimliğiyle değerlendirilmiş kayıt. Kullanıcı 2026-10-19'da 18 Ekim 2026 arşivinden kullanıcıya gösterilen 48 Kariyer.net ilanını incelendi saydı; geri kalan 30 URL incelendi kabul edilmez. Başka ilanları veya aynı şirketin yeni ilanlarını engelleme.
- Şirket yasağı küçük olduğu için mevcut `tools/kariyernet/OSMAN_JOB_PROFILE.md` içindeki `company_key` kayıtlarından okunur. Kesin işveren kaynak anahtarı kullan; genel ad parçası, benzer firma ismi veya serbest metin eşleştirmesiyle şirket engelleme. Belirsiz kimlik eşleşmelerini manuel teyide bırak.
- `tools/kariyernet/filter_candidates.py` günlük toplama **sonrasında** ayrı yeni-aday ve elenenler dosyası üretir. Ham keşif ve resmî kaynak arşivini değiştirme. Kullanıcıya önerirken `new_kariyernet_candidates.json` ile `new_official_candidates.json` kullan; adayları ayrıca gerçek başvuru koşulları açısından doğrula. `excluded_candidates.json` inceleme izi olarak kalır.
- Bundan sonra incelendi kararı alınan ilanların ID'si aynı JSON kaydına eklenmeli; dosya güncellemesinde mevcut SHA ve kapsam doğrulanmalı. Eski inceleme kayıtları silinmemeli.

## Genişletilmiş arama ve kanıta dayalı sıralama (2026-10-20)
- `search_families.py` rol ve teknoloji sorgu aileleri sunar. `search.py --expand` ek sorgularla tarar; sayı sınırı ve robots/403 davranışı korunur. Başarılı HTTP yanıtı kapsam garantisi değildir.
- İlk değerlendirme `filter_candidates.py`: aynı ilan ID'si tekrar önerilmez, yalnız tam kimliği bilinen yasaklı şirket filtrelenir. 54 incelenmiş ilan kimliği ve Isısan kaydı korunur.
- İkinci değerlendirme `smart_rank.py`: meslek (25), zorunlu koşullar (25), beceriler (20), kariyer (15), şehir (10), **bağımsız işveren kanıtı** (5). Ayrı `status`, `requirements_state` ve `open_state` alanları bulunur. Bilinmeyen gereklilikler doğrulanmış sayılmaz.
- `employer_evidence.json` yalnız tam kaynak kimliği (`lever`/board token) ile eşleşen, URL ve somut iddia içeren bağımsız kaynaklar için puan katkısı sağlar; şirketin iyi işveren olduğunun kanıtı veya güvenilirlik notu değildir. Çalışan deneyimleri ve finansal gelişmeler asistan tarafından güncel bağımsız araştırmayla ayrıca doğrulanır. Kaynağı bulunmayan şirketler 0/5 kanıt puanıyla kalır.
- `smart_ranked.json/csv` ve `smart_ranked_report.json` günlük iş akışının parçasıdır. Bu otomatik sıralama yalnız **ön elemedir**. Kullanıcı istediğinde adayların tümünü güncel ilan ve bağımsız şirket incelemesiyle değerlendir; keyfî üst sınır koyma.
