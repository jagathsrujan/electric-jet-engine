"""Build impeller draft 2 in a running SolidWorks session (pywin32, late binding).

Run with the Solidworks-MCP venv interpreter:
  "C:\\Users\\jagath srujan\\mcp-servers\\Solidworks-MCP\\.venv\\Scripts\\python.exe" cad\\scripts\\build_impeller.py
Creates a new part, builds it, saves cad/impeller.SLDPRT (overwrites).
Then run export_impeller.py and check_impeller.py.

Coordinates: axis on Z, back face of the back plate at Z = 0, blades towards +Z (inlet side).
Rotation: counter-clockwise viewed from +Z (inlet side). Blades curve backward (clockwise going out).
All API lengths are metres; parameters below are mm (from docs/parameters.md section 3).
"""
import math
import types
import os
import sys

import pythoncom
import win32com.client

sys.path.insert(0, os.path.dirname(__file__))
from blade_geometry import P, centre, point_at_radius  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
CAD = os.path.dirname(HERE)
OUT_PART = os.path.join(CAD, "impeller.SLDPRT")
M = 1e-3
NOTHING = win32com.client.VARIANT(pythoncom.VT_DISPATCH, None)


def G(obj, name):
    """Late-bound COM members are sometimes properties, sometimes methods."""
    v = getattr(obj, name)
    return v() if isinstance(v, types.MethodType) else v


def log(*a):
    print(*a, flush=True)


app = win32com.client.GetActiveObject("SldWorks.Application")
app.SetUserPreferenceToggle(10, False)   # swInputDimValOnCreate: no modify dialog
for d in list(app.GetDocuments or []):
    if d.GetTitle.lower().startswith(("impeller", "part")):
        app.CloseDoc(d.GetTitle)
tmpl = app.GetUserPreferenceStringValue(8)
doc = app.NewDocument(tmpl, 0, 0.0, 0.0)
assert doc is not None, "NewDocument failed"
ext = doc.Extension
sm = doc.SketchManager
fm = doc.FeatureManager
sm.AddToDB = True
sm.DisplayWhenAdded = False
log("template", tmpl, "length unit", doc.LengthUnit)


def sel(name, kind, append=False, mark=0):
    ok = ext.SelectByID2(name, kind, 0.0, 0.0, 0.0, append, mark, NOTHING, 0)
    if not ok:
        raise RuntimeError(f"select failed: {name} {kind}")


def open_sketch(plane):
    doc.ClearSelection2(True)
    sel(plane, "PLANE")
    sm.InsertSketch(True)


def close_sketch():
    sm.InsertSketch(True)
    return doc.FeatureByPositionReverse(0)  # the sketch just closed


def last_feature():
    return doc.FeatureByPositionReverse(0)


def dim_on(seg, x, y):
    """Add a dimension to a sketch segment (sketch open); return its 'Dn' name."""
    doc.ClearSelection2(True)
    seg.Select4(False, NOTHING)
    dd = doc.AddDimension2(x * M, y * M, 0.0)
    return dd.GetDimension2(0).Name


def extrude(depth_mm, cut=False, flip=False):
    if cut:
        f = fm.FeatureCut4(True, False, flip, 0, 0, depth_mm * M, 0.0,
                           False, False, False, False, 0.0, 0.0,
                           False, False, False, False, False, True, True,
                           False, True, False, 0, 0.0, False, False)
    else:
        f = fm.FeatureExtrusion3(True, False, flip, 0, 0, depth_mm * M, 0.0,
                                 False, False, False, False, 0.0, 0.0,
                                 False, False, False, False, True, True, True, 0, 0.0, False)
    if f is None:
        raise RuntimeError("extrude/cut failed")
    return f


def mass():
    mp = ext.CreateMassProperty
    c = mp.CenterOfMass
    return mp.Volume * 1e9, [v * 1e3 for v in c]


eqs = []  # (lhs, rhs)

