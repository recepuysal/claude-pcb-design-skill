# 03 — Komponent Seçimi (JLCPCB / LCSC Odaklı)

## 1. Seçim Sırası

1. **Elektriksel uygunluk:** gerilim, akım ve güç değerlerinde **%50 pay** bırak (ör. 12 V hatta ≥25 V kondansatör, MOSFET Vds ≥ 1.5×Vmax).
2. **JLC stokta mı?** LCSC sayfasında stok >1000 olsun ve son tarihte stok eksilmesin.
3. **Basic mi, Extended mi?** Basic parçalar ek ücretsizdir. Extended parçaların her farklı çeşidi için yükleme ücreti alınır (yaklaşık $3/çeşit). Preferred Extended (Economic) kategorisinde ücret yoktur ya da düşüktür.
4. **Paket:** dizgi ve lehim kolaylığı, ısıl yeterlilik.
5. **Tedarik riski:** tek kaynak mı? Pin uyumlu alternatifi var mı? (Alternatifi BOM notuna yaz.)

## 2. Pasif Parça Kuralları

| Parça | Varsayılan | Not |
|---|---|---|
| Direnç | 0603 %1 (Basic: UNI-ROYAL 0603WAF...) | Güç: P = I²R. 0603 ≈ 0.1 W, 0805 ≈ 0.125 W, 1206 ≈ 0.25 W. %50 pay bırak. |
| MLCC | 0603 X7R/X5R | **DC bias:** 10 µF/6.3 V/0603, 5 V'ta kapasitesinin %50–70'ini kaybeder. Bulk kondansatörde gerilim değerini 2× seç ve paketi büyüt (0805/1206). |
| Y5V/Z5U | Kullanma | Sıcaklık ve gerilimle kapasite çöker. |
| C0G/NP0 | Kristal, filtre ve zamanlama için | ≤1 nF değerler için. |
| Elektrolitik | Motor/giriş bulk | ESR, ripple akımı ve ömür (105 °C) kontrol edilir. |
| Tantal | Kaçın | Kısa devre durumunda yanma riski. Gerekirse gerilim değeri ≥2× olmalı. |
| Ferrit boncuk | 0603, 600 Ω@100 MHz | Akım değeri yeterli olmalı. DC direnci düşük olmalı. |
| İndüktör (SMPS) | Ekranlı (shielded) | **Isat > Ipeak × 1.2**, Irms > Iout. |

### JLC Basic parça örnekleri (stoktan teyit et)
- 0603 dirençler: tüm E24 değerleri Basic (ör. 10k = C25804, 1k = C21190, 5.1k = C23186, 4.7k = C23162, 100R = C22775, 0R = C21189)
- 0603 MLCC: 100nF = C14663, 1µF = C15849, 10µF (0603 10V) = C19702, 22pF = C1653, 4.7µF = C19666
- 0805 10µF 25V: C15850 civarı. (Değer ve gerilim LCSC'de doğrulanmalı.)
- Diyot: 1N4148WS (C2128), SS34 (C8678), SMBJ/SMAJ TVS'ler
- MOSFET: AO3400A (C20917, N), AO3401A (C15127, P)
- LDO: AMS1117-3.3 (C6186) — Basic ama tavsiye edilmez (yüksek Iq ve dropout); ME6211C33 / XC6206 / AP2112K alternatifleri
- LED 0603: kırmızı C2286, yeşil C72043

> LCSC kodları değişebilir. Yazmadan önce **mutlaka** LCSC/JLC sitesinden ya da kullanıcının LCSC importer aracından doğrula. Doğrulanmamış kodu "(doğrula)" etiketiyle yaz.

## 3. Aktif Parça Seçimi — Kontrol Soruları

- Paket JLC'de dizilebilir mi? (BGA/QFN için ek ücret ve X-ray kontrolü olabilir. QFN normalde sorun değildir.)
- Exposed pad (EP) var mı? Varsa ısıl via ve GND bağlantısı gerekir.
- MSL seviyesi ve depolama koşulları (genelde dizgide sorun çıkmaz).
- Datasheet'te "Layout Example" var mı? Varsa onu birebir kopyala.
- Lifecycle: NRND/EOL ise kullanma.

## 4. Konnektörler

- Kart-kablo: JST XH (2.5 mm, el lehimine uygun, büyük akım ~3 A), JST PH (2.0 mm), JST SH (1.0 mm, Qwiic/STEMMA), XA (kullanıcının mevcut tesisatında kullanılıyor).
- Güç: vidalı klemens 5.08 mm (≥10 A için), DC jack.
- USB-C: güç için 6 pinli (yalnız VBUS/GND/CC) ya da 16 pinli USB 2.0 tip. **Mid-mount ve THT ayaklı** modeller mekanik olarak daha sağlamdır.
- Konnektörlerin **pin 1 yönü ve karşı kablo dizilimi doğrulanmadan** tasarım kapanmaz. Bu kullanıcıya "doğrulanmamış varsayım" olarak listelenir.
- THT konnektörler JLC'de dizilebilir (THT ek ücreti var) ya da elle lehim için bırakılır. Kullanıcıya sor.

## 5. BOM Taslağı Formatı

| Ref | Değer | Paket | LCSC | MPN | Basic/Ext | Adet | Not/Alternatif |
|---|---|---|---|---|---|---|---|

Hedef: Extended çeşit sayısını en aza indir. Aynı değeri tekrar kullan (ör. hem pull-up'larda hem LED'lerde 4k7 yerine 10k ve 1k ile yetin).
