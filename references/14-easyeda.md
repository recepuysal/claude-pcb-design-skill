# 14 — EasyEDA ile Çalışma

Kullanıcının ana aracı EasyEDA'dır (Pro). Claude, EasyEDA arayüzünü doğrudan süremez. Kullanıcının fare ve odağına dokunan GUI otomasyonu **yasaktır**. Bu nedenle aşağıdaki çalışma modlarından birini seç ve projenin başında kullanıcıya hangisini kullandığını söyle.

## Mod A — Tasarım Paketi (kullanıcı EasyEDA'da çizer, Claude yönetir)

Claude her faz için hazır bir "uygulama paketi" üretir. Kullanıcı bunu EasyEDA'da uygular:
1. **Şematik paketi:** blok (kutu) listesi, her blokta parçalar (refdes, değer, LCSC kodu), bağlantı tablosu (`U1.VIN ↔ C1.1 ↔ +5V`), net label adları ve notlar. Kutu yerleşimini ASCII ya da tablo olarak verir (hangi kutu nerede).
2. **Yerleşim paketi:** kart ölçüsü, delik koordinatları, her kritik parçanın koordinatı ve rotasyonu (tablo), blok bölgeleri ve mesafe kuralları.
3. **Routing paketi:** net class tablosu (EasyEDA *Design Rules*'a girilecek değerler), kritik hatların sırası ve özel talimatları, döküm ayarları.
4. **Review:** kullanıcı EasyEDA'dan **PDF (şematik) + PNG/PDF (PCB üst/alt) + 3D görüntü** export eder. Claude bunları Read ile açıp `12-kontrol-listeleri.md`'ye göre inceler ve bulguları "nerede, ne, nasıl düzeltilir" formatında listeler.

## Mod B — KiCad'de Üret, EasyEDA'ya Aktar

Claude projeyi KiCad'de üretir (betikle, `15-kicad-otomasyon.md`). ERC/DRC ve render ile doğrular. Kullanıcı projeyi EasyEDA Pro'ya aktarır: *File > Import > KiCad* (şematik + PCB). Aktarımdan sonra:
- Parçaların LCSC alanlarını ve footprint eşleşmelerini kontrol et.
- Design rules'u EasyEDA'da yeniden gir (aktarımla gelmeyebilir).
- Dökümleri yeniden doldur (Shift+B).
- Arc izler ve teardrop'lar doğru aktarıldı mı, kontrol et.

## Mod C — Review Modu (mevcut EasyEDA tasarımı)

Kullanıcı çizer ve Claude yalnızca inceler. Export istenecek dosyalar:
- Şematik: *Export > PDF* (tüm sayfalar)
- PCB: *Export > PDF/Image*: Top, Bottom ve her katman ayrı ayrı; ayrıca 3D görünüm
- Gerekirse: BOM ve Pick&Place CSV, Gerber zip
- DRC raporu (*Design > Check DRC* sonucu)

## EasyEDA Design Rules (JLC 2 kat varsayılanı)

| Kural | Değer |
|---|---|
| Track width (default) | 0.254 mm (10 mil) |
| Clearance | 0.2 mm |
| Via diameter / drill | 0.6 / 0.3 mm |
| Track width (power) | Net class: `POWER` = 0.5–1.0 mm |
| Copper to board outline | 0.5 mm |
| Copper area clearance | 0.3 mm |

## EasyEDA İpuçları

- Parça eklerken *Library > JLCPCB Assembled Parts / Basic* filtresi kullanılır (Basic parça önceliği).
- Footprint ve 3D model LCSC'den gelir. Pin 1 yönünü 3D görünümde kontrol et.
- Kutu kutu şematik: *Place > Rectangle* (kesikli çizgi), başlık *Text* ile (kalın, büyük) yazılır.
- Smooth yollar: routing sırasında köşe modunu **Arc**'a al. Mevcut köşeleri yuvarlatma ve teardrop araçları *Tools* menüsündedir (sürüme göre adı değişebilir).
- Bakır döküm: *Place > Copper Area*, GND neti, "Remove islands" açık; her değişiklikten sonra Shift+B ile yeniden doldur.
- Sipariş: *Fabrication > PCB Order* ile JLC'ye doğrudan sipariş verilir. BOM ve CPL otomatik gider.
- EasyEDA'da `JLCJLCJLCJLC` metni sipariş numarasının yerini belirler.
