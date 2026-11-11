# 09 — Motor Sürücüler (DC, Step, Güç Katı)

## 1. Sürücü Seçimi

| Uygulama | Entegre örnekleri | Not |
|---|---|---|
| Küçük fırçalı DC (≤1.5 A) | DRV8833, TB6612FNG, DRV8871 (3.6 A) | H-köprü, PWM ile hız kontrolü |
| Step motor (≤2 A) | TMC2209 (sessiz, UART), DRV8825, A4988 | Akım ayarı Vref ya da sense direnci ile yapılır |
| Harici closed-loop sürücü (ör. Leadshine) | STEP/DIR/EN optolu girişler | MCU tarafında 5 V sinyal ya da opto sürme akımı gerekir; seviye kontrolü yap |
| Yüksek akım DC | Gate driver + N-MOSFET köprü | IR2104, DRV8701 ya da yarım köprü sürücüleri |
| Tek yönlü yük (fan, solenoid, röle, LED şerit) | Low-side N-MOSFET (AO3400A, SI2302; büyük akımda DPAK) | **Flyback diyotu şart** (indüktif yük) |

## 2. Low-Side MOSFET Anahtar (en sık kullanılan)

```
VLOAD ──┬── YÜK ──┬── Drain (Q1)
        └─|<|─────┘   (flyback diyot: katot VLOAD tarafında; SS34 / 1N5819 / indüktif yükler için)
GPIO ── Rg 47–100Ω ── Gate
                      Gate ── Rpd 100k ── GND  (MCU reset'teyken FET kapalı kalsın)
Source ── GND (güç dönüşü)
```
- MOSFET **logic-level** olmalı: Rds(on) değeri 2.5 V / 3.3 V Vgs'de tanımlı olmalı. 4.5 V'ta tanımlıysa 3.3 V GPIO ile yeterince açılmaz.
- Kayıp: P = I² × Rds(on) + anahtarlama kaybı. SOT-23 için ~0.5 W sınırına dikkat et.
- PWM frekansı yüksekse (>20 kHz) gate sürücü gerekebilir.

## 3. Sürücü Entegre Layout'u (DRV8833/TB6612/TMC2209 vb.)

1. **VM bulk kondansatörü:** elektrolitik ya da polimer 47–100 µF (motor akımı ve kablo uzunluğuna göre) + 100 nF seramik, VM pinine ≤10 mm. Seramik olan pine ≤2 mm konur.
2. **Sense direnci** (ör. 0R1–0R22, 1206/2512): sürücünün SENSE pinine yakın. Ölçüm için **Kelvin** bağlantı kur: direncin GND tarafı güç GND'ye, ölçüm hattı direnç pad'inden ayrı iz olarak IC'ye gelir. Güç: P = I²R → %100 pay bırak.
3. **EP (exposed pad):** ısıl via dizisi (0.3 mm, 3×3 ya da daha fazla) + alt katmanda geniş GND dökümü. TMC2209 gibi parçalar kart bakırı ile soğur.
4. **Motor çıkış izleri:** geniş (akım tablosu), kısa, konnektöre doğrudan gider. Çıkışları lojik bölgenin üzerinden geçirme.
5. **Güç GND dönüşü:** motor akımı, sürücü GND'si → bulk C → güç girişi yolunu izler. Bu yol MCU ve sensörlerin altından geçmez. Lojik ve motor GND'si tek düzlemdedir ancak yerleşimle akım yolları ayrılır.
6. Charge pump ve VCP kondansatörleri datasheet'teki değerde ve pine yakın olur.
7. Step sürücüde microstep (MS1/MS2) ve EN pinlerini yazılımla ya da jumper ile kontrol edilebilir bırak.

## 4. Koruma

- VM girişinde **TVS** (motor geri EMF ve kablo indüktansı ani gerilim üretir): 12 V sistem için SMBJ15A, 24 V için SMBJ28A–30A.
- Ters kutup koruması: yüksek akımda P-FET ya da ideal diyot denetleyici kullan.
- Bulk kondansatörün gerilim değeri ≥1.5 × VM olmalı. Motor fren/geri besleme yapıyorsa (regen) bu değeri ve TVS'yi buna göre seç.
- Sürücü fault/nFAULT çıkışı (açık-drain) pull-up ile MCU'ya bağlanır.
- Uzun kabloya giden STEP/DIR/EN gibi lojik çıkışlara 100 Ω seri direnç konur. Optolu harici sürücülerde opto LED akımını (tipik 7–16 mA) GPIO'nun verip veremediği kontrol edilir; gerekirse transistör ya da buffer (74HCT245, ULN2003 değil) kullanılır.

## 5. Akım Ölçme

- Low-side shunt + op-amp (ör. INA181/INA199) ya da high-side akım sensörü (INA219/INA226 I2C, ACS712 Hall).
- Shunt değeri: Vshunt_max = I_max × R. Tipik hedef 50–100 mV.
- Shunt'a Kelvin bağlantı, ölçüm hatları birbirine paralel ve yakın çekilir (diferansiyel), ADC'de RC filtre kullanılır.

## 6. Motor Bloğu Kontrol Listesi

- [ ] Sürücü akım ve gerilim payı yeterli; ısıl hesap yapıldı
- [ ] VM bulk + seramik kondansatörler pine yakın
- [ ] Sense direnci Kelvin bağlı ve güç değeri yeterli
- [ ] EP ısıl via + bakır alan var
- [ ] İndüktif yüklerde flyback diyot var
- [ ] Gate pull-down ve gate direnci var (diskret FET)
- [ ] TVS ve ters kutup koruması var
- [ ] Yüksek akım yolu lojik bölgeden geçmiyor
- [ ] Motor konnektörü akım değerine uygun (JST XH ≤3 A, klemens daha yüksek)
