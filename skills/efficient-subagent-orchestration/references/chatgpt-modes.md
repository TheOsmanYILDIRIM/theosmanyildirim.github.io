# ChatGPT'de ajan çalıştırma biçimleri — yetenek kapısı

Bu dosya runtime yetkisi vermez; her kullanımdan önce oturumun fiilî araçlarını kontrol et.

## A — Normal tek sohbet (varsayılan)

- Tek bir model oturumu, uygun araçları kullanarak ayrık işleri adım adım veya araç izin verdiğinde paralel çağrılarla yapabilir.
- Başka ChatGPT sohbetlerini açmak, onlarla gizlice mesajlaşmak veya onlarda otomatik iş çalıştırmak garanti değil. Gerçek alt ajan aracı yoksa "ajan çalıştı" deme.
- Kullanıcı ayrı A/B/C sohbetleri açmışsa her birine ayrı, kendi başına anlaşılır brif ver; bu sohbetlerin birbirlerinin bağlamını görmediğini varsay.
- Alt sohbetin raporunu sadece sohbet özetiyle değil, erişilebiliyorsa kendi branch/commit/CI/artefact kaydı üzerinden teyit et.

## B — Work, Codex veya yetkili bağlı araç

- ChatGPT Work çok adımlı dosya, web ve bağlı uygulama işleri yapabilir; bu, otomatik olarak ayrı ChatGPT alt ajanları doğuracağı anlamına gelmez.
- Codex ayrı ürün/ortamdır; varsa gerçek yetkili kod yürütücüsünü kullan. `codex exec` bilgisini sohbet terminaline erişildi sanma.
- Erişilen projedeki dosyaları ve etkin dalı her seferinde doğrula. Gizli bilgileri alt dallara, raporlara veya CI loglarına sızdırma.
- Saat bazlı yeniden denemeler/gelecek kontroller yalnız gerçekten kurulmuş izinli Scheduled Tasks/otomasyon ile yapılabilir; ChatGPT sohbetinde söz vermek bir otomasyon oluşturmaz.

## C — Kullanıcı koordinasyonlu ayrı sohbetler

1. Koordinatör önce paylaşılan kaynak HEAD ve sözleşmeleri sağlar.
2. Ajan A karar/şema sözleşmesini inceler ve doğrulanmış dal/commit/CI verir.
3. Ajan B/C ancak ilgili A çıktısını okuduktan sonra kendi kapsama sahip dallarında başlar.
4. Ajan D sonuçları inceleyen bağımsız reviewer olabilir; bağımsızlık gerçek kaynak/test erişimiyle desteklenmelidir.
5. Koordinatör tüm raporları *kendi mesajlarına bakarak değil* depo kaynaklarıyla karşılaştırır, uygun sırada entegre eder.

Bu yöntem otomatik paralel ajan işleyişi değil; kullanıcının açtığı ayrı ChatGPT oturumlarının ortak kalıcı kaynak üzerinden koordine edilmesidir.

## D — İş ve maliyet

- Araç/model planlarını veya limitleri her zaman güncel erişime göre değerlendir; video tarihindeki model/limit ve maliyet sayıları taşınamaz.
- Derin mimari/entegrasyon için daha kapsamlı düşünme; net, sınırlı mekanik işler için hızlı çalışma uygundur. Kullanıcı menüsünden seçilen modları sen değiştiriyor gibi davranma.
- Az sayıda bağımsız dal, doğru bağlam ve belirgin kabul testi çok sayıda ajan açmaktan genelde daha denetlenebilirdir. Bu bir ölçüm değil, bu becerinin tasarım varsayımıdır.

## Güncel resmî ürün başlıkları (2026-10-18 kontrolü)

- ChatGPT Skills: https://help.openai.com/en/articles/20001066-skills-in-chatgpt/
- ChatGPT Work: https://help.openai.com/en/articles/20001275-chatgpt-work-and-codex
- Cloud browser: https://help.openai.com/en/articles/20001280-using-cloud-browser-in-chatgpt
- Skill dosya yapısı: https://developers.openai.com/plugins/build/skills

Bunlar anlık ürün dokümanlarıdır; kurulu plan/izin bilgisi değildir. Skill yükleme şu an hesap ve çalışma alanına göre sınırlı olabilir.