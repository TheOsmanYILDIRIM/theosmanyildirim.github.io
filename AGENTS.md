# AGENTS.md

## Portfolio architecture
- Keep `index.html` as a thin shell. Homepage section copy lives in `components/*.html` and is loaded by `js/includes.js`.
- Homepage IDs such as `#work`, `#experience`, and `#about` must remain stable.
- Inner pages use the shared shell: `components/inner-header.html`, `components/inner-footer.html`, `css/site-shell.css`, and `js/site-shell.js`.
- Do not duplicate inner-page header/footer markup in individual pages.
- Copy must be concise, factual, and engineering-focused. Avoid slogans, generic marketing language, and unsupported claims.
- Preserve technical detail in thesis/stage content; simplify framing, not evidence.
- The thesis page opens as a short case study. Full report content remains inside the `#makale` disclosure.
- After any homepage or inner-page visual/content change, run `Portfolio visual capture` and inspect desktop/mobile fold + full-page screenshots.
- Visual capture must wait for modular includes/shared shell and retry while GitHub Pages is deploying.

## Kariyer.net iş araştırması — deney dalı
Bu dalda Kariyer.net iş arşivi/ilan analizi görevi geldiğinde **önce** `tools/kariyernet/OSMAN_JOB_PROFILE.md` ve `tools/kariyernet/README.md` dosyalarını oku. İlan toplama ve nihai değerlendirme farklı aşamalardır: GitHub Actions günlük ilan/URL verisini arşivler; kullanıcının isteği üzerine asistan **arşivdeki bütün kayıtları** değerlendirir.
- İlk 4–5 arama sonuç sayfasındaki her ilanı hedefle; anahtar kelimeleri doğrulanmış CV, coğrafya ve koşullardan üret. Kapsam yetersizse anahtar kelimeleri yeniden dene ve ne kadarının gerçekten okunabildiğini raporla. İstek/robots/sayfalama engelini aşmaya çalışma.
- 1/3/5/10 ilanlık keyfî kota koyma. Uygun olan **tüm** ilanları yeniden doğrulayıp 0–100 CV uyum puanı, gerekçe ve doğrudan bağlantıyla göster. İstanbul'u dışla; yeni mezun makine mühendisliğini önceliklendir.
- Önerilecek **her** işveren için ilan metni dışında bağımsız piyasa araştırması gerçekleştir: sektör, faaliyet, büyüklük (kanıt varsa), itibar ve risk göstergeleri. İşveren reklamını bağımsız teyit sayma. Kaynağın tarihi ve belirsizliği ayrı belirt.
- İlan keşfi ≠ açık başvuru. Doğrulanmayan veya kapanmış pozisyonları kesin açık diye önerme; raporda ayrı tut.
- Kullanıcının doğruladığı yeni tercih ve yetkinlikleri `OSMAN_JOB_PROFILE.md` üzerinde güncelle; kullanıcı bilgisi veya tamamlanmamış CI kanıtı uydurma. Portfolyo sayfalarını ve master dalını koru.

## Zorunlu ilan paneli ve şirket derin araştırması
- Kullanıcı ilanları istediğinde bütün uygun ilanları **tek, kompakt, filtrelenebilir karşılaştırma panelinde** göster: şirket, pozisyon, CV uyum puanı (0–100), şehir, deneyim şartı, açık başvuru doğrulama durumu, doğrudan ilan bağlantısı ve açılır şirket değerlendirmesi. Keyfî sonuç limiti uygulama; mobilde rahat taranabilir olmalı.
- Panelin satırı kısa olabilir ancak **şirket incelemesi kısa olamaz**: her önerilen işveren için açılır ayrıntıda çok kaynaklı, somut, tarihli araştırma yap. Sektör ve gerçek ürün/hizmetler; faaliyet yerleri ve tesisler; mülkiyet/kurumsal yapı; büyüklük (personel, üretim, ciro yalnız kanıt varsa); finansal/operasyonel süreklilik; bağımsız haber, resmî ticaret/kurum kayıtları; çalışan deneyimleri, ücret/mesai/İSG iddiaları; olumlu/olumsuz riskler, çelişkiler ve belirsizliği değerlendir. Doğrulanmayan ölçüyü veya güvenilirlik puanını uydurma.
- İşverenin kendi sayfası şirketin kendi beyanıdır; **bağımsız ikinci kaynaktan doğrula**. İşçi yorumları tekil/anekdotsal olabilir; suçlama ve şikâyetleri kanıtlanmış gerçek gibi sunma. Kaynak tarihi, güvenilirliği ve bulguyu açıkça ilişkilendir.
- Her şirket ayrıntısında kullanıcı açısından karar: **neden başvurulur, hangi risk/eksik teyit edilir, mülakatta ne sorulur?** Bu derin araştırmayı yalnız önerilen aday şirketlerde yap; ham arşivdeki her şirkette değil.
- Tam inceleme imkânı yoksa "araştırıldı" iddiasında bulunma; hangi şirketin hangi boyutunun doğrulanmadığını göster. Ayrıntılı araştırmayı gereksiz uzun liste metni olarak değil, panelin açılır şirket bölümünde tut.

## Şirket dosyasında zorunlu sektör/faaliyet açıklaması
- Kompakt ilan panelinde **Sektör** ayrı görünür sütun olsun; bilinmiyorsa açıkça "doğrulanamadı" yaz.
- Açılır şirket dosyasının **ilk iki bölümü**: (1) şirketin somut iş kolu, ürün/hizmetleri, müşterileri ve hizmet verdiği endüstriler; (2) üretim süreci/teknolojileri, makine parkı, tesisler ve makine mühendisinin işte fiilen ne yapacağı. Şirket adından veya ilan başlığından faaliyet uydurma.
- Ardından ölçek, mali/operasyonel durum, bağımsız itibar ve çalışan deneyimi, riskler, CV uyumu ve mülakat soruları gelsin. İşveren açıklamalarını bağımsız kaynaklarla karşılaştır; teyit edilemeyenleri ayrıca işaretle.

## Değerlendirilen ilanlar ve engellenen şirketler
- `tools/kariyernet/reviewed_listings.json`: yalnız ilan başına `provider + listing_id` kimliğiyle değerlendirilmiş kayıt. Kullanıcı 2026-10-19'da 18 Ekim 2026 arşivindeki 78 Kariyer.net ilanını incelendi saydı. Başka ilanları veya aynı şirketin yeni ilanlarını engelleme.
- Şirket yasağı küçük olduğu için mevcut `tools/kariyernet/OSMAN_JOB_PROFILE.md` içindeki `company_key` kayıtlarından okunur. Kesin işveren kaynak anahtarı kullan; genel ad parçası, benzer firma ismi veya serbest metin eşleştirmesiyle şirket engelleme. Belirsiz kimlik eşleşmelerini manuel teyide bırak.
- `tools/kariyernet/filter_candidates.py` günlük toplama **sonrasında** ayrı yeni-aday ve elenenler dosyası üretir. Ham keşif ve resmî kaynak arşivini değiştirme. Kullanıcıya önerirken `new_kariyernet_candidates.json` ile `new_official_candidates.json` kullan; adayları ayrıca gerçek başvuru koşulları açısından doğrula. `excluded_candidates.json` inceleme izi olarak kalır.
- Bundan sonra incelendi kararı alınan ilanların ID'si aynı JSON kaydına eklenmeli; dosya güncellemesinde mevcut SHA ve kapsam doğrulanmalı. Eski inceleme kayıtları silinmemeli.
