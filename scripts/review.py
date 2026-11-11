#!/usr/bin/env python3
"""KiCad projesi için otomatik review paketi.

ERC + DRC (JSON) çalıştırır, şematik ve PCB görüntülerini üretir, özet yazar.
Çıktıdaki PNG'leri Read ile açıp 12-kontrol-listeleri.md'ye göre incele.

Kullanım:
  python review.py proje.kicad_pro [--out review_klasoru] [--dpi 150] [--no-3d]

Gereksinim: KiCad 10 (kicad-cli), görüntü için PyMuPDF (pip install pymupdf).
"""
import argparse
import json
import os
import shutil
import subprocess
import sys
from collections import Counter
from pathlib import Path

DEFAULT_CLI = [
    r"C:\Program Files\KiCad\10.0\bin\kicad-cli.exe",
    r"C:\Program Files\KiCad\9.0\bin\kicad-cli.exe",
    "/usr/bin/kicad-cli",
    "/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli",
]

PCB_VIEWS = {
    "pcb_top": "F.Cu,F.Silkscreen,F.Mask,Edge.Cuts",
    "pcb_bottom": "B.Cu,B.Silkscreen,Edge.Cuts",
    "pcb_silk_top": "F.Silkscreen,F.Fab,Edge.Cuts",
    "pcb_assembly_top": "F.Fab,F.Courtyard,Edge.Cuts",
    "pcb_copper_both": "F.Cu,B.Cu,Edge.Cuts",
}


def find_cli():
    env = os.environ.get("KICAD_CLI")
    if env and Path(env).exists():
        return env
    for c in DEFAULT_CLI:
        if Path(c).exists():
            return c
    w = shutil.which("kicad-cli")
    if w:
        return w
    sys.exit("kicad-cli bulunamadı. KICAD_CLI ortam değişkenini ayarla.")


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode not in (0, 5):  # 5 = violations exist (exit-code-violations)
        print(f"  ! komut hata verdi ({r.returncode}): {' '.join(cmd[:4])} ...\n{r.stderr.strip()[:500]}")
    return r


def pdf_to_png(pdf, out_prefix, dpi):
    try:
        import pymupdf as fitz
    except ImportError:
        try:
            import fitz
        except ImportError:
            print("  PyMuPDF yok; PNG üretilmedi (pip install pymupdf).")
            return []
    outs = []
    doc = fitz.open(pdf)
    for i, page in enumerate(doc):
        pix = page.get_pixmap(dpi=dpi)
        p = f"{out_prefix}_{i + 1}.png" if len(doc) > 1 else f"{out_prefix}.png"
        pix.save(p)
        outs.append(p)
    return outs


def summarize(report_path, kind):
    if not Path(report_path).exists():
        return f"{kind}: rapor yok"
    data = json.loads(Path(report_path).read_text(encoding="utf-8"))
    items = []
    if kind == "ERC":
        for sheet in data.get("sheets", []):
            for v in sheet.get("violations", []):
                v["_sheet"] = sheet.get("path", "")
                items.append(v)
    else:
        items = data.get("violations", []) + data.get("unconnected_items", []) + data.get("schematic_parity", [])
    sev = Counter(v.get("severity", "?") for v in items)
    typ = Counter(v.get("type", "?") for v in items)
    lines = [f"{kind}: toplam {len(items)}  " + ", ".join(f"{k}={n}" for k, n in sev.most_common())]
    for t, n in typ.most_common(15):
        lines.append(f"   - {t}: {n}")
    if kind == "DRC":
        lines.append(f"   unconnected_items: {len(data.get('unconnected_items', []))}, "
                     f"schematic_parity: {len(data.get('schematic_parity', []))}")
    for v in [x for x in items if x.get("severity") == "error"][:20]:
        refs = "; ".join(i.get("description", "") for i in v.get("items", [])[:2])
        lines.append(f"   * [{v.get('type')}] {v.get('description')} :: {refs}")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("project", help=".kicad_pro dosyası")
    ap.add_argument("--out", default=None, help="çıktı klasörü (varsayılan: <proje>/review)")
    ap.add_argument("--dpi", type=int, default=150)
    ap.add_argument("--no-3d", action="store_true")
    a = ap.parse_args()

    pro = Path(a.project).resolve()
    sch = pro.with_suffix(".kicad_sch")
    pcb = pro.with_suffix(".kicad_pcb")
    out = Path(a.out) if a.out else pro.parent / "review"
    out.mkdir(parents=True, exist_ok=True)
    cli = find_cli()
    summary = [f"Proje: {pro.name}", f"Çıktı: {out}", ""]

    if sch.exists():
        print("ERC ...")
        run([cli, "sch", "erc", "--format", "json", "--severity-all", "-o", str(out / "erc.json"), str(sch)])
        summary.append(summarize(out / "erc.json", "ERC"))
        print("Şematik PDF ...")
        run([cli, "sch", "export", "pdf", "-o", str(out / "schematic.pdf"), str(sch)])
        pngs = pdf_to_png(out / "schematic.pdf", str(out / "schematic"), a.dpi)
        summary.append("Şematik görüntüleri: " + ", ".join(Path(p).name for p in pngs))
    else:
        summary.append("Şematik bulunamadı.")

    if pcb.exists():
        print("DRC ...")
        run([cli, "pcb", "drc", "--format", "json", "--severity-all", "--schematic-parity",
             "-o", str(out / "drc.json"), str(pcb)])
        summary.append(summarize(out / "drc.json", "DRC"))
        for name, layers in PCB_VIEWS.items():
            pdf = out / f"{name}.pdf"
            cmd = [cli, "pcb", "export", "pdf", "--mode-single", "-l", layers, "--scale", "0", "-o", str(pdf), str(pcb)]
            if "bottom" in name:
                cmd.insert(-1, "--mirror")
            run(cmd)
            if pdf.exists():
                pdf_to_png(pdf, str(out / name), a.dpi * 2)
        if not a.no_3d:
            print("3D render ...")
            run([cli, "pcb", "render", "--side", "top", "--quality", "high", "-o", str(out / "3d_top.png"), str(pcb)])
            run([cli, "pcb", "render", "--rotate", "-45,0,45", "--perspective", "--quality", "high",
                 "-o", str(out / "3d_iso.png"), str(pcb)])
            run([cli, "pcb", "render", "--side", "bottom", "-o", str(out / "3d_bottom.png"), str(pcb)])
        summary.append("PCB görüntüleri: " + ", ".join(sorted(p.name for p in out.glob("pcb_*.png"))))
    else:
        summary.append("PCB bulunamadı.")

    text = "\n".join(summary)
    (out / "SUMMARY.txt").write_text(text, encoding="utf-8")
    print("\n" + text)


if __name__ == "__main__":
    main()
