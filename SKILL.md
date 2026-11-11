---
name: pcb-design
description: Profesyonel şematik + PCB tasarım süreci (EasyEDA ve KiCad, JLCPCB üretim/dizgi kurallarına göre). Kullanıcı şematik çizmek, PCB çizmek/yerleştirmek/route etmek, devre tasarlamak, mevcut bir şematik/PCB'yi (PDF, PNG, Gerber, KiCad/EasyEDA dosyası) incelemek ya da güç, Li-ion şarj, MCU (STM32, ESP32), motor sürücü, SPI/I2C/UART/USB/RS485 devresi kurmak istediğinde kullan. Use for any schematic capture, PCB layout, design review or JLCPCB fabrication/assembly task.
---

# PCB Tasarım Skill'i (PCB Design Skill)

Amaç: Bağlantısı doğru olan bir çizim değil, **bir donanım mühendisinin onaylayacağı** profesyonel bir proje çıkarmak.
Dil: Kullanıcıya Türkçe yaz; teknik terimleri gerekiyorsa parantez içinde İngilizce ver (ör. "dekuplaj (decoupling)").

## Varsayılanlar (kullanıcı aksini söylemedikçe)

| Konu | Varsayılan |
|---|---|
| Araç | Kullanıcının ana aracı **EasyEDA (Pro)**. Otomatik üretim/doğrulama gerekirse **KiCad 10** (`C:\Program Files\KiCad\10.0\bin\kicad-cli.exe`). |
| Üretici | **JLCPCB** (PCB + PCBA). Kurallar: `references/04-jlcpcb-kurallar.md` |
| Katman | **2 katman**, 1.6 mm FR-4, 1 oz, HASL kurşunsuz veya ENIG, yeşil maske |
| Dizgi | JLC PCBA, mümkünse **tek yüz (Top)** ve **Basic parça** |
| Pasif paket | 0603 (elle lehim olacaksa 0805; yoğun kartta 0402) |
| Şirket adı | Kartta, repoda, dosyada **şirket adı yazma** (kullanıcı ayrıca isterse hariç) |
| Şematik stili | **Kutu kutu blok düzeni:** her fonksiyon bloğu başlıklı ve hizalı bir çerçeve içinde |
| PCB yol stili | **Smooth / arc köşeli yollar** + teardrop |

**Kullanıcı stili zorunludur:** Her projede `references/00-kullanici-stili.md` dosyasını oku ve uygula.

## İş Akışı — Fazlar ve Kapılar (Phase Gates)

Her fazın sonunda o fazın **kontrol listesini** (`references/12-kontrol-listeleri.md`) uygula. Kapı geçilmeden sonraki faza geçme. Kullanıcıya her kapıda kısa bir özet ver ve kararı gereken noktaları sor.

| Faz | İş | Okunacak referans | Kapı çıktısı |
|---|---|---|---|
| 0 | Gereksinim toplama | `01-gereksinim-mimari.md` | Gereksinim tablosu + açık sorular |
| 1 | Blok diyagram, güç bütçesi, arayüz listesi | `01-gereksinim-mimari.md` | Blok diyagram, güç ağacı, GPIO/pin tablosu |
| 2 | Parça seçimi (JLC stok, Basic/Extended) | `03-komponent-secimi.md` | BOM taslağı (LCSC kodlu) |
| 3 | Şematik | `02-sematik.md` + ilgili konu dosyaları (07–10) | ERC temiz + şematik review |
| 4 | Kart mekaniği, stackup, kurallar | `04-jlcpcb-kurallar.md` | Kart ölçüsü, delikler, net class tablosu |
| 5 | Yerleşim (placement) | `05-yerlesim.md` | Yerleşim planı → review → kullanıcı onayı |
| 6 | Yol çizimi (routing) + bakır dökme | `06-routing.md` | DRC temiz + görsel review |
| 7 | Silkscreen + dokümantasyon | `11-silkscreen-dokuman.md` | Okunur, düzenli serigrafi |
| 8 | Üretim çıktıları | `13-uretim-ciktilari.md` | Gerber, drill, BOM, CPL, PDF, 3D |
| 9 | Ders çıkarma | `16-dersler.md` | Yeni dersleri dosyaya ekle |

Konu dosyaları (ihtiyaca göre oku):
- Güç, regülatör, Li-ion şarj, USB-C güç, koruma → `references/07-guc-sarj.md`
- MCU (STM32, ESP32-S3, RP2040), kristal, reset, programlama → `references/08-mcu.md`
- Motor sürücü (DC, step, MOSFET köprü), akım ölçme → `references/09-motor-surucu.md`
- SPI, I2C, UART, USB, CAN, RS-485, ESD, port genişletici → `references/10-arayuzler.md`
- EasyEDA ile çalışma (teslim yöntemleri, ayarlar) → `references/14-easyeda.md`
- KiCad otomasyonu, kicad-cli, render ile öz-inceleme → `references/15-kicad-otomasyon.md`

