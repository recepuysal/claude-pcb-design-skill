# 04 — JLCPCB Üretim Kuralları, Stackup ve Net Class'lar

Kaynak: https://jlcpcb.com/capabilities/pcb-capabilities (2026-11 itibarıyla okundu). Sınır değerler değişebilir, kritik bir durumda siteyi tekrar kontrol et.

## 1. JLC Kapasitesi (sınır) ve Bizim Varsayılanımız (rahat bölge)

| Parametre | JLC minimum (1–2 kat, 1 oz) | **Bizim varsayılan** | Not |
|---|---|---|---|
| İz genişliği / boşluk | 0.10 / 0.10 mm | **0.25 / 0.20 mm** sinyal | Yoğun bölgede (QFN fan-out) 0.15/0.15 serbest |
| 2 oz iz/boşluk | 0.16 / 0.16 mm | 0.30 / 0.30 mm | |
| Via delik / çap | 0.15 / 0.25 mm (pahalı) | **0.30 / 0.60 mm** sinyal, **0.40 / 0.80 mm** güç | Delik 0.2–0.25 mm ve çap <0.45 mm ise ek ücret alınır |
| PTH delik min | 0.15 mm | ≥0.3 mm | |
| PTH halka (annular ring) | 0.18 mm (2 kat, 1 oz), önerilen 0.25 | ≥0.25 mm | |
| NPTH min delik | 0.50 mm | ≥1.0 mm | |
| Via–via delik aralığı | 0.20 mm | ≥0.3 mm | |
| PTH delik–delik aralığı | 0.45 mm | ≥0.5 mm | |
| Pad–iz boşluğu | 0.10 mm | 0.20 mm | |
| PTH–iz | 0.28 mm (öneri 0.35) | 0.35 mm | |
| Farklı net SMD pad–pad | 0.15 mm | footprint'e bağlı | |
| Bakır–kart kenarı (freze) | 0.20 mm | **≥0.5 mm** (GND döküm için 0.5–1 mm) | |
| Bakır–V-cut kenar | 0.40 mm | ≥0.6 mm | |
| Serigrafi çizgi kalınlığı | 0.15 mm | **0.15 mm** | |
| Serigrafi yazı yüksekliği | 1.0 mm | **1.0 mm** (refdes), 1.5–2 mm başlık | Genişlik:yükseklik oranı ~1:6 |
| Pad–serigrafi | 0.15 mm | 0.15 mm | |
| Maske köprüsü (dam) | 0.10 mm (yeşil), 0.13 mm (siyah/beyaz) | Fine-pitch IC'de footprint'e bırak | |
| Kart kalınlığı | 0.4–2.0 mm | **1.6 mm** | |
| Min kart | 3×3 mm (castellated 10×10) | | |
| Castellated delik | ≥0.5 mm, kenara ≥1 mm | | |

Dielektrik sabiti (FR-4): 2 kat çekirdek εr ≈ 4.5; 7628 prepreg ≈ 4.4; 2116 ≈ 4.16; 3313 ≈ 4.1.

## 2. Stackup

### 2 katman (varsayılan)
- Top: sinyal + parçalar + kısa güç yolları
- Bottom: **mümkün olduğunca kesintisiz GND** + kaçınılmaz kısa geçişler + gerekirse güç dökümü
- 1.6 mm kalınlıkta katmanlar arası mesafe ~1.5 mm olduğu için kontrollü empedans **pratik değildir** (50 Ω için ~2.9 mm iz gerekir). Hızlı sinyalleri kısa tut. USB FS (12 Mbps) için sorun yoktur.
- Kontrollü empedans gerekiyorsa (USB HS, Ethernet, RF) **4 katmana geç** ya da 2 katmanda coplanar waveguide (CPWG) kullan ve JLC'nin empedans hesaplayıcısıyla hesapla.

