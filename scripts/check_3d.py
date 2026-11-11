#!/usr/bin/env python3
"""3D model <-> footprint hizalama kontrolu (VRML modeller icin).

Her footprint icin: model dosyasindaki noktalari okur, footprint'teki (rotate/offset/scale)
donusumunu uygular ve modelin XY sinir kutusunu pad'lerin sinir kutusuyla karsilastirir.
Supheli durumlar: merkez kaymasi > 0.25 mm, model uzun ekseni pad ekseninden farkli (90° hata),
model pad'leri kapsamiyor ya da cok tasiyor.

Kullanim:  python check_3d.py <footprint.pretty klasoru> [--proj <KIPRJMOD klasoru>]
Not: KiCad VRML birimi 1 = 0.1 inc = 2.54 mm. 3D eksende y yukari, footprint'te y asagi.
"""
import argparse
import math
import os
import re


def sexp_num(s, key):
    m = re.search(r"\(%s\s+\(xyz\s+([-\d.e]+)\s+([-\d.e]+)\s+([-\d.e]+)\s*\)" % key, s)
    return tuple(float(v) for v in m.groups()) if m else (0.0, 0.0, 0.0) if key != "scale" else (1, 1, 1)


def pads_bbox(t):
    xs, ys = [], []
    for m in re.finditer(r'\(pad\s+(?:"[^"]*"|\S+)\s+(\w+)\s+(\w+)\s*\(at\s+([-\d.]+)\s+([-\d.]+)(?:\s+([-\d.]+))?\)\s*\(size\s+([-\d.]+)\s+([-\d.]+)\)', t):
        kind, x, y, rot, w, h = m.group(1), float(m.group(3)), float(m.group(4)), float(m.group(5) or 0), float(m.group(6)), float(m.group(7))
        if kind == "np_thru_hole" or w < 0.05:
            continue
        if int(round(rot)) % 180 == 90:
            w, h = h, w
        xs += [x - w / 2, x + w / 2]
        ys += [y - h / 2, y + h / 2]
    return (min(xs), min(ys), max(xs), max(ys)) if xs else None


def wrl_points(path):
    txt = open(path, encoding="utf-8", errors="ignore").read()
    pts = []
    for blk in re.findall(r"point\s*\[([^\]]*)\]", txt):
        nums = [float(v) for v in re.findall(r"[-\d.eE+]+", blk)]
        pts += [nums[i:i + 3] for i in range(0, len(nums) - 2, 3)]
    return pts


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pretty")
    ap.add_argument("--proj", default=None, help="${KIPRJMOD} degeri (varsayilan: .pretty'nin 2 ust klasoru)")
    a = ap.parse_args()
    proj = a.proj or os.path.dirname(os.path.dirname(os.path.abspath(a.pretty)))
    print(f"{'footprint':40} {'pad kutusu (WxH)':>17} {'model kutusu (WxH)':>19} {'merkez farki':>13}  durum")
    for f in sorted(os.listdir(a.pretty)):
        if not f.endswith(".kicad_mod"):
            continue
        t = open(os.path.join(a.pretty, f), encoding="utf-8").read()
        mm = re.search(r'\(model\s+"([^"]+)"(.*?\(rotate\s+\(xyz[^)]*\)\s*\))', t, re.S)
        pb = pads_bbox(t)
        name = f[:-10]
        if not mm or not pb:
            print(f"{name:40} model/pad yok")
            continue
        mpath = mm.group(1).replace("${KIPRJMOD}", proj)
        if not mpath.lower().endswith(".wrl") or not os.path.exists(mpath):
            print(f"{name:40} {'':>17} {'(STEP/eksik: gorsel kontrol)':>19}")
            continue
        body = mm.group(0)
        off, rot, sc = sexp_num(body, "offset"), sexp_num(body, "rotate"), sexp_num(body, "scale")
        rz = math.radians(rot[2])
        pts = wrl_points(mpath)
        X, Y = [], []
        for x, y, z in pts:
            x, y = x * 2.54 * sc[0], y * 2.54 * sc[1]
            xr = x * math.cos(rz) - y * math.sin(rz)
            yr = x * math.sin(rz) + y * math.cos(rz)
            X.append(xr + off[0])
            Y.append(-(yr + off[1]))          # 3D y yukari -> footprint y asagi
        mb = (min(X), min(Y), max(X), max(Y))
        pw, ph = pb[2] - pb[0], pb[3] - pb[1]
        mw, mh = mb[2] - mb[0], mb[3] - mb[1]
        dx = (mb[0] + mb[2]) / 2 - (pb[0] + pb[2]) / 2
        dy = (mb[1] + mb[3]) / 2 - (pb[1] + pb[3]) / 2
        issues = []
        if math.hypot(dx, dy) > 0.25:
            issues.append("MERKEZ KAYIK")
        if (pw - ph) * (mw - mh) < 0 and abs(pw - ph) > 0.3 and abs(mw - mh) > 0.3:
            issues.append("90° DONUK")
        if mw < 0.4 * pw or mh < 0.4 * ph:
            issues.append("MODEL KUCUK")
        if mw > 1.6 * pw + 1 or mh > 1.6 * ph + 1:
            issues.append("MODEL BUYUK")
        print(f"{name:40} {pw:7.2f}x{ph:<7.2f}  {mw:7.2f}x{mh:<7.2f}   ({dx:+.2f},{dy:+.2f})  "
              f"{', '.join(issues) or 'ok'}  [rot={rot[2]:g}]")


if __name__ == "__main__":
    main()
