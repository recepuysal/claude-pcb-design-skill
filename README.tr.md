# pcb-design — Profesyonel Şematik ve PCB Tasarımı için Claude Code Skill'i

🇬🇧 [English README](README.md)

Claude'u disiplinli bir donanım tasarım asistanına çeviren [Claude Code](https://claude.com/claude-code) skill'i. Süreç şöyle ilerler: gereksinim → mimari → şematik → yerleşim → routing → review → JLCPCB üretim çıktıları. Her adımda faz kapıları ve kontrol listeleri uygulanır.

## Öne Çıkanlar

- **Faz kapılı iş akışı** ve ölçülebilir kurallar (ör. "dekuplaj pine ≤2 mm", "1 A → ≥0.5 mm iz").
- **JLCPCB odaklı:** üretim sınırları ve rahat varsayılan değerler, 2 katman stackup, net class'lar, Basic/Extended parça stratejisi, BOM/CPL formatı.
- **Konu rehberleri:** güç ve Li-ion şarj (TP4056, buck/boost, USB-C), MCU (STM32, ESP32-S3, RP2040, kristal), motor sürücüler (DRV8833, TMC2209, MOSFET anahtarlar), arayüzler (I2C, SPI, UART, USB, RS-485, CAN, ESD).
- **Kullanıcı stili:** şematikte kutu kutu fonksiyon blokları, PCB'de smooth (arc) yollar ve teardrop.
- **Araçlar:** EasyEDA (Pro) tasarım paketi ve review modları, KiCad 10 otomasyonu.
- **Öz-inceleme döngüsü:** `scripts/review.py` ERC + DRC çalıştırır ve şematik/PCB/3D görüntüleri üretir.
- **Hesaplayıcılar:** `scripts/pcb_calc.py` (IPC-2221 iz genişliği, via akımı, I2C pull-up, LED direnci, bölücü, kristal yük kondansatörü, LDO ısıl hesabı, buck indüktörü, yay geometrisi).
- **Ders kaydı:** `references/16-dersler.md` her projede büyür.

## Kurulum

```bash
git clone https://github.com/recepuysal/claude-pcb-design-skill ~/.claude/skills/pcb-design
```
Şematik/PCB işi istediğinde Claude Code skill'i otomatik yükler. Elle çağırmak için `/pcb-design` yazılır.

## Lisans

MIT
