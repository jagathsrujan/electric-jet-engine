"""Measure impeller draft 2 from the built SolidWorks model (open cad/impeller.SLDPRT first,
or run right after build_impeller.py). Prints every check; nothing here is hand-computed input
except the PLA density 1250 kg/m^3 (interp.)."""
import math
import types

import pythoncom
import win32com.client

NOTHING = win32com.client.VARIANT(pythoncom.VT_DISPATCH, None)
RHO_PLA = 1250.0  # kg/m^3 (interp.)


def G(obj, name, *a):
    v = getattr(obj, name)
    return v(*a) if isinstance(v, types.MethodType) else v


app = win32com.client.GetActiveObject("SldWorks.Application")
doc = app.ActiveDoc
print("doc", doc.GetTitle)
ext = doc.Extension

# ---- mass properties ----
mp = ext.CreateMassProperty
vol = mp.Volume * 1e9
com = [v * 1e3 for v in mp.CenterOfMass]
print(f"volume {vol:.1f} mm^3; mass at PLA {RHO_PLA} kg/m3 = {mp.Volume * RHO_PLA * 1e3:.2f} g")
print(f"centre of mass mm: x {com[0]:.3e} y {com[1]:.3e} z {com[2]:.4f}; radial offset {math.hypot(com[0], com[1]):.3e} mm")
dens = mp.Mass / mp.Volume
Iz = mp.GetMomentOfInertia(0)   # 3x3 at centre of mass, SW density
print(f"SW density {dens:.0f} kg/m3; Izz at PLA = {Iz[8] * RHO_PLA / dens:.3e} kg m^2")

# ---- bounding box ----
body = doc.GetBodies2(0, False)[0]
bb = [v * 1e3 for v in G(body, "GetBodyBox")]
print("body box mm", [round(v, 4) for v in bb])

# ---- blade faces: cylinders that are not coaxial with Z ----
cyl = []
fillet_faces = 0
for f in G(body, "GetFaces"):
    s = G(f, "GetSurface")
    if G(s, "IsCylinder"):
        p = G(s, "CylinderParams")
        o, a, r = p[0:3], p[3:6], p[6]
        if math.hypot(o[0], o[1]) > 1e-4 and r > 0.01:  # off-axis, R>10 mm = blade side face (fillet cylinders are R 1)
            cyl.append((o[0] * 1e3, o[1] * 1e3, r * 1e3, f))
    if G(s, "IsTorus") or (not G(s, "IsPlane") and not G(s, "IsCylinder")):
        fillet_faces += 1
print("off-axis cylindrical faces (blade sides):", len(cyl))
# group by centre
groups = {}
for x, y, r, f in cyl:
    key = (round(x, 3), round(y, 3))
    groups.setdefault(key, []).append(r)
print("distinct arc centres:", len(groups))


def angle_from_tangent(c, R, r):
    d = math.hypot(*c)
    return math.degrees(math.acos((r * r + R * R - d * d) / (2 * r * R)))


res = []
for k, rs in sorted(groups.items(), key=lambda kv: math.atan2(kv[0][1], kv[0][0])):
    rs = sorted(set(round(v, 4) for v in rs))
    Rc = sum(rs) / len(rs)
    res.append((k, rs, Rc, angle_from_tangent(k, Rc, 24.0), angle_from_tangent(k, Rc, 50.0)))
for k, rs, Rc, b1, b2 in res:
    print(f"  centre ({k[0]:8.3f},{k[1]:8.3f}) |c|={math.hypot(*k):.4f} side radii {rs} -> "
          f"centreline R {Rc:.4f}, beta at r24 {b1:.3f} deg, at r50 {b2:.3f} deg, thickness {rs[-1]-rs[0]:.3f}")

# ---- non-planar, non-cylindrical faces counted as fillet faces ----
print("faces that are neither plane nor cylinder (fillets etc.):", fillet_faces)

# ---- fillet faces: R 1 mm cylinders (along straight root edges) + tori (along arc root edges) ----
n_c1 = n_tor = 0
for f in G(body, "GetFaces"):
    srf = G(f, "GetSurface")
    if G(srf, "IsCylinder") and abs(G(srf, "CylinderParams")[6] - 1e-3) < 1e-7:
        n_c1 += 1
    if G(srf, "IsTorus"):
        tp = G(srf, "TorusParams")
        n_tor += 1
        tmin = tp[8] * 1e3 if len(tp) > 8 else None
print(f"fillet faces: {n_c1} R1 cylinders, {n_tor} tori (minor radius {tmin} mm)")

# ---- leading edge and taper: vertical straight edges with r < 31 mm (blade corners) ----
vert = []
for e in G(body, "GetEdges"):
    if not G(G(e, "GetCurve"), "IsLine"):
        continue
    cp = G(e, "GetCurveParams2")
    s, t = [v * 1e3 for v in cp[0:3]], [v * 1e3 for v in cp[3:6]]
    if math.hypot(s[0] - t[0], s[1] - t[1]) < 1e-6 and 20 < math.hypot(s[0], s[1]) < 31:
        vert.append((s[0], s[1], min(s[2], t[2]), max(s[2], t[2])))
print("vertical blade-corner edges r<31:", len(vert))
# blade nearest +X axis: corners with angle in (-25, 5) deg
b = sorted([v for v in vert if -25 < math.degrees(math.atan2(v[1], v[0])) < 5], key=lambda v: math.hypot(v[0], v[1]))
for v in b:
    print(f"  corner x {v[0]:.4f} y {v[1]:.4f} r {math.hypot(v[0], v[1]):.4f} z {v[2]:.3f}..{v[3]:.3f}")
if len(b) == 4:
    le = sorted(b, key=lambda v: math.hypot(v[0], v[1]))
    # LE corners: the two with the smallest distance to (24,0)
    by_le = sorted(b, key=lambda v: math.hypot(v[0] - 24, v[1]))
    l1, l2, t1, t2 = by_le
    w_le = math.hypot(l1[0] - l2[0], l1[1] - l2[1])
    w_t = math.hypot(t1[0] - t2[0], t1[1] - t2[1])
    m_le = ((l1[0] + l2[0]) / 2, (l1[1] + l2[1]) / 2)
    m_t = ((t1[0] + t2[0]) / 2, (t1[1] + t2[1]) / 2)
    chord = math.dist(m_le, m_t)
    print(f"LE width {w_le:.4f} mm, LE midpoint r {math.hypot(*m_le):.4f}; thickness at taper end {w_t:.4f} mm; "
          f"taper chord length {chord:.4f} mm (arc length = 2 R asin(c/2R) = {2*61.3*math.asin(chord/2/61.3):.4f})")
    print("LE corner heights:", [(round(v[2], 3), round(v[3], 3)) for v in (l1, l2)])

# ---- rotation sense: where the blade near +X meets r = 50 (vertical edges on the rim) ----
rim = []
for e in G(body, "GetEdges"):
    if not G(G(e, "GetCurve"), "IsLine"):
        continue
    cp = G(e, "GetCurveParams2")
    s, t = [v * 1e3 for v in cp[0:3]], [v * 1e3 for v in cp[3:6]]
    if math.hypot(s[0] - t[0], s[1] - t[1]) < 1e-6 and abs(math.hypot(s[0], s[1]) - 50) < 0.05:
        a = math.degrees(math.atan2(s[1], s[0]))
        if -70 < a < -20:
            rim.append(round(a, 3))
print("blade starting at LE angle 0 deg (r 24) reaches r 50 at polar angles", sorted(set(rim)),
      "deg -> negative = clockwise seen from +Z, i.e. trailing a counter-clockwise rotation (backward-curved)")
