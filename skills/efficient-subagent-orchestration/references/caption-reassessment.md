# Forn AI ve Avenox — bağımsız altyazı yeniden değerlendirmesi

**Amaç:** ChatGPT ile alt ajan koordinasyonu için uygulanabilir davranışları *önceki skill'in çıkarımlarına başvurmadan* yeniden kurmak. **Araştırma tarihi:** 2026-10-18. **Ham kaynak:** iki kanala ait GitHub Actions #39160443031 `youtube-subagent-research` artifact'ı (`manifest.json`, `selected.md`, altyazılar). Bağımsız başarılı koşu: #39160432433. Bu paket telifli tam transkriptleri yeniden yayımlamaz.

## Yöntem ve kapsam

1. Kaynak ZIP açıldı; CRC bütünlüğü kontrol edildi. 113 video keşfi, 81 altyazılı video, 291 metin dosyası içeriyor. Dosya sayısı video sayısı değildir: çoğu videoda dil ve otomatik çeviri varyantı birden fazla.
2. 81 videonun *orijinal Türkçe altyazı varyantı* varsa `tr-orig`, yoksa `tr` üzerinden metinsel terim taraması gerçekleştirildi. Tema taraması: delege/paralel iş, yazma sahipliği, bağlam, plan, test ve kanıt, skill tekrarlanabilirliği, yetkiler.
3. Önceki kolektörün `direct_description` bayrağı sadece başlık+açıklama eşleşmesidir. Gerçek konu kanıtı değildir. Başlığa bakıp kopyalamak yerine **odaklı video parça incelemesi** yapıldı. Kaynak değerlendirme bu yeniden okunan parçalara dayanır; 81 videonun tamamının dakikası dakikasına elle okunduğu iddia edilmez.
4. Doğal konuşma altyazısı yazım/dil hataları içerir (ör. “agent”, “ajan”, özel isimler). Cümleleri kurala dönüştürürken lafzi alıntı değil, anlamı ve bağlamı özetlendi. Video açıklamasına yazılan reklam/boilerplate doğrudan kanıt sayılmadı.
5. Aşağıdaki her kaynak için ayrım: **G** = içerikte gösterilen veya tartışılan gözlem (creator demonstration); **Ö** = yaratıcı görüşü/önerisi; **T** = bu becerinin ChatGPT ortamına uyarlanmış kendi tasarım kararı. G/Ö bağımsız ürün performans testi değildir.

## Birincil ve yüksek değerli kaynaklar

