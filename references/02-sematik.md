# 02 — Şematik Çizim Kuralları (Schematic Capture)

Şematik bir **belge**dir. Bunu ilk kez gören bir mühendis, devreyi 2 dakikada anlayabilmelidir.

## 1. Sayfa Organizasyonu

- **Bir sayfa = bir fonksiyon bloğu.** Örnek sırası: 1 Kapak/blok diyagram/revizyon notları → 2 Güç girişi ve koruma → 3 Regülatörler → 4 MCU → 5 Arayüzler/konnektörler → 6 Motor sürücü...
- Küçük projede (≤40 parça) tek sayfa olabilir. Bu durumda sayfa **çerçeveli bölgelere** (grafik dikdörtgen + başlık) ayrılır: "GÜÇ GİRİŞİ", "3V3 LDO", "MCU", "KONNEKTÖRLER".
- Sayfa boyutu: A4, çok doluysa A3. Sayfayı doldurmak için sıkıştırma; yeni sayfa aç.
- Başlık bloğu (title block): proje adı, sayfa adı, revizyon (v0.1), tarih, çizen. Şirket adı yazılmaz.
- Kapak sayfasında revizyon geçmişi ve genel notlar bulunur ("Aksi belirtilmedikçe dirençler 0603 %1, kondansatörler 0603 X7R").

## 2. Yerleşim ve Akış

- **Sinyal soldan sağa** akar: girişler (konnektör, sensör) solda, işlem ortada, çıkışlar (sürücü, konnektör) sağda.
- **Güç yukarıdan aşağıya** akar: pozitif rayın sembolü yukarı, GND sembolü aşağı bakar. GND sembolü asla yukarı bakmaz.
- Güç zinciri soldan sağa çizilir: Giriş → koruma → regülatör → çıkış.
- IC sembolleri ortalanır, çevre parçaları ilgili pinin yanına konur.
- Her IC'nin **dekuplaj kondansatörleri IC sembolünün hemen yanında**, güç pinine yakın durur ve "her VDD pinine bir 100n" düzeni görünür.
- Pull-up/pull-down dirençleri ait oldukları pinin yanında olur.
- Boşluk bırak: bloklar arasında en az 10–15 mm (400–600 mil) boşluk olmalı. Sıkışık şematik amatör görünür.

## 3. Bağlantı: Tel mi, Label mı?

| Durum | Yöntem |
|---|---|
| Aynı blok içinde, yakın bağlantı | **Tel (wire)** |
| Blok/sayfa arası bağlantı | **Net label** (sayfa içi) / **global label / hiyerarşik port** (sayfalar arası) |
| Güç rayları | **Güç sembolleri** (+3V3, +5V, VBAT, GND). Ray için tel çekme. |
| Bus (veri yolu) | Bus + bus entry ya da her hatta label; isimler `D0..D7` |

Kurallar:
- Her pine label koyup hiçbir tel çizmemek ("label çorbası") **yasaktır**. Okuyucu devreyi göremez.
- Bir tel başka bir sembolün üzerinden ya da pin üzerinden geçmez.
- **4 yollu kavşak (4-way junction) yok.** T birleşmeleri kullan, kavşağı ikiye böl.
- Tel köşeleri 90°'dir; çapraz tel yoktur.
- Kesişen ama bağlanmayan teller noktasız kesişir. Bağlantı noktası (junction dot) yalnızca T birleşiminde kullanılır.
- Tel uçları pinlere tam oturmalıdır (KiCad: 1.27 mm / 50 mil ızgara; asla ızgara dışı çalışma).
- Label tel üzerinde ve okunur yönde (0° veya 90°) olur.

## 4. İsimlendirme

