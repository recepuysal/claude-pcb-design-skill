# 07 — Güç, Regülatörler, Li-ion Şarj ve Koruma

## 1. Güç Girişi ve Koruma Zinciri

Sıra: **Konnektör → Sigorta/PTC → Ters kutup koruması → TVS → (filtre) → Bulk C → Regülatör**

| Koruma | Çözüm | Not |
|---|---|---|
| Aşırı akım | PTC (ör. FSMD/1812/2920 serisi) ya da SMD sigorta | Hold akımı > normal akım × 1.25 |
| Ters kutup (düşük akım) | Seri Schottky (SS34) | Basit; ~0.4 V kayıp |
| Ters kutup (yüksek akım) | **P-MOSFET** high-side (Gate → GND, 10k + Zener gate koruması Vin > Vgs_max ise) | Kayıp ≈ I²·Rds(on) |
| Aşırı gerilim/ESD | TVS: SMBJ/SMAJ, Vrwm ≥ nominal giriş (12 V hat → SMBJ15A; 24 V → SMBJ28A/30A) | Konnektörün dibine |
| Inrush | NTC ya da yük anahtarı (load switch), soft-start | Büyük bulk C varsa |

## 2. USB-C Güç (Sink)

- **CC1 ve CC2 her biri ayrı 5.1 kΩ ile GND'ye** bağlanır (Rd). Tek direnci iki CC'ye ortak bağlamak **yanlıştır**; bu durumda e-marker'lı ya da C-C kablolarda güç gelmez.
- 5.1 kΩ ile maksimum 5 V elde edilir. 5 V dışında gerilim (9/12/20 V) gerekiyorsa PD tetikleyici (CH224K, IP2721, HUSB238) kullanılır.
- VBUS'ta TVS (5 V hat için SMF5.0A / SRV05-4 gibi) ve bulk kondansatör (≥10 µF; USB spesifikasyonu takılı anda en fazla 10 µF ister) bulunur.
- Veri hattı varsa D+/D− için ESD dizisi (USBLC6-2SC6) konnektörün dibine konur. USB 2.0'da A6/B6 ve A7/B7 pinleri birleştirilir.
- Konnektör kılıfı (shield): GND'ye doğrudan ya da 1 MΩ ∥ 4.7 nF ile bağlanır. Kararını not et.

## 3. LDO

- Kayıp: P = (Vin − Vout) × Iout. Junction sıcaklığı: Tj = Ta + P × θJA. SOT-23-5 için θJA ≈ 200–250 °C/W → **≤0.3 W**. SOT-223 için ≈60–100 °C/W.
- Dropout: Vin_min − Vout ≥ Vdropout(max @ Iout). Li-ion (3.0–4.2 V) → 3.3 V için **düşük dropout** LDO gerekir (ME6211, AP2112K, RT9013, TLV755). AMS1117 uygun değildir (~1.1 V dropout).
- Kararlılık: çıkış kondansatörünün tipini datasheet belirler. AMS1117 ESR ister (tantal veya 22 µF); modern CMOS LDO'lar seramikle çalışır (1 µF giriş / 1 µF çıkış minimum).
- Pil ile çalışan sistemde **Iq** önemlidir (ME6211 ~40 µA, XC6206 ~1 µA, AMS1117 ~5 mA).
- Layout: giriş ve çıkış kondansatörleri pinlere ≤2 mm uzaklıkta olmalı; GND pini ve tab büyük bakıra bağlanmalı.

## 4. Buck (Düşürücü) SMPS