| Video ve kanal | Altyazıda bulunan asıl katkı | Kanıt düzeyi | ChatGPT'ye aktarım |
|---|---|---|---|
| [Forn — Ajanlarım Benden Çok Çalışıyor](https://www.youtube.com/watch?v=3RcSsjTgnhI) | Başta bağlam/örnekler, ardından bağımlılık planı, planın sorgulanması, dışarıdan doğrulanabilir durma koşulu; loop ve hedef ayrımı | Ö/G | Hedef/kabul ölçütü önceden; durağan planı kör izleme; hayali arka plan çalışması yapma |
| [Forn — Tek Prompt vs 20 Ajan](https://www.youtube.com/watch?v=4bg9_FdyXwI) | Kapsamlı çok-ajanlı video editöründe süre/mimari büyüyor; çok sayıda özellik çalışmazken tek prompt prototipinde çalışan parçalar bulunuyor | G | Çok ajan sayısını kalite sayacı sayma; küçük çalışan dikey kesit ve gerçek kullanıcı testi iste |
| [Forn — Bir Ay Boyunca Yapay Zekâyla Çalışınca Ne Öğrendim?](https://www.youtube.com/watch?v=X1S8fi-mwTw) | İstenilen davranış ile mevcut bağlam farkı; eksik referansları sağlama, hatalardan öğrenme, başarısız sürecin yeniden tasarımı | Ö/G | Başarısızlıkta yeni promptu uzatmak yerine eksik kanıt/tasarım varsayımını kontrol et |
| [Forn — Fable ve Claude Ajanlarını Projemde Çalıştırdım](https://www.youtube.com/watch?v=xw0_UZo8-3I) | Kendi yerine planlayan koordinatör, çalışan referansların incelenmesi ve oyun prototipinde kademeli uygulama | G | Üst kararlar ve çalışan kaynak örneği; kopya üretmek değil, davranış testi |
| [Forn — Yapay Zekâya Hafıza Nasıl Takılır?](https://www.youtube.com/watch?v=7YUSYyXOoOY) | Sohbet arası süreklilik için harici kaynak, görev durumu ve yapılan işin kanıtı/makbuzu | Ö | Önce mevcut kalıcı proje kayıtlarını kullan; yeni/mükerrer hafıza mimarisi açma |
| [Forn — Context'i Bir de Benden Dinleyin](https://www.youtube.com/watch?v=h9AfHc_UFLo) | Önceden kurulan söylemin sonraki yanıtı yanlılığa itebildiğine dair eğitici sohbet denemesi | G/Ö | Eski hatalı ajan raporlarını otorite sanma; yeni kanıt ile sıfırdan değerlendir |
| [Forn — Yapay Zekâyı Oyunum İçin İşe Aldım](https://www.youtube.com/watch?v=nqRLMhKSKME) | Kaynak tarama, oyun için ön karar/araştırma, ajanla yapılan işin gözle denetlenmesi | G | Dünya/oyun alt ajanlarında sözleşme ve görsel kabulü de istemeyi değerlendir |
| [Avenox — Kendi Yapay Zekâ Ekibimi Kurdum](https://www.youtube.com/watch?v=MFqtKpzttGA) | Üst ajanın görev ayrıştırıp delege etmesi, alt ajanların kısa rapor dönmesi, yazma sınırları ve worktree | G/Ö | Koordinatör sentez ve entegrasyon; dosya sahipliği; rapor değil repo kaynakları doğrulansın |
| [Avenox — 20 Agent Aynı Projede Nasıl Birbirine Girmiyor?](https://www.youtube.com/watch?v=z8r237sMmmQ) | Aynı görevin çift sahiplenilmesi, çift deploy, ortak dosyada çatışma ve yanlış kaynak bağlamı; görev/izin/scope katmanlarının gerekliliği | G/Ö | Kim hangi dalın/dosyanın yazarı? Tek yazıcı, kararlı sözleşme ve çakışma kapısı |
| [Avenox — Context'i Kendim Doldurmuyorum](https://www.youtube.com/watch?v=4vWlWHDol-g) | Ana ajan yerine inceleme yapan alt ajanların odaklı rapor getirmesi, mevcut backlog ve proje raporlarının okunması | G | Bağımsız salt okunur araştırma şeritleri; kaynağa dayalı kısa bulgu; repo durumunu geri oku |
| [Avenox — Fable 5 Planlıyor, Codex Yapıyor](https://www.youtube.com/watch?v=0tMyfqhuB2M) | Mimari yargı ve uygulamanın ayrılması; model limitlerinin işin ağırlığıyla dengelenmesi; uzun tutturulan sürenin aşırı optimizasyona dönüşmesi | Ö/G | Zor karar ve mekanik uygulamayı ayır ama marka/model ve süre garantisi gömme |
| [Avenox — GPT Astra’yı Böyle Kullanıyorum: Kendi Skill’ini Oluştur](https://www.youtube.com/watch?v=PUtaB4uYvvA) | Tekrarlanan yöntemi skill'e çevirme; ne zaman, hangi kaynaklar, nasıl yapılır, ne olunca biter; SKILL+references+scripts | G/Ö | Açık tetikleyici + kısa süreç + ihtiyaca göre başvuru dosyaları; gereksiz dev prompttan kaçın |
| [Avenox — Yapay Zekayı Böyle Çalıştırıyorum](https://www.youtube.com/watch?v=2n84xa99FRY) | Benzer işleri birkaç kez yaptıktan sonra tekrarlanabilir skill edinme; odağı boğmadan bağlam toplama; gerçek testlerin önemi | Ö/G | Her tek seferlik çözümü skill yapma; işe yarayan davranışı tekrar kullanılabilir hale getir |
| [Avenox — Anthropic ve OpenAI Uyardı, Skill'lerimi Baştan Yazıyorum](https://www.youtube.com/watch?v=5LLLxHxkCnI) | Aynı görevin aşırı sıkı talimatlı ve gevşek brifli varyantlarına ait karşılaştırmalı örnekler; aşırı uzun yönergelerin kaliteyi kısıtlayabildiği iddiası | G/Ö | Yalnız koruma/kabul alanlarını katı tut; çözüme giden yaratıcı yolu ayrıntısıyla zorunlu kılma |
| [Avenox — 1.900 Promptumdan Çıkan Tek Ders](https://www.youtube.com/watch?v=AmODkS6GzlY) | Prompt uzunluğundan çok hedef, veri, bağlam ve sınırların açıklığı; farklı model/harness deneyimleri | Ö/G | Kısa, tam ve kanıtlı brief. Modele insan benzeri rol ataması gereksiz |
| [Avenox — Promptu Uzatmayı Bıraktım](https://www.youtube.com/watch?v=1hHOgnmAHlE) | Az ama alakalı gerçek kanıt ile odaklı ajan araştırması; bağlam seçiminin önemi | Ö/G | Dosyaların tümünü zorla yığmak yerine ilgili kesin kaynakları ve taze değişiklikleri ver |
| [Avenox — Sorun Promptunda Değil, Modelin Göremediği Şeyde](https://www.youtube.com/watch?v=i_KHwrmn3JA) | Doğru/yanlış görsel referansların aynı modele farklı sonuç verdirdiği örnekler; alakasız bağlamın maliyeti | G | Yanlış veya eskimiş rapor/asset vermek yokluğundan daha kötü olabilir; kaynak tarihi/kalite kontrolü |
| [Avenox — Yapay Zekaya Kod Yazdırdım, Bir Tanesini Hata Aramaya Koydum](https://www.youtube.com/watch?v=TREm_35AtB4) | Ayrı kod ve gözden geçirme rolleri, ortak rapor endeksi ve gerçek hata karşısında testin yetersizliği | G | Bağımsız incelemeci; testin varlığı ve yeşil oluşunu canlı davranış kanıtıyla tamamla |
| [Avenox — Yapay Zekayı Gece Bırakıyorum](https://www.youtube.com/watch?v=MHk8390TDjw) | Tekrarlanan loop'un önceki düzeltmeleri unutunca aynı hatayı defalarca çözmesi; turdan tura taşınan görev durumu | G/Ö | Sadece gerçekten kurulu otomasyonlarda devam; kalıcı checkpoint, tekillik, tekrar koruması |
| [Avenox — 3 Yıldır Yapay Zeka Kullanıyorum](https://www.youtube.com/watch?v=9C386jpjnlo) | Ayrı araştırma raporları arasında uyuşmazlıkların sentezleyiciye gösterilmesi, gerçek görevlerden test seti kurulması | Ö | Çoklu ajanın ortak söylediği doğru kabul edilmez; çelişkiyi kaynakla yeniden aç |
| [Avenox — Yapay Zeka Projeme Sıfırdan Böyle Başlıyorum](https://www.youtube.com/watch?v=8G4IN7q4tao) | Kod atölyesi ve ikinci beyin alanlarını ayırma; araştırma raporlarının ileride yeniden kullanılabilmesi; önce davranış testi | G/Ö | Repo kodu ile kalıcı hafızanın görevlerini ayır, yeni kayıt düzenini izinsiz ekleme |
| [Avenox — Claude ile Oyun Yapmaya Değil, Oyun Fabrikası Kurmaya Başladım](https://www.youtube.com/watch?v=J7l5txZ3l9s) | İlişkili oyun alt sistemleri/raporları, fazlı teslim, en başta test/depo kuralları | G | Oyun alt ajanlarının çıktısını kural/sözleşmeye bağla; görsel ve kod testlerini ayrı değerlendir |
| [Avenox — 5.800 Promptumu Claude'a Verdim](https://www.youtube.com/watch?v=W6H8h0UL1tM) | Prompt/araç/bağlam sınırları, yeni kanıta göre planı gerekçeyle güncelleme, kaynak verinin eski olabilmesi | Ö | Plan değişikliğinin sebebini kaydet, sözleşme kırılacaksa dur/teyit iste |
| [Avenox — Fable ve Astra’yı Aynı Projede Birlikte Çalıştırdım](https://www.youtube.com/watch?v=884c8bDYyBM) | Farklı uygulayıcılar, ayrı PR ve kaynak raporları, maliyet/limit yönetimi | G | Heterojen araçları kullanmak şart değil; gerçek izin, maliyet ve CI belirleyici |
| [Avenox — Bu Yapay Zeka 130 Gündür Hafızasını Yazıyor](https://www.youtube.com/watch?v=sRCTOxc4658) | Kalıcı hafıza olayları, günlük/öğrenme, veri uydurma riskini adım adım test etme | Ö/G | Mevcut Beyin/Drive/repo tek kaynaktır; not/makbuz işleminde doğrulama esastır |

## Önceki versiyondan bağımsız yeniden çıkan sonuçlar

**D1 — Ön hazırlık gerekli, fakat sonsuz araştırma değil.** Hem Forn hem Avenox hedefli bağlam ve kaynağa dayalı planı vurguluyor. Yeni skill, küçük işte tam keşfi zorunlu kılmıyor; belirsizlik/riske göre kapsamı genişletiyor. **[T]**

**D2 — Ana ajan koordinatör, mutlak “hiç iş yapmaz” değil.** Avenox yüksek paralellikte üst ajanın kararlarını korumayı gösteriyor. Ama Forn'un çok ajanlı editör denemesi aşırı tasarımın yanlış yöne gidebildiğini gösteriyor. ChatGPT'de tek küçük görevi tek oturumda yapmak varsayılan. **[T]**

**D3 — “Çok ajan = daha iyi” kanıtlanmadı.** Video anlatımı ürünün tüm testlerini, dış bağımsız ölçümü veya tekrarlı istatistiksel deneyi sunmuyor. Çok sayıda ajan, başarısız ürün özelliklerini düzeltmiyor. **[G/T]**

**D4 — Sahiplik sınırı operasyonel, dilsel değil.** “Şu dosyaya dokunma” iyi bir talimat olsa da teknik izin/kısıt yerine geçmez. GitHub dalı, ayrı worktree, gerçek diff ve ref değişimi ayrıca doğrulanmalı. **[T]**

**D5 — Birim testi geçmek kullanıcı sonucunu doğrulamaz.** Testler gerçekten çağrılmalı, gerekirse ekran kaydı/screenshot ve gerçek cihaz farklı kapılardır. **[G/T]**

**D6 — Kalıcı durum proje biçimine göre.** Görülen her konuşma sonrası yeni backlog veya rapor dosyası açılmaz. Var olan resmî dosyayı ve görev protokolünü kullan, ara teslimi bağımsız doğrula. **[T]**

**D7 — Kısa ama kaynaklı skill.** Videolardan uzun model reklamı ve belirli sürüme özgü eylem komutları aktarılmadı. Dört alanı olan kısa brief bile karar/koruma/kanıt içermeli. **[T]**

**D8 — ChatGPT kabiliyeti videolardaki CLI kabiliyeti değildir.** Claude Code/Codex `Agent` araçlarını ChatGPT standart sohbetine aktararak “arka planda paralel ajanları çalıştırdım” demek yanlış. Etkin özellikleri kontrol et ve gerekiyorsa kullanıcı için *ayrı sohbet brifleri* sun. **[T]**

## Dışarıda bırakılan iddialar ve gerekçeleri

- Güncel model sıralaması, fiyat/limit katsayıları ve belirli ürün sürümleri: zamanla değişiyor, kullanıcının hesabına göre farklı olabilir.
- 20/200/2000 ajan, %x token tasarrufu veya “tüm işler bir gecede biter” sayıları: kişisel örnekler; genellenebilir ölçüm yok.
- Video içindeki “her zaman şu modeli şef yap, şu modeli amele yap” tarzı kesin kurallar: iş/ücret/erişim bağlamından koparılmamalı.
- Uzun prompt kötüdür/geniş prompt iyidir türünden kategorik iddialar: bağlam ve görev ayrımına bağlı; sabit sözleşme ve gerçek test gerektiğinde ayrıntılı brief zorunlu olabilir.
- Yetkisiz otomasyon, cookie veya secret aktarımı ve gerçek dışı CI/cihaz sonucu: araştırma kaynağından böyle bir yetki doğmaz.

## Doğrulama sınırı

Burada **video altyazısındaki anlatım** ve içerikte tarif edilen demolar analiz edilmiştir; videoların kareleri/sunulan UI tarafımızdan bu yeniden değerlendirmede görsel olarak incelenmedi. Otomatik transkript hataları ve içerik üreticilerinin öznel görüşleri mümkündür. Konuya özel öneriler, kaynak metnin bilimsel doğrulanması veya kullanıcının hesabında aynı özelliğin bulunduğu iddiası değildir.