- **Referans (designator):** R, C, L, D, LED (veya D), Q, U, J (konnektör), SW, F (sigorta), FB (ferrit), Y (kristal), TP (test noktası), H (montaj deliği), BZ. Numaralar sayfaya/bloğa göre sıralı olmalı (soldan sağa, yukarıdan aşağıya, annotate).
- **Değer yazımı:** `10k`, `4k7`, `100R`, `0R`, `100n`, `4u7`, `10u`, `22p`. Tutarlı ol. Gerekiyorsa yanında gerilim/tolerans: `10u 25V X5R`, `0R1 1% 1W`.
- **Net adları:** BÜYÜK HARF, anlamlı: `I2C1_SDA`, `SPI_SCK`, `MOTOR_A_IN1`, `VBUS`, `VBAT`, `+3V3`. Aktif-düşük sinyallerde KiCad'de `~{RESET}`, EasyEDA'da `RESET_N` ya da `nRESET`.
- Ray adlarında birim: `+5V`, `+3V3`, `+12V`, `VMOT`.
- Anlamsız otomatik net adları (Net-(R1-Pad2)) önemli hatlarda kalmamalı; ölçüm veya debug yapılacak her hatta isim olmalı.

## 5. Sembol Kalitesi

- Pin isimleri ve numaraları görünür olmalı. IC sembolünde pinler **fonksiyona göre** gruplanır (güç üstte, GND altta, girişler solda, çıkışlar sağda). Fiziksel sıraya göre dizilmez.
- Kutuplu parçalar (diyot, elektrolitik, LED) doğru yönde çizilir; diyot katodu akışa uygun yönde olur.
- Konnektör sembolünde pin numarasının yanında sinyal adı da görünmelidir (label ile).
- Bağlanmayan pinlere **No-Connect (X)** işareti konur. Boş pin bırakılmaz.
- Kullanılmayan op-amp/kapı birimleri datasheet'e göre sonlandırılır.

## 6. Alanlar (Fields) — her parçada

| Alan | Örnek | Neden |
|---|---|---|
| Value | 10k | |
| Footprint | R_0603_1608Metric | |
| **LCSC** | C25804 | JLC dizgi BOM'u |
| MPN | 0603WAF1002T5E | Alternatif tedarik |
| DNP (gerekirse) | DNP | Takılmayacak parça |

EasyEDA'da LCSC alanı kütüphaneden gelir. **"Supplier Part" alanının dolu olduğunu kontrol et.**

## 7. Notlar ve Dokümantasyon Şematiğin İçinde

- Kritik hesaplar şematiğe not olarak yazılır: `Vout = 0.6 × (1 + R1/R2) = 5.02 V`, `Iprog = 1000/Rprog = 1 A`.
- Layout notları da şematiğe yazılır: "C5 U3 VIN pinine ≤2 mm", "R10 Kelvin bağlantı".
- Konnektörlerin yanına kablo/karşı konnektör bilgisi yazılır.
- Test noktaları (TP) şematikte yer alır: her ray, GND, önemli haberleşme hatları.
- Montaj delikleri (H1..H4) ve fiducial'lar şematikte sembol olarak bulunur (BOM'a girmemeleri için "exclude from BOM").

## 8. Elektriksel Kontrol (ERC)

- KiCad: güç girişine **PWR_FLAG** koy (regülatör çıkışı, konnektörden gelen ray). Uyarıları "susturmak" için koyma; gerçekten güç kaynağı olan yerlere koy.
- ERC'yi **0 hata** ile bitir. Uyarıları tek tek açıkla ya da düzelt.
- ERC'nin yakalayamadıkları için manuel kontrol yap:
  - Her IC'nin her güç pini bağlı mı, her GND/EP (exposed pad) GND'ye bağlı mı?
  - Pull-up gereken açık-drain hatlarda pull-up var mı (I2C, INT, RESET, open-drain LED)?
  - Gerilim seviyeleri uyumlu mu (5 V çıkış → 3V3 giriş)?
  - Kutup ve pinout doğru mu (SOT-23 transistörlerde BCE, MOSFET'lerde GSD; LDO'larda pin dizilimi üreticiye göre değişir!)?

## 9. Şematik Review Kontrol Listesi

→ `12-kontrol-listeleri.md` §Şematik
