#!/usr/bin/env python3
"""PCB / devre hesap araçları (PCB design calculators).

Örnekler:
  python pcb_calc.py trace --amps 2 [--oz 1] [--dt 10] [--internal]
  python pcb_calc.py via --drill 0.3 [--plating-um 20]
  python pcb_calc.py i2c --vdd 3.3 --cb 100 [--speed 400]
  python pcb_calc.py led --vdd 3.3 --vf 2.0 --ma 2
  python pcb_calc.py divider --vref 0.6 --vout 5 [--rbot 10000]
  python pcb_calc.py xtal --cl 10 [--cstray 4]
  python pcb_calc.py ldo --vin 5 --vout 3.3 --amps 0.3 [--theta 200] [--ta 40]
  python pcb_calc.py buck --vin 12 --vout 5 --amps 2 --fsw 500e3 [--ripple 0.3]
  python pcb_calc.py fillet --radius 1.0 --angle 90
"""
import argparse
import math

E24 = [1.0, 1.1, 1.2, 1.3, 1.5, 1.6, 1.8, 2.0, 2.2, 2.4, 2.7, 3.0, 3.3, 3.6, 3.9, 4.3,
       4.7, 5.1, 5.6, 6.2, 6.8, 7.5, 8.2, 9.1]
E96 = [round(10 ** (i / 96), 2) for i in range(96)]


def nearest(value, series=E24):
    if value <= 0:
        return value
    exp = math.floor(math.log10(value))
    best = None
    for e in (exp - 1, exp, exp + 1):
        for b in series:
            c = b * 10 ** e
            if best is None or abs(c - value) < abs(best - value):
                best = c
    return best


def fmt_r(r):
    if r >= 1e6:
        return f"{r / 1e6:.3g}M"
    if r >= 1e3:
        return f"{r / 1e3:.3g}k"
    return f"{r:.3g}R"


def cmd_trace(a):
    k = 0.024 if a.internal else 0.048
    area_mil2 = (a.amps / (k * a.dt ** 0.44)) ** (1 / 0.725)
    thick_mil = 1.378 * a.oz
    w_mil = area_mil2 / thick_mil
    w_mm = w_mil * 0.0254
    rec = max(0.25, math.ceil(w_mm * 1.5 / 0.05) * 0.05)
    print(f"IPC-2221 ({'iç' if a.internal else 'dış'} katman, {a.oz} oz, ΔT={a.dt}°C, {a.amps} A)")
    print(f"  Minimum genişlik : {w_mm:.3f} mm ({w_mil:.1f} mil)")
    print(f"  Önerilen (x1.5)  : {rec:.2f} mm")
    if rec > 3:
        print("  Not: >3 mm ise polygon/döküm, 2 oz ya da iki katmanda paralel yol düşün.")


def cmd_via(a):
    # Via barrel = halka kesitli iletken; IPC-2221 iç katman katsayısı ile muhafazakâr tahmin
    d_mil = a.drill / 0.0254
    t_mil = a.plating_um / 25.4
    area = math.pi * ((d_mil / 2 + t_mil) ** 2 - (d_mil / 2) ** 2)
    i = 0.048 * a.dt ** 0.44 * area ** 0.725
    print(f"Via {a.drill} mm delik, {a.plating_um} µm kaplama: kesit {area:.1f} mil² → ~{i:.2f} A (ΔT={a.dt}°C, kaba tahmin)")
    print("  Pratik kural: 0.3 mm via ≈ 1 A; güç geçişinde ≥2 via ve her 1 A için ≥1 via kullan.")


def cmd_i2c(a):
    tr = {100: 1000e-9, 400: 300e-9, 1000: 120e-9}[a.speed]
    rmin = (a.vdd - 0.4) / 3e-3
    rmax = tr / (0.8473 * a.cb * 1e-12)
    print(f"I2C {a.speed} kHz, VDD={a.vdd} V, Cb={a.cb} pF")
    print(f"  Rmin = {fmt_r(rmin)}   Rmax = {fmt_r(rmax)}")
    if rmax < rmin:
        print("  UYARI: Rmax < Rmin → hat kapasitesi çok yüksek; hızı düşür ya da buffer kullan.")
    else:
        cands = [r for r in (1e3, 1.5e3, 2.2e3, 3.3e3, 4.7e3, 10e3) if rmin <= r <= rmax]
        print(f"  Uygun standart değerler: {', '.join(fmt_r(r) for r in cands) or 'yok'}")


def cmd_led(a):
    r = (a.vdd - a.vf) / (a.ma / 1000)
    rn = nearest(r)
    p = (a.ma / 1000) ** 2 * rn
    print(f"R = {fmt_r(r)} → E24: {fmt_r(rn)}  (I = {(a.vdd - a.vf) / rn * 1000:.2f} mA, P = {p * 1000:.1f} mW)")