### 4 katman (ihtiyaç olursa)
- Standart düzen: **SIG / GND / PWR(veya GND) / SIG**. JLC standart 4 katman stackup'ında (JLC04161H-7628, 1.6 mm) dış katman ile iç katman arası ≈0.2 mm'dir; tam değerleri sipariş ekranındaki stackup aracından al.
- İç katman bakırı varsayılan olarak 0.5 oz'dur.
- L2'deki GND katmanı **asla bölünmez**.

## 3. Net Class Tablosu (her projede doldur)

| Class | Netler | İz genişliği | Boşluk | Via |
|---|---|---|---|---|
| Default | sinyaller | 0.25 mm | 0.20 mm | 0.3/0.6 |
| Power_Low (≤0.5 A) | +3V3, +5V lojik | 0.40 mm | 0.20 mm | 0.3/0.6 |
| Power_1A | ≤1 A | 0.60 mm | 0.25 mm | 0.4/0.8 (×2) |
| Power_3A | ≤3 A | 1.5 mm ya da polygon | 0.30 mm | 0.4/0.8 (×4+) |
| HV (>50 V) | şebeke/yüksek gerilim | — | IPC-2221 tablosundan | |
| USB | USB_D+/D− | 0.30 mm (diff pair) | 0.15 mm çift içi | via yok |

İz genişlikleri IPC-2221'e göre ΔT=10 °C, 1 oz dış katman için hesaplanmıştır (yuvarlanmış ve pay eklenmiştir). `python scripts/pcb_calc.py trace --amps 2` ile hesapla.

| Akım (1 oz, dış, ΔT=10°C) | IPC-2221 minimum | **Kullan** |
|---|---|---|
| 0.5 A | 0.12 mm | 0.30 mm |
| 1 A | 0.30 mm | 0.50–0.60 mm |
| 2 A | 0.79 mm | 1.0–1.2 mm |
| 3 A | 1.37 mm | 1.5–2.0 mm ya da polygon |
| 5 A | 2.8 mm | polygon + 2 oz ya da iki katmanda paralel |

**Via akımı:** 0.3 mm delikli via (1 oz kaplama) için kabaca ~1 A hesapla. Güç geçişlerinde **her 1 A için en az 1 via, minimum 2 via** kullan.

**Gerilim aralığı (clearance):** ≤30 V için 0.2 mm yeterlidir. 30–100 V arası için ≥0.6 mm (IPC-2221 B4, kaplamasız dış katman), şebeke geriliminde ≥2.5 mm creepage + yarık (slot) kullanılır.

## 4. Mekanik Standartlar

- Köşe yarıçapı: 1–2 mm (keskin köşe kullanma).
- M3 montaj deliği: 3.2 mm NPTH ya da PTH (GND'ye bağlı). Etrafında **Ø6.5–7 mm** parça/iz yasak bölgesi (vida başı ve rondela için) bırak.
- M2.5 için 2.7 mm, M2 için 2.2 mm.
- Kart kenarından parça kenarına ≥1 mm. JLC panel rayları için bu mesafe ≥3 mm olmalıdır (V-cut veya PCBA panel).
- Konnektörler kart kenarına hizalanır. USB-C ağzı kenardan 0–0.5 mm taşabilir; kutu tasarımına göre karar ver.
- Ölçüleri yuvarla: 50×30 mm gibi; delikler 2.54 mm veya 0.5 mm ızgarada olsun.

## 5. JLC Sipariş Seçenekleri (varsayılan)

- Base material FR-4, 2 layer, 1.6 mm, HASL lead-free (fine-pitch/QFN varsa **ENIG** tercih et), yeşil maske, beyaz serigrafi.
- "Remove order number": KiCad/EasyEDA'da `JLCJLCJLCJLC` metniyle yer belirlenir ya da ücretli kaldırma seçilir.
- PCBA: Economic (tek yüz), "Confirm parts placement" **işaretli** (DFM önizlemesinde rotasyonu kontrol etmek için).
