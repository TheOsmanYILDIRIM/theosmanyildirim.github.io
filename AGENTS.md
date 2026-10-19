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
