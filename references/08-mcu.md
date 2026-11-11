# 08 — Mikrodenetleyici Devreleri (MCU)

Her MCU için "Hardware Design Guidelines" / "Getting started with hardware" uygulama notunu oku:
- STM32: **AN2586** (F1), AN4488 (F4), AN4325 (F0/G0) — "Getting started with STM32 hardware development"
- ESP32-S3: **Espressif ESP32-S3 Hardware Design Guidelines**
- RP2040: "Hardware design with RP2040"

## 1. Ortak Kurallar

- **Her VDD pinine 100 nF** (0603/0402, pine ≤2 mm), ayrıca rayda 1 adet 4.7–10 µF bulk kondansatör.
- **Analog besleme (VDDA/AVDD):** ferrit boncuk (ya da 10 Ω) + 1 µF + 10–100 nF. VSSA aynı GND'ye bağlanır.
- **Reset:** pull-up (genelde dahili) + 100 nF GND'ye. Reset butonu varsa butona seri 100–470 Ω (isteğe bağlı) bağlanır.
- **Boot/strap pinleri:** belirli seviyede olmalı; pull direnci + buton ya da jumper kullanılır.
- **Programlama portu her zaman bulunur:** SWD (STM32), UART + boot (ESP32), USB.
- Kullanılmayan GPIO'lar yazılımla çıkışa/pull-up'a alınır. Donanımda yedek pinleri test noktasına çıkar.
- 5 V'luk dış dünyaya bağlanan pinler: STM32'de "FT" (5 V tolerant) pinleri seç; ESP32 5 V tolerant **değildir** (seviye dönüştürücü ya da bölücü gerekir).
- Harici dünyaya giden her GPIO'ya 100–330 Ω seri direnç konur (kısa devre ve ESD'ye karşı ucuz koruma), konnektörde TVS/ESD diyotu bulunur.

## 2. STM32 (ör. STM32F103C8T6 / G0 / G4)

