# 12 — Kontrol Listeleri (Review Checklists)

Her kapıda ilgili listeyi uygula. Sonucu kullanıcıya şu formatta raporla:
`✅ geçti / ⚠️ kabul edilen istisna (gerekçesi) / ❌ düzeltilecek`.
Bulguları önem sırasına göre ver: **Kritik** (kart çalışmaz/yanar) → **Önemli** (güvenilirlik, EMI, üretim) → **Kozmetik**.

## A. Şematik Review

**Elektriksel**
- [ ] ERC 0 hata; uyarılar açıklandı
- [ ] Her IC'nin tüm güç ve GND pinleri (EP dahil) bağlı
- [ ] Her VDD pininde dekuplaj var; bulk kondansatörler var
- [ ] Açık-drain hatlarda pull-up var (I2C, INT, RESET, FAULT, CHRG)
- [ ] Reset, boot ve strap pinleri tanımlı
- [ ] Gerilim seviyeleri uyumlu; 5 V → 3V3 girişler korumalı
- [ ] Polarite ve pinout doğrulandı (SOT-23 FET/BJT, LDO pin sırası, diyot yönü)
- [ ] Kondansatör gerilim değerleri ≥1.5–2× (DC bias dikkate alındı)
- [ ] Direnç güçleri hesaplandı (sense, LED, bölücü)
- [ ] Regülatör FB/prog dirençleri hesaplandı ve not edildi
- [ ] Koruma: sigorta/PTC, ters kutup, TVS, ESD
- [ ] İndüktif yüklerde flyback diyotu
- [ ] Kullanılmayan pinlerde NC işareti; kullanılmayan op-amp/kapı birimleri sonlandırıldı
- [ ] Programlama/debug portu ve test noktaları var

**Okunabilirlik / stil**
- [ ] Kutu kutu blok düzeni; kutular hizalı ve başlıklı (`00-kullanici-stili.md`)
- [ ] Sinyal soldan sağa, güç yukarıdan aşağıya akıyor; GND sembolleri aşağı bakıyor
- [ ] Blok içi bağlantılar tel ile; label çorbası yok
- [ ] 4 yollu kavşak yok, tel sembol üstünden geçmiyor, ızgara dışı uç yok
- [ ] Net adları anlamlı ve tutarlı; değer yazımı tutarlı (`4k7`, `100n`)
- [ ] Refdes'ler annotate edilmiş ve sıralı
- [ ] Hesap ve layout notları ilgili yerlerde
- [ ] Başlık bloğunda revizyon ve tarih var

**BOM / Üretim**
- [ ] Her parçada footprint + LCSC kodu var
- [ ] Extended parça sayısı en aza indirildi; stok kontrolü yapıldı
- [ ] DNP parçalar işaretli; montaj deliği/fiducial BOM dışı

## B. Yerleşim Review

- [ ] Kart ölçüsü, delikler ve konnektör konumları mekaniğe uygun
- [ ] Fonksiyon blokları gruplu; akış mantıklı
- [ ] Gürültülü (SMPS/motor) ve hassas (analog/kristal/anten) bölgeler ayrık
- [ ] Dekuplaj ≤2 mm, SMPS sıcak döngü minimum, kristal ≤5 mm
- [ ] ESD konnektör dibinde
- [ ] Pasifler 0/90°, gruplar hizalı, kutup işaretleri aynı yönde
- [ ] Anten keepout, montaj deliği yasak bölgesi temiz
- [ ] Tüm SMD parçalar Top tarafta (tek yüz dizgi)
- [ ] Elle lehim/THT erişimi var; uzun parçalar gölge yapmıyor
- [ ] Isınan parçalar için bakır alan ayrıldı

## C. Routing Review

- [ ] DRC 0 hata; unrouted 0
- [ ] Güç izleri net class genişliğinde; via sayısı akıma yeterli
- [ ] Alt GND düzlemi bütün; uzun yarık ya da ada yok; dikiş via'ları var
- [ ] Hızlı sinyallerin altında kesintisiz referans düzlemi var
- [ ] USB diferansiyel çift kurallarına uyuldu
- [ ] Kristal kurallarına uyuldu
- [ ] FB/sense hatları Kelvin ve gürültüden uzak
- [ ] Dar açı, stub, çift iz, boşta via yok
- [ ] Köşeler smooth (arc), yarıçaplar tutarlı; teardrop eklendi (`00-kullanici-stili.md`)
- [ ] Pad girişleri düz ve merkezden
- [ ] Bakır–kenar mesafesi ≥0.5 mm
- [ ] Döküm yeniden dolduruldu

## D. Serigrafi ve Çıktı Review

- [ ] `11-silkscreen-dokuman.md` kontrol listesi geçti
- [ ] 3D görünüm kontrol edildi (çakışma, yükseklik, konnektör yönü)
- [ ] Gerber önizlemesi (JLC'nin görüntüleyicisi ya da KiCad Gerber Viewer) kontrol edildi: katmanlar, delikler, kenar
- [ ] CPL rotasyonları JLC önizlemesinde kontrol edilecek (kullanıcıya hatırlatılır)
- [ ] BOM ve CPL refdes'leri birebir eşleşiyor

## E. "Doğrulanmamış Varsayımlar" Listesi (her teslimde)

Teslimin sonunda kullanıcıya **mutlaka** ayrı bir başlık altında ver:
- Konnektör pin 1 yönü / karşı kablo dizilimi
- Ölçülmesi gereken mekanik mesafeler (ör. header aralığı, modül delikleri)
- Doğrulanmamış LCSC kodları ve stok
- Datasheet'te bulunamayan ve tahmin edilen değerler
- Pilin JST polaritesi
