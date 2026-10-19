# İş Arama Profili — Osman Yıldırım

> Kanonik bağlam: Bu belge bu deney dalındaki ilan araştırma ve değerlendirme işlemlerinde okunur. Kaynak: bu çalışmadaki kullanıcı tercihleri ve repodaki `cv/index.html`. Özel iletişim bilgileri burada tutulmaz. Yeni kullanıcı kararı değişirse eski tercihin yerine güncel olanı işle.

## Birincil hedef ve konum
- Ana hedef: **makine mühendisi olarak istihdam**; yazılım, AI, Python ve otomasyon becerileri yalnız ayırt edici ek avantajdır. Tek başına yazılım pozisyonlarını makine mühendisliği ilanlarının önüne koyma.
- Öncelikli roller: makine mühendisi, üretim, imalat, kalite/kalite kontrol, mekanik tasarım, CAD, Ar-Ge/Ür-Ge, proses, mekanik bakım, üretim planlama, teknik proje ve uygun başlangıç seviyesi fabrika mühendisliği.
- Başlangıç seviyesi: yeni mezun, deneyimsiz, 0–2 yıl. 3+ yıl zorunluluğunu belirgin düşür; kıdemli/şef/yönetici pozisyonlarını yeni mezuna uygun diye sunma.
- Coğrafya: merkez Kahramanmaraş; ilk halka Kahramanmaraş, Gaziantep, Osmaniye, Adana, Kayseri, Malatya. İkinci halka Mersin ve Ankara. Adıyaman ve Hatay makul yakın alternatiflerdir; konum tercihini gerektiğinde kullanıcıya teyit ettir. **İstanbul hariç**; şehir belirsizse uygun konum varsayma.
- İngilizce CV'de A2–B1; ileri/akıcı İngilizce zorunluluğu puanı düşürür. Gereklilik tercih ise kesin diskalifiye etme.

## Doğrulanmış eğitim ve saha
- Kahramanmaraş Sütçü İmam Üniversitesi, Makine Mühendisliği lisans, 2022–2026.
- İÇTAŞ, Silifke/Mersin ME200 imalat stajı (2024): talaşlı imalat, kaynak, metal şekillendirme, soğuk dövme, diş açma/bükme, teknik resim ve sipariş takibi.
- İÇTAŞ, Silifke/Mersin ME322 organizasyon stajı (2026): Akkuyu NGS çelik konstrüksiyon üretim akışı, NDT ve kalite kontrol gözlemi, üretim takibi, İSG.
- Bitirme projesi: plastik enjeksiyon kalıbında geleneksel/helisel konformal soğutma kanallarının sayısal karşılaştırması; SolidWorks ve Autodesk Moldflow; ısı transferi ve mekanik tasarım.
- Araçlar: SolidWorks orta; AutoCAD, Zetacad, Onshape temel, Autodesk Moldflow; Python, MATLAB, Git/GitHub.
- Stajları tam zamanlı profesyonel deneyim diye sunma. Ölçülmemiş yetkinlik veya sertifika uydurma.

## Eşleştirme ilkeleri
1. Önce mühendislik rolü + şehir filtresi, sonra deneyim/mezuniyet/teknik beceri ve dil şartları. İşverenin sektörünün CV ile uyumuna ve iş tanımına bak.
2. 0–100 arası açıklanabilir CV uyum puanı ver. Puanın altına olumlu kanıt, eksik şart, belirsizlik, gerekli teyit ve lokasyon yaz. Sıralama sezgisel olduğundan uygunluğu garanti etmez.
3. Kariyer.net keşif URL'sini doğrulanmış/açık ilanla karıştırma. Doğrudan ilan veya resmî işveren kaynağında başvuru koşulları ve açıklığı teyit edilmediğinde statüyü **doğrulanamadı** tut.
4. Açık, uygun bulunan ilanların **tamamını** raporla; 3/5/10 gibi keyfî üst sınır koyma. Tekrarlanan ilanları birleştir. Her alan için puanı ve gerekçeyi göster.
5. Her önerilen işveren için dış kaynaklı bağımsız araştırma yap: faaliyet alanı, ölçek (kanıtlıysa), operasyonel konum, kurumsal güvenilirlik göstergeleri ve somut risk/şikâyet örüntüleri. İşverenin kendi reklam dilini bağımsız kanıt sayma; iddiaları kaynak ve tarihle ayır. Bilgi yoksa güvenilir/güvensiz hükmü verme.
6. Eski/kapanmış ilanı açıkmış gibi sunma; veri alınamıyorsa erişim engelini ve sonuç kapsamını dürüstçe belirt.

## İlgili dosyalar
- İş akışı: `.github/workflows/kariyernet-nightly.yml` (master'da zamanlayıcı), deneyde `.github/workflows/kariyernet-jobs.yml`
- Toplayıcılar: `tools/kariyernet/search.py`, `official_sources.py`, `regional_sources.py`.
- CV puanlayıcı: `tools/kariyernet/cv_rank.py`.
- Günlük tarihli arşiv: `data/kariyernet/daily/YYYY-MM-DD/` (deney dalı); bakılacak ilk dosyalar `discovered_urls.json`, `jobs.json`, `official_jobs.json`, `cv_ranked.json` ve raporları.
- Geliştirme görevi: Avenox Beyin `career-kariyernet-actions-harvester-20261017`. Her gerçek repo yazmasından önce mevcut revizyonu oku; görev durumunu kanıtla.

## Bakım
Kullanıcının doğruladığı yeni eğitim, beceri, hareketlilik, dil veya tercih kararlarını bu belgede güncelle. Önceki kayıtları silip deneyimi şişirme. Yalnız ilgili bilgileri yaz; kişisel kimlik/telefon/e-posta veya hassas veri saklama.

## Tercih edilen çıktı: tek panel + kapsamlı işveren dosyası
- Bütün uygun ilanları tek kompakt, filtrelenebilir/sıralanabilir panelde sun. Her satırda şirket, rol, şehir, deneyim, 0–100 CV uyum puanı, ilan durumu, doğrudan bağlantı ve **açılır kapsamlı şirket araştırması** olsun. Sayıyı keyfî azaltma. Görsel kontrol desteklenmiyorsa aynı alanları tek tabloda, araştırmaları şirket bazlı açılabilir bölümlerde sun.
- Şirket araştırması sırf "büyük firma", "kurumsal", "üretim tesisi var" gibi kısa notlar değil; bağımsız kaynaklı sektör/ürün, lokasyon ve operasyon, ortaklık/ölçek, finansal veya sipariş sürekliliği (varsa), işveren/çalışan deneyimi, İSG, ücret/mesai risk göstergeleri, itibar, son gelişmeler, belirsizlikler, kaynak tarihi ve **başvuru kararı** içermeli.
- Öneri olarak seçilen her işveren ayrı ayrı incelenir. Şirketin tanıtımını tek dayanak kabul etme; en az bir bağımsız ikinci kaynak ara. Bağımsız kaynak bulunamadığında "bağımsız doğrulama yetersiz" de. Olumsuz iddiaları otomatik doğru sayma; olumlu tanıtımı da sorgula.
- Panelde bir satıra sığdırmak için araştırmayı kısaltma; derin raporu açılır bölüme yerleştir. İlanın kendisini ve şirketi iki ayrı doğrulama konusu olarak ele al. 
