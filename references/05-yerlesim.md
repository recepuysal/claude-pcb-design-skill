# 05 — Yerleşim (Placement)

> "Yerleşim, routing'in %80'idir." Yerleşim bitmeden tek yol çizme.

## 1. Sıra

1. **Kart çerçevesi** (Edge.Cuts / Board Outline) — ölçü ve köşe yarıçapı
2. **Mekanik sabitler:** montaj delikleri, konnektörler, buton, LED, ekran, anten bölgesi. Bunları kilitle (lock).
3. **Fonksiyon bloklarını kaba yerleştir** (blok diyagramdaki sırayla): güç girişi → koruma → regülatör → MCU → çevre birimleri → çıkışlar
4. **Kritik parçalar:** regülatör + kondansatörleri + indüktörü, kristal, dekuplaj, motor sürücü + bulk kondansatör + sense direnci
5. **Diğer pasifler**
6. Ratsnest çizgilerine bakarak **pin swap / blok döndürme** ile kesişmeleri azalt
7. Review → kullanıcıya yerleşim görüntüsünü göster → onay al → routing'e geç

## 2. Bölgeleme (Floorplan)

- Akış kart üzerinde de **soldan sağa** olsun: güç girişi bir kenarda, yüksek akım bölgesi o kenara yakın; hassas analog ve kristal bu bölgeden uzakta.
- **Gürültülü bölgeler** (SMPS, motor sürücü, röle) ile **hassas bölgeler** (ADC, kristal, sensör, anten) ayrı tarafta olur.
- Yüksek akım yolu kısa ve düz olur: konnektör → sigorta/TVS → sürücü → motor konnektörü. Bu yol kartı boydan boya dolaşmaz.
- Wi-Fi/BLE modülünün anteni **kart kenarına taşar ya da kenarda olur**. Altında **hiçbir katmanda bakır olmaz** (keepout). Anten önünde metal veya büyük parça bulunmaz.
- Isınan parçaların (LDO, MOSFET, sürücü) çevresinde bakır alan için yer bırakılır; ısıya duyarlı parçalar (NTC, kristal, elektrolitik) bunlardan uzakta tutulur.

## 3. Mesafe Kuralları (ölçülebilir)

| Parça | Kural |
|---|---|
| Dekuplaj 100 nF | IC güç pinine **≤2 mm**, IC ile aynı yüzde; akış yönü kaynak → kondansatör → pin |
| Bulk (4.7–22 µF) | IC'ye ≤5 mm |
| SMPS giriş kondansatörü | VIN ve GND pinlerine **≤1–2 mm**; sıcak döngü (hot loop) en küçük alan |
| SMPS indüktör | SW pinine bitişik; SW alanı minimum |
| Geri besleme bölücü | FB pinine yakın; çıkış kondansatörünün ucundan beslenir |
| Kristal + yük kondansatörleri | MCU OSC pinlerine **≤5 mm**; altında ve çevresinde başka sinyal yok |
| Pull-up/pull-down | Hedef pine yakın (I2C pull-up'ları master yakınında olabilir) |
| ESD/TVS | Korunan **konnektörün dibinde**; konnektör → TVS → (seri direnç) → IC sırası |
| Seri sonlandırma direnci (SPI SCK vb.) | **Kaynak** (sürücü) pine yakın |
| Sense direnci | Sürücünün sense pinine yakın; Kelvin bağlantı yapılır |
| Motor bulk kondansatörü | Sürücünün VM pinine ≤10 mm |
| Parçadan parçaya | Courtyard çakışması yok; elle lehim olacaksa ≥0.5 mm |
| Montaj deliği | Ø6.5–7 mm yasak bölge (M3) |

## 4. Yön ve Hizalama (profesyonel görünümün sırrı)

- Pasifler **sadece 0° / 90°** dönüklükte olur. Çapraz yerleşim yoktur (RF dışında).
- Aynı gruptaki parçalar **aynı yönde ve hizada** dizilir (ör. 8 pull-up direnci yan yana, eşit aralıklı).
- Kutuplu parçaların (diyot, LED, elektrolitik) **hepsi aynı yöne** bakar. Bu, montaj hatasını azaltır.
- IC'lerin pin 1 işaretleri mümkünse aynı köşeye bakar.
- Izgara: yerleşimde 0.5 mm veya 0.25 mm ızgara kullan. Konnektörleri 2.54 mm ızgaraya oturt.
- Simetrik bloklar (ör. 4 kanallı sürücü) birbirinin kopyası gibi yerleştirilir. KiCad'de "Multichannel / repeat layout", EasyEDA'da "Layout reuse" kullanılabilir.

## 5. JLC Dizgi ile İlgili

- Tüm SMD parçalar **Top** tarafta olmalı (tek yüz dizgi ucuzdur).
- THT parçalar ya JLC'ye dizdirilir (ek ücretli) ya da elle lehimlenir. Elle lehimlenecek THT parçaların çevresinde havya için 1.5–2 mm boşluk bırak.
- Uzun ve yüksek parçalar (elektrolitik, konnektör) küçük parçaları gölgelemesin. Reflow ve AOI için bu önemlidir.
- Kart kenarına 3 mm'den yakın parça varsa JLC panele kenar rayı (edge rail) ekler. Bunu bil ve kabul et.
- Fiducial: tek kart Economic PCBA'da zorunlu değildir. Panel ya da fine-pitch parça varsa 3 adet global fiducial koy (1 mm bakır, 2 mm maske açıklığı).

## 6. Yerleşim Kapısı

- [ ] Mekanik parçalar doğru ve kilitli; konnektör ağızları dışarı bakıyor
- [ ] Bloklar gruplu, akış mantıklı, gürültülü ve hassas bölgeler ayrık
- [ ] Mesafe tablosundaki kurallar sağlandı
- [ ] Pasifler 0/90°, gruplar hizalı, kutuplar aynı yönde
- [ ] Ratsnest'te gereksiz uzun ya da çapraz kesişen hatlar pin swap ile azaltıldı
- [ ] Anten keepout ve montaj deliği yasak bölgeleri temiz
- [ ] Yerleşim görüntüsü kullanıcıya gösterildi ve onay alındı