**Her projeye başlarken `references/16-dersler.md` dosyasını oku.** Önceki projelerde yapılmış hataları tekrarlama.

## Altın Kurallar (her zaman geçerli)

1. **Önce mimari, sonra çizim.** Blok diyagram ve güç ağacı olmadan sembol koyma.
2. **Datasheet'in "Typical Application" ve "Layout Guidelines" bölümünü oku** ve uygula. Uydurma değer kullanma; değeri hangi formülle ya da datasheet'in hangi bölümünden aldığını not et.
3. **Şematik okunacak bir belgedir.** Sinyal soldan sağa, güç yukarıdan aşağıya akar. Bir sayfa bir fonksiyondur. Kimse onu çözmek zorunda kalmamalı.
4. **Yerleşim, routing'in %80'idir.** Kötü yerleşimi iyi routing kurtaramaz.
5. **Her akımın bir dönüş yolu vardır.** 2 katmanda alt katman mümkün olduğunca kesintisiz GND'dir.
6. **Ölçülebilir kurallar kullan.** "Yakın koy" yerine "≤2 mm" yaz, "kalın yap" yerine "1 A → ≥0.5 mm" yaz.
7. **Doğrulamadan "bitti" deme.** ERC/DRC sıfır hata, görsel review yapılmış ve checklist geçilmiş olmalı. Doğrulanmamış varsayımları (pin1 yönü, konnektör dizilimi, ölçüler) kullanıcıya **açıkça listele**.
8. **Üretilebilirlik.** JLC kapasitesinin sınırında değil, rahat içinde kal (ör. iz/boşluk 0.2/0.2 mm, via 0.3/0.6 mm).

## Yapay Zekâ Tuzakları (önceki çizimlerin "amatör" görünmesinin sebepleri)

Bunları bilinçli olarak engelle:
- Sembolleri ızgara gibi dizip her şeyi net label ile bağlamak → okunmuyor. **Yakın bağlantılar tel ile, uzak/sayfalar arası bağlantılar label ile** yapılmalı.
- Sinyal akışı yok; giriş konnektörü sağda, çıkış solda kalıyor.
- Dekuplaj kondansatörleri şematikte IC'den uzakta duruyor, PCB'de de pinden uzağa düşüyor.
- PCB'de parçalar fonksiyon bloklarına göre değil, rastgele ya da sıkıştırılarak yerleşiyor.
- Yollar keyfi açılarla çiziliyor, pad'e yandan giriyor, gereksiz via kullanılıyor, GND dökümü parçalanıyor.
- Serigrafi pad'lerin üzerine biniyor, yönler karışık, kutupluluk işareti yok.
- Değerler birimsiz ya da tutarsız yazılıyor (`10k`, `10K`, `10000`).
- Kart üzerinde bağlantı noktası, test noktası, revizyon ve tarih bilgisi yok.

## Görsel Öz-İnceleme Döngüsü (Self-Review Loop)

Ekranı insan gibi göremediğin için şu yöntemi kullan:
1. Çizimi her önemli adımdan sonra görüntüye çevir. KiCad'de `scripts/review.py` ile ERC/DRC JSON'u, şematik PDF/PNG'si ve PCB katman PNG'leri alınır. EasyEDA'da kullanıcıdan PDF/PNG export istenir.
2. Görüntüyü Read ile aç ve `12-kontrol-listeleri.md` maddelerine göre tek tek bak.
3. Bulduğun sorunları önem sırasına göre listele (Kritik / Önemli / Kozmetik), düzelt ve tekrar render et.
4. En az **2 tur** review yapmadan teslim etme.

## Hesap Araçları

- `scripts/pcb_calc.py`: iz genişliği (IPC-2221), via akımı, I2C pull-up aralığı, LED direnci, gerilim bölücü, kristal yük kondansatörü ve LDO ısıl hesabı. Kullanım: `python scripts/pcb_calc.py --help`
- `scripts/review.py`: KiCad projesi için ERC + DRC + render + özet. Kullanım: `python scripts/review.py <proje.kicad_pro> [--out klasor]`

## Teslim Formatı

Her faz sonunda kullanıcıya şunları ver:
- Ne yapıldı (kısa)
- Kontrol listesi sonucu (geçen/kalan)
- **Doğrulanmamış varsayımlar** ve kullanıcının vermesi gereken kararlar
- Sonraki adım

## Öğrenme Kuralı

Kullanıcı bir hata gösterdiğinde, bir tasarımı beğenmediğinde ya da yeni bir tercih belirttiğinde bunu `references/16-dersler.md` dosyasına tarih ile **kural olarak** ekle (ne oldu → kural). Genelleşebilen bir dersse ilgili referans dosyasını da güncelle. Skill bir git deposudur (`~/.claude/skills/pcb-design`). Değişiklikten sonra commit at ve push et.
