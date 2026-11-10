"""Check cad/export/impeller.stl (binary) and impeller.step share the model frame:
axis on Z (X/Y bounds symmetric about 0), back face at Z = 0. Pure Python, no SolidWorks."""
import os
import re
import struct

EXP = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "export")

with open(os.path.join(EXP, "impeller.stl"), "rb") as f:
    f.read(80)
    n = struct.unpack("<I", f.read(4))[0]
    lo, hi = [1e9] * 3, [-1e9] * 3
    vol = 0.0
    for _ in range(n):
        d = struct.unpack("<12fH", f.read(50))
        v = [d[3:6], d[6:9], d[9:12]]
        for p in v:
            for i in range(3):
                lo[i] = min(lo[i], p[i]); hi[i] = max(hi[i], p[i])
        a, b, c = v
        vol += (a[0] * (b[1] * c[2] - b[2] * c[1]) - a[1] * (b[0] * c[2] - b[2] * c[0]) + a[2] * (b[0] * c[1] - b[1] * c[0])) / 6
print(f"STL triangles {n}; bounds x {lo[0]:.4f}..{hi[0]:.4f} y {lo[1]:.4f}..{hi[1]:.4f} z {lo[2]:.4f}..{hi[2]:.4f} mm; volume {vol:.1f} mm^3")

txt = open(os.path.join(EXP, "impeller.step"), encoding="latin-1").read()
unit = "mm" if "SI_UNIT(.MILLI.,.METRE.)" in txt.replace(" ", "") else "check units"
pts = [tuple(float(x) for x in m.groups()) for m in re.finditer(
    r"CARTESIAN_POINT\s*\(\s*'[^']*'\s*,\s*\(\s*([-\d.E+]+)\s*,\s*([-\d.E+]+)\s*,\s*([-\d.E+]+)\s*\)", txt)]
# control points of curved surfaces can lie outside the solid; vertices are tighter but this is enough for the frame check
zs = [p[2] for p in pts]; xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
print(f"STEP ({unit}) {len(pts)} cartesian points; x {min(xs):.4f}..{max(xs):.4f} y {min(ys):.4f}..{max(ys):.4f} z {min(zs):.4f}..{max(zs):.4f}")