# ---------------- global variables ----------------
gv = dict(D2=P["D2"], t_bp=P["t_bp"], b1=P["b1"], b2=P["b2"], d_h=P["d_h"], d_bore=P["d_bore"],
          Z=P["Z"], r1=P["r1"], beta1b=P["beta1b"], beta2b=P["beta2b"], Rb=P["Rb"], t=P["t"],
          t_LE=P["t_LE"], L_taper=P["L_taper"], r_fil=P["r_fillet"], arrow_depth=0.4)
em = doc.GetEquationMgr
for k, v in gv.items():
    em.Add2(-1, f'"{k}" = {v}', True)

# ---------------- 1. back plate ----------------
open_sketch("Front Plane")
c_out = sm.CreateCircleByRadius(0, 0, 0, P["D2"] / 2 * M)
c_bore = sm.CreateCircleByRadius(0, 0, 0, P["d_bore"] / 2 * M)
n1, n2 = dim_on(c_out, 30, 45), dim_on(c_bore, 3, 3)
sk = close_sketch(); sk.Name = "SK_BackPlate"
eqs += [(f"{n1}@SK_BackPlate", '"D2"'), (f"{n2}@SK_BackPlate", '"d_bore"')]
doc.ClearSelection2(True); sel(sk.Name, "SKETCH")
f = extrude(P["t_bp"]); f.Name = "BackPlate"
eqs.append(("D1@BackPlate", '"t_bp"'))
log("plate", mass())

# ---------------- 2. hub boss ----------------
open_sketch("Front Plane")
c_hub = sm.CreateCircleByRadius(0, 0, 0, P["d_h"] / 2 * M)
c_bore2 = sm.CreateCircleByRadius(0, 0, 0, P["d_bore"] / 2 * M)
n1, n2 = dim_on(c_hub, 8, 8), dim_on(c_bore2, 2, -2)
sk = close_sketch(); sk.Name = "SK_Hub"
eqs += [(f"{n1}@SK_Hub", '"d_h"'), (f"{n2}@SK_Hub", '"d_bore"')]
doc.ClearSelection2(True); sel(sk.Name, "SKETCH")
f = extrude(P["t_bp"] + P["b1"]); f.Name = "Hub"
eqs.append(("D1@Hub", '"t_bp" + "b1"'))
log("hub", mass())

# ---------------- 3. seed blade ----------------
C = centre()
R = P["Rb"]
cx, cy = C
a1 = math.atan2(0 - cy, P["r1"] - cx)            # centreline angle about C at the leading edge
p_te = point_at_radius(C, R, P["D2"] / 2, (40, -30))
a2 = math.atan2(p_te[1] - cy, p_te[0] - cx)
sgn = 1 if (a2 - a1 + math.pi) % (2 * math.pi) - math.pi > 0 else -1   # sweep direction about C
aT = a1 + sgn * P["L_taper"] / R                 # end of leading-edge taper (8 mm along the centreline)
h, hLE = P["t"] / 2, P["t_LE"] / 2


def on(rad, ang):
    return (cx + rad * math.cos(ang), cy + rad * math.sin(ang))


LEp, LEm = on(R + hLE, a1), on(R - hLE, a1)
Tp, Tm = on(R + h, aT), on(R - h, aT)
Ep = point_at_radius(C, R + h, P["D2"] / 2, p_te)
Em = point_at_radius(C, R - h, P["D2"] / 2, p_te)
coords = dict(C=C, LE_centre=(P["r1"], 0.0), LE_plus=LEp, LE_minus=LEm, taper_end_plus=Tp,
              taper_end_minus=Tm, exit_plus=Ep, exit_minus=Em, TE_centre=p_te)
for k, v in coords.items():
    log(f"coord {k}: ({v[0]:.4f}, {v[1]:.4f}) r={math.hypot(*v):.4f}")