Seçim: senkron buck (MP1584, TPS5430, LMR14xxx, SY8xxx, MP2315; JLC'de JW5026, TPS563201, MT2492). Datasheet'teki **layout örneğini birebir uygula.**

Hesaplar:
- İndüktör: L = (Vin − Vout) × D / (fsw × ΔIL), burada D = Vout/Vin ve ΔIL ≈ 0.3 × Iout
- Ipeak = Iout + ΔIL/2 → **Isat > 1.2 × Ipeak**
- Çıkış ripple: ΔV ≈ ΔIL / (8 × fsw × Cout) + ΔIL × ESR
- Geri besleme: Vout = Vref × (1 + Rtop/Rbot). Rbot 10k–100k aralığında; hesabı şematiğe not yaz.

Layout (kritik):
1. **Sıcak döngü (hot loop):** Cin → VIN pini → high-side FET → (low-side FET/diyot) → GND → Cin. Bu döngü **en küçük alanı** kaplamalı ve tamamen **üst katmanda** kalmalıdır. Cin (100 nF + 10 µF) VIN-GND pinlerinin dibinde durur.
2. **SW düğümü:** kısa ve küçük bir bakır alan (ısı için yeterli, EMI için küçük); altında ve yanında hassas hat bulunmaz.
3. **FB:** bölücü FB pinine yakın durur; üst direnç **çıkış kondansatörünün ucundan** beslenir. FB izi indüktörden ve SW'den uzak, ince ve kısa olur. Altında GND düzlemi bulunur.
4. Çıkış kondansatörünün GND'si ile Cin GND'si aynı bakır adada ve kısa yolla birleşir. Çoklu via ile alt GND'ye bağlanır.
5. Boot kondansatörü (BST–SW) pinlere yakın konur.
6. EP (exposed pad) ısıl via dizisi: 0.3 mm delik, 1–1.2 mm aralıkla 4–9 adet.

## 5. Boost (Yükseltici)

- MT3608, SX1308, TPS61023, FP6291 gibi. Sıcak döngü bu kez **çıkış tarafındadır:** SW → diyot/sync FET → Cout → GND → IC GND. Cout'u diyot ve IC GND'ye en yakın yere koy.
- Boost'un "kapatma"da bile giriş geriliminin (Vin − Vdiyot) çıkışa geçtiğini unutma. Tam kesme gerekiyorsa yük anahtarı ya da "true shutdown" özellikli IC kullan.
- Diyot: Schottky, If ≥ Iout × 2, Vr ≥ Vout × 1.5.

## 6. Li-ion / Li-Po Şarj

| IC | Akım | Not |
|---|---|---|
| TP4056 (+ DW01A/FS8205A koruma) | ≤1 A lineer | Iprog = 1200 / Rprog (1.2 kΩ → 1 A, 2 kΩ → ~580 mA). Lineer olduğu için ısınır: P = (Vin − Vbat) × I. 1 A'da ~1 W → EP ve geniş bakır gerekir. |
| MCP73831 | ≤500 mA | SOT-23-5, küçük projeler için |
| BQ24074 / BQ25601 / IP5306 | power-path / anahtarlamalı | Şarj olurken sistem beslenecekse **power-path** şarttır |

Kurallar:
- **NTC:** Pilde varsa bağla (TP4056 TEMP pini). Yoksa datasheet'e göre devre dışı bırak (TP4056: TEMP → GND).
- **Koruma:** Korumasız hücre kullanılıyorsa DW01A + FS8205A (ya da tek çip koruma) şarttır. Korumalı pakette ise kartta koruma isteğe bağlıdır.
- Şarj LED'leri: TP4056 ~CHRG/~STDBY açık-drain çıkışlardır. LED + direnç VIN'den beslenir.
- Pil konnektörü: polariteyi serigrafi ile + / − olarak işaretle. JST PH 2.0 kablolarında polarite üreticiye göre ters olabilir. Bunu **doğrulanmamış varsayım** olarak kullanıcıya bildir.
- Batarya ölçümü: bölücü (100k/100k) sürekli akım çeker. Yüksek değer (1M/1M + 100 nF ADC kondansatörü) ya da P-FET ile anahtarlanmış bölücü kullan; ya da yakıt göstergesi (MAX17048) tercih et.
- Kart üzerinde ısınan şarj IC'si ile pil arasında mesafe bırak.

## 7. Güç Yolu Seçimi (Power-ORing)

- USB ve pil arasında otomatik geçiş için: Schottky diyot (basit) ya da **P-FET ideal diyot** (USB varken pil P-FET'i kapanır; gate'i VBUS'a, 100k ile GND'ye bağlanır) kullanılır. P-FET body diyotunun yönüne dikkat et.
- Ayrıntılı tasarımda load-sharing (TP4056 + P-FET + Schottky) devresini şematiğe not olarak açıkla.

## 8. Güç Bloğu Kontrol Listesi

- [ ] Her regülatörün ısıl hesabı yapıldı (Tj < 100 °C, Ta = 40 °C)
- [ ] Giriş/çıkış kondansatörlerinin DC bias sonrası etkin değerleri yeterli
- [ ] Buck/boost layout'u datasheet örneğine göre yapıldı, sıcak döngü minimum
- [ ] FB bölücü değeri hesaplanıp şematiğe yazıldı
- [ ] Ters kutup, aşırı akım ve ESD/TVS koruması var
- [ ] USB-C'de CC dirençleri ayrı
- [ ] Şarj IC'sinin EP'si ısıl via ile GND'ye bağlı
- [ ] Her ray için test noktası ve (isteğe bağlı) LED göstergesi var