def cmd_divider(a):
    rbot = a.rbot
    rtop = rbot * (a.vout / a.vref - 1)
    for name, series in (("E24", E24), ("E96", E96)):
        rt = nearest(rtop, series)
        v = a.vref * (1 + rt / rbot)
        print(f"{name}: Rtop = {fmt_r(rt)}, Rbot = {fmt_r(rbot)} → Vout = {v:.3f} V ({(v / a.vout - 1) * 100:+.2f}%)")
    print(f"Bölücü akımı ≈ {a.vout / (rtop + rbot) * 1e6:.1f} µA")


def cmd_xtal(a):
    c = 2 * (a.cl - a.cstray)
    print(f"C1 = C2 = 2 × (CL − Cstray) = 2 × ({a.cl} − {a.cstray}) = {c:.1f} pF → E24: {nearest(c):.3g} pF (C0G)")


def cmd_ldo(a):
    p = (a.vin - a.vout) * a.amps
    tj = a.ta + p * a.theta
    print(f"Kayıp P = ({a.vin} − {a.vout}) × {a.amps} = {p:.3f} W")
    print(f"Tj = {a.ta} + {p:.3f} × {a.theta} = {tj:.1f} °C  ({'OK' if tj < 100 else 'FAZLA — paketi büyüt / buck kullan'})")
    print(f"Verim ≈ {a.vout / a.vin * 100:.0f}%")


def cmd_buck(a):
    d = a.vout / a.vin
    dil = a.ripple * a.amps
    L = (a.vin - a.vout) * d / (a.fsw * dil)
    ipk = a.amps + dil / 2
    print(f"D = {d:.3f}, ΔIL = {dil:.3f} A")
    print(f"L = {L * 1e6:.2f} µH (en yakın standart değeri seç: 2.2/3.3/4.7/6.8/10/15/22 µH)")
    print(f"Ipeak = {ipk:.2f} A → Isat ≥ {ipk * 1.2:.2f} A, Irms ≥ {a.amps:.2f} A")
    for cout in (22e-6, 44e-6):
        print(f"Cout {cout * 1e6:.0f} µF (ideal seramik) → ripple ≈ {dil / (8 * a.fsw * cout) * 1000:.1f} mV")


def cmd_fillet(a):
    th = math.radians(a.angle)
    d = a.radius * math.tan(th / 2)
    print(f"Yarıçap {a.radius} mm, köşe dönüşü {a.angle}°: yay her iki segmentten {d:.3f} mm geri kesilir.")
    print(f"Yay uzunluğu = {a.radius * th:.3f} mm")


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    s = p.add_subparsers(dest="cmd", required=True)
    t = s.add_parser("trace"); t.add_argument("--amps", type=float, required=True); t.add_argument("--oz", type=float, default=1)
    t.add_argument("--dt", type=float, default=10); t.add_argument("--internal", action="store_true"); t.set_defaults(f=cmd_trace)
    v = s.add_parser("via"); v.add_argument("--drill", type=float, default=0.3); v.add_argument("--plating-um", type=float, default=20)
    v.add_argument("--dt", type=float, default=10); v.set_defaults(f=cmd_via)
    i = s.add_parser("i2c"); i.add_argument("--vdd", type=float, default=3.3); i.add_argument("--cb", type=float, default=100)
    i.add_argument("--speed", type=int, choices=[100, 400, 1000], default=100); i.set_defaults(f=cmd_i2c)
    l = s.add_parser("led"); l.add_argument("--vdd", type=float, required=True); l.add_argument("--vf", type=float, default=2.0)
    l.add_argument("--ma", type=float, default=2); l.set_defaults(f=cmd_led)
    dv = s.add_parser("divider"); dv.add_argument("--vref", type=float, required=True); dv.add_argument("--vout", type=float, required=True)
    dv.add_argument("--rbot", type=float, default=10000); dv.set_defaults(f=cmd_divider)
    x = s.add_parser("xtal"); x.add_argument("--cl", type=float, required=True); x.add_argument("--cstray", type=float, default=4)
    x.set_defaults(f=cmd_xtal)
    d = s.add_parser("ldo"); d.add_argument("--vin", type=float, required=True); d.add_argument("--vout", type=float, required=True)
    d.add_argument("--amps", type=float, required=True); d.add_argument("--theta", type=float, default=200, help="θJA °C/W (SOT-23-5≈200, SOT-223≈80)")
    d.add_argument("--ta", type=float, default=40); d.set_defaults(f=cmd_ldo)
    b = s.add_parser("buck"); b.add_argument("--vin", type=float, required=True); b.add_argument("--vout", type=float, required=True)
    b.add_argument("--amps", type=float, required=True); b.add_argument("--fsw", type=float, required=True)
    b.add_argument("--ripple", type=float, default=0.3); b.set_defaults(f=cmd_buck)
    fl = s.add_parser("fillet"); fl.add_argument("--radius", type=float, required=True); fl.add_argument("--angle", type=float, default=90)
    fl.set_defaults(f=cmd_fillet)
    a = p.parse_args()
    a.f(a)


if __name__ == "__main__":
    main()