open_sketch("Front Plane")
L = lambda p, q: sm.CreateLine(p[0] * M, p[1] * M, 0, q[0] * M, q[1] * M, 0)  # noqa: E731
L(LEp, LEm)                       # leading edge, 0.8 mm
L(LEp, Tp)                        # taper flank, outer side
L(LEm, Tm)                        # taper flank, inner side
# CreateArc direction: 1 = counter-clockwise, -1 = clockwise (from start to end)
sm.CreateArc(cx * M, cy * M, 0, Tp[0] * M, Tp[1] * M, 0, Ep[0] * M, Ep[1] * M, 0, sgn)
sm.CreateArc(cx * M, cy * M, 0, Tm[0] * M, Tm[1] * M, 0, Em[0] * M, Em[1] * M, 0, sgn)
# exit edge on the D2 circle
ae, am_ = math.atan2(Ep[1], Ep[0]), math.atan2(Em[1], Em[0])
d_exit = 1 if (am_ - ae + math.pi) % (2 * math.pi) - math.pi > 0 else -1
sm.CreateArc(0, 0, 0, Ep[0] * M, Ep[1] * M, 0, Em[0] * M, Em[1] * M, 0, d_exit)
sk = close_sketch(); sk.Name = "SK_Blade"
doc.ClearSelection2(True); sel(sk.Name, "SKETCH")
f = extrude(P["t_bp"] + P["b1"]); f.Name = "Blade"
eqs.append(("D1@Blade", '"t_bp" + "b1"'))
v_blade = mass()
log("blade", v_blade)

# ---------------- 4. root fillet on the seed blade ----------------
body = doc.GetBodies2(0, False)[0]
zr = P["t_bp"] * M
root = []
for e in G(body, "GetEdges"):
    cp = G(e, "GetCurveParams2")
    s, t_ = cp[0:3], cp[3:6]
    if abs(s[2] - zr) > 1e-7 or abs(t_[2] - zr) > 1e-7:
        continue
    rs, rt = math.hypot(s[0], s[1]) / M, math.hypot(t_[0], t_[1]) / M
    if min(rs, rt) < 15 or (rs > 49.9 and rt > 49.9):
        continue
    root.append(e)
log("root edges found", len(root))
sd = doc.SelectionManager.CreateSelectData
fillet_note = "all root edges"


def try_fillet(edges):
    doc.ClearSelection2(True)
    for e in edges:
        e.Select4(True, sd)
    ff = fm.FeatureFillet(1 | 2, P["r_fillet"] * M, 0, 0, None, None, None)
    return ff if (ff is not None and ff.GetErrorCode == 0) else None


ff = try_fillet(root)
if ff is None:
    # retry without the 0.8 mm leading-edge edge (shortest)
    lens = []
    for e in root:
        cp = G(e, "GetCurveParams2")
        lens.append(math.dist(cp[0:3], cp[3:6]))
    keep = [e for e, l_ in zip(root, lens) if l_ > 1.0 * M]
    ff = try_fillet(keep)
    fillet_note = "root edges except the 0.8 mm leading-edge edge"
if ff is None:
    fillet_note = "FAILED"
else:
    ff.Name = "RootFillet"
    eqs.append(("D1@RootFillet", '"r_fil"'))
log("fillet:", fillet_note, mass())

# ---------------- 5. axis on Z and circular pattern ----------------
doc.ClearSelection2(True)
sel("Top Plane", "PLANE"); sel("Right Plane", "PLANE", True)
ok = doc.InsertAxis2(True)
ax = last_feature(); ax.Name = "Axis_Z"
log("axis", ok, ax.Name)
doc.ClearSelection2(True)
sel("Axis_Z", "AXIS", False, 1)
sel("Blade", "BODYFEATURE", True, 4)
if ff is not None:
    sel("RootFillet", "BODYFEATURE", True, 4)
pat = fm.FeatureCircularPattern4(int(P["Z"]), 2 * math.pi, False, "", False, True, False)
if pat is None:
    raise RuntimeError("circular pattern failed")
pat.Name = "BladePattern"
eqs.append(("D1@BladePattern", '"Z"'))
log("pattern", pat.GetErrorCode, mass())

# ---------------- 6. blade height taper (revolve cut) ----------------
# Top Plane sketch: sketch x = model X (radius), sketch y = -model Z
open_sketch("Top Plane")
zt, ze = P["t_bp"] + P["b1"], P["t_bp"] + P["b2"]
poly = [(20, zt), (P["r1"], zt), (P["D2"] / 2, ze), (P["D2"] / 2 + 5, ze), (P["D2"] / 2 + 5, zt + 10), (20, zt + 10)]
sm.CreateCenterLine(0, 0, 0, 0, -0.03, 0)
for i in range(len(poly)):
    p, q = poly[i], poly[(i + 1) % len(poly)]
    sm.CreateLine(p[0] * M, -p[1] * M, 0, q[0] * M, -q[1] * M, 0)
