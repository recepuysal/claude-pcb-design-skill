# 15 — KiCad Otomasyonu ve Öz-İnceleme

KiCad 10.0 kurulu: `C:\Program Files\KiCad\10.0\bin\kicad-cli.exe`. KiCad'in kendi Python'u: `C:\Program Files\KiCad\10.0\bin\python.exe` (pcbnew modülü bununla çalışır).

## 1. kicad-cli Komutları

```bash
K="/c/Program Files/KiCad/10.0/bin/kicad-cli.exe"
"$K" sch erc --format json --severity-all -o erc.json proje.kicad_sch
"$K" sch export pdf -o schematic.pdf proje.kicad_sch
"$K" sch export netlist -o netlist.net proje.kicad_sch
"$K" pcb drc --format json --severity-all --schematic-parity --refill-zones -o drc.json proje.kicad_pcb
"$K" pcb export pdf --mode-single -l F.Cu,F.Silkscreen,Edge.Cuts --scale 0 -o top.pdf proje.kicad_pcb
"$K" pcb render --side top --quality high -o 3d_top.png proje.kicad_pcb
"$K" pcb render --rotate -45,0,45 --perspective -o 3d_iso.png proje.kicad_pcb
```
Hepsi tek komutta: `python scripts/review.py proje.kicad_pro` → `review/` klasörüne ERC/DRC JSON, PNG'ler ve SUMMARY.txt yazılır.

## 2. Programatik Tasarım Üretimi (gerekirse)

- Şematik ve PCB dosyaları **S-expression** formatındadır. Betikle üretmek mümkündür, ancak elle düzenlenmiş bir projeyi **asla** betikle üzerine yazma. Kullanıcı KiCad'de düzenleme yaptıysa KiCad dosyası esas alınır.
- Şematik üretim kuralları:
  - Tüm koordinatlar **1.27 mm ızgarada** olur; pin uçları ve tel uçları birebir çakışır. ERC'de `endpoint_off_grid` uyarısı çıkmamalıdır.
  - Her blok için önce sınır kutusu hesaplanır, kutular ızgara düzeninde yerleştirilir (`00-kullanici-stili.md`). Blok içinde parçalar sinyal akışına göre dizilir.
  - Telleri yalnızca yatay/dikey segmentlerle çiz. Bir telin başka bir pinin üzerinden geçmediğini kontrol et.
  - `lib_symbols` bölümüne sembol tanımları gömülür. Kütüphane uyuşmazlık uyarıları (lib_symbol_mismatch) temizlenir ya da açıklanır.
  - UUID'ler sabit tutulmalıdır (deterministik üret). Aksi halde PCB'deki eşleşme bozulur ve "referansa göre yeniden bağla" gerekir.
- PCB üretimi: KiCad Python (`pcbnew`) ile footprint yükle, konumla, net ata. Arc izler için `PCB_ARC` kullanılır (start, mid, end). Dökümler `ZONE` ile oluşturulur ve `ZONE_FILLER` ile doldurulur.
- Netlist doğrulaması: üretimden sonra beklenen bağlantı listesini netlist ile karşılaştıran bir betik yaz (`verify_netlist.py` yaklaşımı). Bu, en değerli otomatik testtir.

## 3. Routing Gerçekçiliği

- Otomatik yol çizimi (Freerouting vb.) profesyonel sonuç vermez. Kritik ağları (güç, kristal, USB, SMPS) **kurallı olarak elle (betikle koordinat vererek)** çiz. Geri kalanı kullanıcıyla birlikte interaktif router'da tamamla.
- Kullanıcıya routing için "rehber" sunmak çoğu zaman daha verimlidir: hangi hat hangi katmanda, hangi sırayla, hangi genişlikte.

## 4. Görsel Öz-İnceleme Prosedürü

1. `review.py` çalıştır.
2. `SUMMARY.txt` oku: hata sayıları ve türleri.
3. PNG'leri sırayla aç:
   - `schematic*.png`: kutu düzeni, akış, label çorbası, okunurluk
   - `pcb_top.png` / `pcb_bottom.png`: yerleşim grupları, izlerin düzgünlüğü, alt GND bütünlüğü
   - `pcb_silk_top.png`: serigrafi çakışmaları, refdes konumları
   - `3d_iso.png`: konnektör yönleri, yükseklik çakışmaları
4. Bulguları `12-kontrol-listeleri.md` formatında raporla, düzelt ve tekrar çalıştır.
5. Büyük kartlarda görüntü küçük kalırsa ilgili bölgeyi kırpıp büyüt (PyMuPDF ile `clip` kullanarak) ve kritik bölgelere (SMPS, MCU, USB) ayrı ayrı yakından bak.
