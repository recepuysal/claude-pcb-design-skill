# 13 — Üretim Çıktıları (JLCPCB Fabrication & Assembly)

## 1. Teslim Paketi

```
<proje>_v1.0_<tarih>/
├── gerber/              ← Gerber + drill (zip'lenir → JLC'ye yüklenir)
├── assembly/
│   ├── BOM_JLC.csv      ← Comment, Designator, Footprint, LCSC Part #
│   └── CPL_JLC.csv      ← Designator, Mid X, Mid Y, Layer, Rotation
├── docs/
│   ├── schematic.pdf
│   ├── pcb_assembly_top.pdf
│   ├── 3d_top.png / 3d_iso.png
│   └── README.md        ← revizyon, notlar, doğrulanmamış varsayımlar
└── source/              ← EasyEDA/KiCad kaynak dosyaları
```

## 2. Gerber (JLC gereksinimleri)

Katmanlar (2 kat): F.Cu, B.Cu, F.Mask, B.Mask, F.Silkscreen, B.Silkscreen, F.Paste (stencil için), Edge.Cuts + **Excellon drill** (PTH ve NPTH ayrı ya da birleşik).
- **EasyEDA:** *Fabrication > PCB Fabrication File (Gerber)* → doğrudan JLC'ye sipariş verilebilir. BOM ve Pick&Place da aynı menüdedir.
- **KiCad CLI:**
  ```
  kicad-cli pcb export gerbers --output gerber/ --layers F.Cu,B.Cu,F.Mask,B.Mask,F.Silkscreen,B.Silkscreen,F.Paste,B.Paste,Edge.Cuts --subtract-soldermask --use-drill-file-origin proje.kicad_pcb
  kicad-cli pcb export drill --output gerber/ --format excellon --drill-origin absolute --excellon-units mm --excellon-separate-th --generate-map --map-format gerberx2 proje.kicad_pcb
  ```
  JLC'nin KiCad için önerdiği ayarlar: "Use Protel filename extensions" açık, "Subtract soldermask from silkscreen" açık, drill dosyasında "PTH and NPTH in single file" kapalı (ayrı dosya).
- Gerber'i JLC yüklemeden önce görüntüleyicide (KiCad GerbView / JLC önizleme) kontrol et: kart kenarı kapalı mı, delikler doğru mu, serigrafi kesilmiş mi?

## 3. BOM (JLC formatı)

| Comment | Designator | Footprint | LCSC Part # |
|---|---|---|---|
| 10k | R1,R2,R5 | 0603 | C25804 |

- Aynı LCSC koduna sahip parçalar tek satırda gruplanır.
- DNP parçalar BOM'a girmez (ya da LCSC alanı boş bırakılır).
- KiCad: `kicad-cli sch export bom --fields "Value,Reference,Footprint,LCSC" --labels "Comment,Designator,Footprint,LCSC Part #" --group-by "Value,Footprint,LCSC" --exclude-dnp -o BOM_JLC.csv proje.kicad_sch`

## 4. CPL / Pick and Place

- Sütunlar: `Designator, Mid X, Mid Y, Layer, Rotation` (mm, Layer = Top/Bottom).
- KiCad: `kicad-cli pcb export pos --format csv --units mm --side front --smd-only -o pos.csv proje.kicad_pcb`. Ardından sütun adları JLC formatına çevrilir (Ref→Designator, PosX→Mid X, PosY→Mid Y, Rot→Rotation, Side→Layer).
- **Rotasyon hataları sık görülür.** KiCad ile JLC kütüphanesi arasında SOT-23, SOIC, QFN, diyot ve LED gibi paketlerde 90°/180° fark olabilir. JLC sipariş ekranındaki önizlemede **her parçanın pin 1 ve kutup yönünü kontrol et**. Gerekirse rotasyon düzeltmesi tablosu tut ve `16-dersler.md` dosyasına ekle.
- EasyEDA'da JLC kütüphanesi kullanıldığı için rotasyon genelde doğru gelir. Yine de önizlemede kontrol et.

## 5. Sipariş Öncesi Son Kontrol

- [ ] DRC/ERC sıfır hata
- [ ] Gerber önizlemesi kontrol edildi
- [ ] BOM ↔ CPL refdes'leri eşleşiyor; tüm dizilecek parçaların LCSC kodu var ve stokta
- [ ] Extended parça sayısı ve tahmini maliyet kullanıcıya bildirildi
- [ ] JLC seçenekleri: kalınlık, yüzey kaplaması, renk, sipariş numarası yeri, "Confirm parts placement"
- [ ] Revizyon numarası ve tarih kartta ve dosya adında aynı
- [ ] Kaynak dosyalar ve çıktılar repoya/klasöre kaydedildi