sk = close_sketch(); sk.Name = "SK_HeightTaper"
doc.ClearSelection2(True); sel(sk.Name, "SKETCH")
rc = fm.FeatureRevolve2(True, True, False, True, False, False, 0, 0, 2 * math.pi, 0.0,
                        False, False, 0.0, 0.0, 0, 0.0, 0.0, True, True, True)
if rc is None:
    raise RuntimeError("revolve cut failed")
rc.Name = "HeightTaper"
log("taper", mass())

# ---------------- 7. rotation arrow, 0.4 mm into the back face, 3 copies ----------------
# Arrow follows counter-clockwise rotation about +Z (true sense; seen from the back face it reads clockwise).
r_in, r_out, r_mid = 36.0, 40.0, 38.0
th0, th1, th2 = math.radians(200), math.radians(245), math.radians(262)
pt = lambda r, a: (r * math.cos(a) * M, r * math.sin(a) * M, 0)  # noqa: E731
open_sketch("Front Plane")
sm.CreateArc(0, 0, 0, *pt(r_out, th0), *pt(r_out, th1), 1)
sm.CreateArc(0, 0, 0, *pt(r_in, th0), *pt(r_in, th1), 1)
sm.CreateLine(*pt(r_in, th0), *pt(r_out, th0))
sm.CreateLine(*pt(r_out, th1), *pt(42.5, th1))
sm.CreateLine(*pt(42.5, th1), *pt(r_mid, th2))
sm.CreateLine(*pt(r_mid, th2), *pt(33.5, th1))
sm.CreateLine(*pt(33.5, th1), *pt(r_in, th1))
sk = close_sketch(); sk.Name = "SK_Arrow"
doc.ClearSelection2(True); sel(sk.Name, "SKETCH")
v0 = mass()[0]
try:
    cut = extrude(0.4, cut=True, flip=False)
except RuntimeError:
    log("cut toward -Z failed (no material); retrying with direction flipped")
    doc.ClearSelection2(True); sel(sk.Name, "SKETCH")
    cut = extrude(0.4, cut=True, flip=True)
cut.Name = "RotationArrow"
eqs.append(("D1@RotationArrow", '"arrow_depth"'))
log("arrow removed mm3", v0 - mass()[0])
doc.ClearSelection2(True)
sel("Axis_Z", "AXIS", False, 1)
sel("RotationArrow", "BODYFEATURE", True, 4)
ap = fm.FeatureCircularPattern4(3, 2 * math.pi, False, "", False, True, False)
ap.Name = "ArrowPattern"
log("arrow pattern", mass())

# ---------------- 8. link dimensions to global variables ----------------
for lhs, rhs in eqs:
    idx = em.Add2(-1, f'"{lhs}" = {rhs}', True)
    log("eq", lhs, "=", rhs, "->", idx)
doc.ForceRebuild3(False)
log("after equations", mass())
for i in range(em.GetCount):
    log("  ", em.Equation(i), "=", em.Value(i))

# ---------------- 9. hide sketches and axis, save ----------------
for name in ["SK_BackPlate", "SK_Hub", "SK_Blade", "SK_HeightTaper", "SK_Arrow"]:
    doc.ClearSelection2(True); sel(name, "SKETCH"); doc.BlankSketch()
doc.ClearSelection2(True); sel("Axis_Z", "AXIS"); doc.BlankRefGeom()
doc.ClearSelection2(True)
err = win32com.client.VARIANT(pythoncom.VT_BYREF | pythoncom.VT_I4, 0)
wrn = win32com.client.VARIANT(pythoncom.VT_BYREF | pythoncom.VT_I4, 0)
ok = ext.SaveAs3(OUT_PART, 0, 1, NOTHING, NOTHING, err, wrn)
log("saved", ok, err.value, OUT_PART)
log("fillet_note", fillet_note)
