# pcb-design — Claude Code Skill for Professional Schematic & PCB Design

🇹🇷 [Türkçe README](README.tr.md)

A [Claude Code](https://claude.com/claude-code) skill that turns Claude into a disciplined hardware design assistant: requirements → architecture → schematic → placement → routing → review → JLCPCB manufacturing outputs, with phase gates and checklists at every step.

The skill content is written **in Turkish (primary)** with English technical terms.

## Highlights

- **Phase-gated workflow** with measurable rules (e.g. "decoupling ≤ 2 mm from pin", "1 A → ≥ 0.5 mm trace").
- **JLCPCB-first:** fabrication limits vs. comfortable defaults, 2-layer stackup, net classes, Basic/Extended part strategy, BOM/CPL format.
- **Topic guides:** power & Li-ion charging (TP4056, buck/boost, USB-C sink), MCUs (STM32, ESP32-S3, RP2040, crystals), motor drivers (DRV8833, TMC2209, MOSFET switches), interfaces (I2C, SPI, UART, USB, RS-485, CAN, ESD).
- **House style:** boxed functional blocks in schematics, smooth (arc) tracks + teardrops on PCBs.
- **Tool support:** EasyEDA (Pro) design-pack / review modes, KiCad 10 automation.
- **Self-review loop:** `scripts/review.py` runs ERC + DRC, renders schematic/PCB/3D images for visual checking.
- **Calculators:** `scripts/pcb_calc.py` (IPC-2221 trace width, via current, I2C pull-ups, LED resistor, divider, crystal load caps, LDO thermal, buck inductor, fillet geometry).
- **Lessons log:** `references/16-dersler.md` grows with every project.

## Install

```bash
git clone https://github.com/recepuysal/claude-pcb-design-skill ~/.claude/skills/pcb-design
```
Claude Code loads it automatically when you ask for schematic/PCB work.

## Layout

```
SKILL.md                     entry point & workflow
references/00..16-*.md       rules, checklists, topic guides
scripts/pcb_calc.py          calculators
scripts/review.py            KiCad ERC/DRC/render review pack
```

## Requirements

- KiCad 10 (`kicad-cli`) for automated review; Python 3.10+, `pymupdf` for PNG rendering.

## License

MIT