| Pin/blok | Bağlantı |
|---|---|
| VDD × n | Her birine 100 nF + rayda 4.7 µF |
| VDDA | Ferrit + 1 µF + 10 nF (F1'de VDDA = VDD olmalı) |
| VBAT | Pil yoksa VDD'ye bağla (100 nF ile) |
| NRST | 100 nF GND'ye (dahili pull-up var), SWD konnektörüne |
| BOOT0 | **10k GND'ye** (F1). G0/G4'te BOOT0 option byte ile ayarlanabilir; yine de pull-down koy |
| BOOT1 (PB2, F1) | 10k GND'ye |
| HSE | 8 MHz kristal + iki C0G yük kondansatörü (hesap: §5) |
| LSE (32.768 kHz) | RTC gerekiyorsa; çok düşük güçlü osilatördür, yük kondansatörlerini ve layout'u titiz yap |
| USB (F1: PA11/PA12) | F1'de D+ hattına 1.5 kΩ pull-up gerekir (dahili yoktur). G0/G4/F0 serilerinde dahilidir |
| SWD | SWDIO (PA13), SWCLK (PA14), NRST, 3V3, GND. **2×5 1.27 mm Cortex Debug** ya da 1×5 2.54 mm header |

Notlar:
- Blue Pill klonlarındaki hataları kopyalama (USB D+ pull-up'ının 10k olması gibi).
- PA13/PA14'ü GPIO olarak kullanma (SWD'yi kaybedersin).
- Kristalsiz çalışmak (HSI) USB dışındaki projelerde kabul edilebilir. USB için HSE gerekir (G0/G4'te HSI48 + CRS ile kristalsiz de olabilir).

## 3. ESP32-S3 (modül: WROOM-1 / MINI-1)

| Pin/blok | Bağlantı |
|---|---|
| 3V3 | Kaynak **≥500 mA** (Wi-Fi tepe akımı ~350 mA+). Modülün yanında 10 µF + 100 nF, girişte 22 µF |
| EN (CHIP_PU) | **10 kΩ pull-up + 1 µF** GND'ye (RC gecikmesi; güç oturmadan çip açılmasın). Reset butonu EN–GND arasına |
| GPIO0 | Boot butonu GND'ye (dahili pull-up var; 10k harici isteğe bağlı) |
| Strapping | GPIO0, GPIO3, GPIO45, GPIO46. Açılışta seviyeleri etkilenmemeli (GPIO46'yı çıkış yükü ile yukarı çekme) |
| USB | GPIO19 (D−), GPIO20 (D+), dahili USB-Serial/JTAG. Seri direnç gerekmez; isteğe bağlı 22 Ω. ESD konnektörde |
| UART0 | TX0 GPIO43, RX0 GPIO44: programlama/log için header'a çıkar |
| Kullanma | Flash/PSRAM pinleri: GPIO26–32. **Octal PSRAM'lı (R8) modüllerde GPIO33–37 de kullanılamaz** |
| ADC | ADC2 Wi-Fi açıkken kullanılamaz; ADC1 (GPIO1–10) tercih edilir |

Anten:
- Modülün anten kısmı **kart kenarından dışarı taşar** ya da tam kenardadır. Anten altında tüm katmanlarda **bakır yoktur** (keepout). Datasheet'teki önerilen yerleşim bölgesine uy (antenin her iki yanında ≥15 mm boşluk idealdir).
- Anten yakınında metal parça, vida, konnektör ya da pil bulunmaz.

Otomatik programlama (USB-UART kullanılıyorsa): CH340/CP2102 + iki NPN (S8050) ya da çift transistör ile DTR/RTS → EN/GPIO0 devresi kurulur. Doğrudan USB-Serial/JTAG kullanılırsa bu devreye gerek yoktur.

## 4. RP2040 (özet)

- 1.1 V dahili regülatör: VREG_VOUT → DVDD, 1 µF. Her IOVDD'ye 100 nF.
- Harici QSPI flash (W25Q16JV), flash CS hattında BOOTSEL butonu (1k seri) bulunur.
- 12 MHz kristal + 1 kΩ seri direnç (XOUT) — Raspberry Pi'nin referans tasarımına uy.
- USB: 27 Ω seri dirençler D+/D− hattına konur.

## 5. Kristal (Crystal) Tasarımı

- Yük kondansatörü: **C1 = C2 = 2 × (CL − Cstray)**. Cstray ≈ 3–5 pF. Örnek: CL = 10 pF → 2 × (10 − 4) = 12 pF. (`pcb_calc.py xtal --cl 10`)
- C0G/NP0 kondansatör kullan.
- Layout:
  - Kristal MCU pinlerine ≤5 mm; izler kısa, simetrik ve **via'sız**.
  - Yük kondansatörlerinin GND'si kısa yoldan, tek noktadan GND'ye iner.
  - Kristal bölgesinin altı solid GND olmalı ve **başka sinyal geçmemeli** (hiçbir katmanda).
  - Çevresine GND guard (via'larla dikili döküm) yapılabilir.
- Kristal yerine osilatör/MEMS, sıcaklık ve titreşim zor koşullarda daha güvenlidir.

## 6. Programlama Header Standardı

| Arayüz | Konnektör | Pin sırası |
|---|---|---|
| SWD (ARM 10 pin) | 2×5 1.27 mm | 1 VTref, 2 SWDIO, 3 GND, 4 SWCLK, 5 GND, 6 SWO, 7 KEY, 8 NC/TDI, 9 GNDDetect, 10 nRESET |
| SWD (basit) | 1×5 2.54 mm | 3V3, SWDIO, SWCLK, NRST, GND (serigrafiye pin adlarını yaz) |
| UART | 1×4/1×6 2.54 mm | GND, 3V3/5V, TX, RX (FTDI 6 pin: GND CTS VCC TX RX DTR) |
| Tag-Connect | TC2030 | Yer kazandırır; footprint ve yasak bölgesine dikkat et |

## 7. MCU Bloğu Kontrol Listesi

- [ ] Her VDD/VDDA dekuplajı var ve pinlere yakın
- [ ] Reset/EN RC devresi var; boot/strap pinleri doğru seviyede
- [ ] Programlama/debug portu var ve pin sırası serigrafide yazılı
- [ ] Kristal yük kondansatörleri hesaplandı, layout kurallarına uyuldu
- [ ] USB pull-up/seri direnç ihtiyacı MCU serisine göre kontrol edildi
- [ ] Yasak pinler (flash/PSRAM, SWD) kullanılmadı
- [ ] 5 V'luk dış sinyaller için tolerans/seviye dönüşümü sağlandı
- [ ] Anten keepout ve yerleşimi doğru (kablosuz modüllerde)
