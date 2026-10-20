# Alt ajan brifi — kısa, bağımsız ve kanıtlanabilir

**Proje / kaynak:** [owner/repo veya mutlak çalışma yolu], [deney/mevcut dal], [gözlenen HEAD]. Başlamadan güncel HEAD'i ve AGENTS.md/README/karar/görev kayıtlarını doğrula.

**Tek hedef:** [Somut kullanıcı sonucu]. **Bağımlılık:** [Ajan A sözleşmesi / uygulanmadan önce gereken karar].

**Yalnız senin yazma sahipliğin:** [dosyalar]. **Salt okunur / dokunma:** [diğer ajanların dosyaları, core/save, main, kullanıcı verileri].

**Korunacak sözleşme:** [kimlik, API, şema, sabitler, sürümler ve ana kararlar].

**Kabul ölçütü:** [çalıştırılacak birim/regresyon/entegrasyon testleri, CI koşusu ve istenen artefact]. Test dosyasının varlığı çalıştırıldığı anlamına gelmez.

**Durma ve rapor:** [kaynak eksik, dal çakışması, CI engeli, plan uyuşmazlığı]. Sorunları gizleme, tamamlanmış işi tekrarlama, izinsiz yeni görev/dal açma.

**Teslim formatı:** branch + commit/HEAD + değişen dosyalar + gerçek test/run bağlantısı + başarılı/başarısız/doğrulanmamış + engel/sonraki adım. Aynı dalda kısa rapor yazmak için mevcut proje düzenini kullan; yeni kayıt dosyası yapısı için onay al.