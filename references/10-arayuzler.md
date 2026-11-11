# 10 — Haberleşme Arayüzleri (SPI, I2C, UART, USB, CAN, RS-485) ve ESD

## 1. I2C

- Açık-drain hat; **SDA ve SCL'de pull-up şart** (bir hatta yalnızca bir pull-up seti olmalı; birden fazla modül kendi pull-up'ını getiriyorsa bunlar paralel bağlanır ve toplam değeri hesaba kat).
- Pull-up aralığı (`pcb_calc.py i2c`):
  - Rmin = (VDD − 0.4 V) / 3 mA → 3.3 V'ta ≈ 967 Ω
  - Rmax = tr / (0.8473 × Cb); tr = 1000 ns (100 kHz), 300 ns (400 kHz), 120 ns (1 MHz)
  - Tipik değerler: **4.7 kΩ** (100 kHz, kısa hat), **2.2 kΩ** (400 kHz), 1 kΩ (1 MHz ya da uzun hat)
- Toplam hat kapasitesi ≤400 pF. Kart dışına uzun kablo (>30–50 cm) gidiyorsa I2C uygun değildir; buffer (P82B715, PCA9615 diferansiyel) kullanılır.
- Adres çakışmalarını pin tablosunda kontrol et. Adres pinleri GND/VDD'ye doğrudan bağlanmalı, boş bırakılmamalı.
- Seviye dönüştürme (3V3 ↔ 5V): BSS138 tabanlı çift yönlü devre ya da PCA9306/TXS0102 (I2C için TXB serisi **kullanılmaz**).
- Kart dışına çıkan I2C hattına 33–100 Ω seri direnç + ESD koruması konur.
- Qwiic/STEMMA QT standardı: JST SH 4 pin, 1 GND, 2 3V3, 3 SDA, 4 SCL.

## 2. SPI

- Hatlar: SCK, MOSI (COPI), MISO (CIPO), her slave için ayrı CS.
- **CS hatlarına 10 kΩ pull-up** konur; MCU açılırken slave'ler seçili kalmasın.
- Birden fazla slave varsa MISO'yu tri-state yapmayan cihazlara dikkat et (bazı SD kart ve modüller CS pasifken MISO'yu bırakmaz).
- SCK en kritik hattır: kısa tut, sürücüye yakın **22–33 Ω seri direnç** (kenar yumuşatma / kaynak sonlandırma) koy. >10 MHz ya da >10 cm hatlarda bu dirençler şarttır, diğer durumlarda DNP olarak yer bırakmak iyi bir alışkanlıktır.
- SCK izinin altında kesintisiz GND bulunur; SCK paralel uzun hatlardan uzak tutulur.
- Port genişletici **MCP23S17**: **RESET pinini 10k ile VDD'ye çek** (boş bırakılırsa çip rastgele resetlenir). Donanım adresi (A0–A2) kullanılacaksa IOCON.HAEN yazılımla etkinleştirilir. INTA/INTB açık-drain olarak ayarlanacaksa pull-up gerekir. Her çipe 100 nF dekuplaj konur.
- Dışarıya (kablo/konnektör) giden GPIO'lar doğrudan IC pinine bağlanmamalı: 100–330 Ω seri direnç + ESD koruması kullanılmalı. (Kablo test cihazı gibi uygulamalarda bu karar kullanıcıyla bilinçli olarak verilmeli.)
- SD kart: tüm hatlarda 10–47k pull-up (SD spec), VDD'de 10 µF + 100 nF, kart takma anında inrush oluşabilir (gerekirse yük anahtarı).

## 3. UART

- TX → RX çapraz bağlanır. Net isimlerini **MCU perspektifinden** yaz (`MCU_TX`, `MCU_RX`) ve konnektör serigrafisinde bu bilgiyi belirt. Çapraz bağlantı karışıklığı en sık yapılan hatadır.
- Boşta yüksek (idle high): RX hattına 10k pull-up koyabilirsin (konnektör boşken gürültüyü önler).
- 5 V cihazla bağlantıda seviye uyumuna dikkat et: MCU RX'ine bölücü ya da seviye dönüştürücü ekle.
- USB-UART: CH340C (kristalsiz), CP2102N. TXD/RXD hatlarına 1k seri direnç konursa, cihaz kapalıyken hat üzerinden besleme (back-powering) azalır.

## 4. USB 2.0 Full-Speed (12 Mbps)

- D+/D− **diferansiyel çift** olarak çizilir: 90 Ω hedef (2 katman 1.6 mm'de tam tutturulamaz; FS hızında sorun olmaz). Kısa (≤5 cm ideal), eşit uzunlukta (±0.15 mm), via'sız, kesintisiz GND üzerinde ve birbirine paralel çizilir.
- ESD: **USBLC6-2SC6** (C7519) ya da benzeri konnektörün hemen dibine konur. Hat önce ESD pad'inin üzerinden geçer, sonra IC'ye gider (stub oluşturma).
- Seri direnç: MCU'ya göre değişir (RP2040 27 Ω, STM32/ESP32-S3'te genelde gerekmez).
- VBUS algılama (self-powered cihaz): bölücü ile GPIO'ya bağlanır.
- USB-C veri: A6/B6 (D+) ve A7/B7 (D−) birleştirilir. Bu birleşme konnektörün altında kısa bir via köprüsüyle ya da iki tarafta simetrik izle yapılır.

## 5. RS-485 / CAN (endüstriyel, uzun kablo)

- RS-485: transceiver (MAX3485 3V3, SP3485, THVD1410), hat sonunda **120 Ω terminasyon** (jumper ile seçilebilir), fail-safe bias (A'ya 560–680 Ω pull-up, B'ye pull-down; ya da dahili fail-safe özellikli transceiver), TVS (SM712), DE/~RE kontrol pini.
- CAN: transceiver (TJA1051, SN65HVD230 3V3), 120 Ω terminasyon (split termination: 2×60 Ω + 4.7 nF), ESD (PESD2CAN), CANH/CANL diferansiyel çift.
- Konnektörde GND referansı da taşınır.

## 6. Dijital Giriş / Çıkış ve Dış Dünya

- Buton: dahili ya da harici pull-up + 100 nF debounce (isteğe bağlı) + kablo uzunsa ESD.
- 12/24 V endüstriyel giriş: optokuplör (PC817/LTV-356T) + akım sınırlama direnci + ters diyot; ya da bölücü + Zener/TVS.
- Optokuplör çıkışı pull-up ile MCU'ya bağlanır; CTR değerine göre direnç hesaplanır.
- Röle: low-side MOSFET + flyback diyotu; bobin akımına göre FET seçilir.
- LED: R = (VDD − Vf) / I. 3.3 V ve kırmızı LED için 1k → ~1.3 mA (gösterge LED'i için yeterli; parlak LED kullanmaya gerek yok).

## 7. ESD ve Konnektör Koruması

| Nerede | Ne |
|---|---|
| USB veri | USBLC6-2SC6 |
| Genel GPIO (kablo) | TVS dizisi (SRV05-4, ESDA6V1, TPD4E05) + 100 Ω seri direnç |
| Güç girişi | SMBJ/SMAJ (Vrwm ≥ nominal) |
| RS-485 | SM712 |
| CAN | PESD2CAN |

Yerleşim kuralı: **Konnektör → ESD → seri direnç → IC.** ESD diyotunun GND'si kısa yoldan ve çoklu via ile GND düzlemine bağlanır. Uzun GND yolu ESD korumasını etkisiz kılar.

## 8. Arayüz Kontrol Listesi

- [ ] I2C pull-up'ları hesaplandı, tek set var, adres çakışması yok
- [ ] SPI CS pull-up'ları var, SCK seri direnci (ya da DNP yeri) var
- [ ] MCP23S17 RESET pull-up, HAEN/adres pinleri tanımlı
- [ ] UART TX/RX isimlendirmesi MCU perspektifinden ve doğru çaprazlanmış
- [ ] USB ESD konnektörde, diferansiyel çift kurallarına uyuldu
- [ ] Dış dünyaya giden tüm hatlarda ESD + seri direnç var
- [ ] Gerilim seviyeleri uyumlu (3V3 ↔ 5V)
