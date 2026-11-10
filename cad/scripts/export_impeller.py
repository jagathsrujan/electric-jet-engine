"""Export impeller draft 2: STEP + STL in model coordinates, and real SolidWorks view images.

Run after build_impeller.py with cad/impeller.SLDPRT active in SolidWorks.
- STEP AP214 and binary STL (mm) with "do not translate STL data to positive space" on,
  so both keep the model frame: axis on Z, back face at Z = 0.
- impeller_iso.png: SolidWorks pictorial view (*Front rotated 55 deg about screen X; axis up). impeller_top.png: SolidWorks *Front view,
  which looks down -Z from the +Z (inlet/blade) side, i.e. the true top view of the impeller
  as printed (back plate down). Sketches, axes, planes and origins hidden.
"""
import math
import os

import pythoncom
import win32com.client
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
EXP = os.path.join(os.path.dirname(HERE), "export")
NOTHING = win32com.client.VARIANT(pythoncom.VT_DISPATCH, None)

app = win32com.client.GetActiveObject("SldWorks.Application")
doc = app.ActiveDoc
assert doc.GetTitle.lower().startswith("impeller"), doc.GetTitle
ext = doc.Extension


def save_copy(path):
    err = win32com.client.VARIANT(pythoncom.VT_BYREF | pythoncom.VT_I4, 0)
    wrn = win32com.client.VARIANT(pythoncom.VT_BYREF | pythoncom.VT_I4, 0)
    ok = ext.SaveAs3(path, 0, 1 | 2, NOTHING, NOTHING, err, wrn)  # silent | copy
    print("save", os.path.basename(path), ok, err.value, wrn.value, os.path.getsize(path) if os.path.exists(path) else "missing")


# STL options (application-level preferences)
app.SetUserPreferenceToggle(71, True)    # swSTLDontTranslateToPositive
app.SetUserPreferenceToggle(69, True)    # swSTLBinaryFormat
app.SetUserPreferenceToggle(70, False)   # swSTLShowInfoOnSave
app.SetUserPreferenceToggle(191, False)  # swSTLPreview
app.SetUserPreferenceIntegerValue(211, 0)  # swExportStlUnits = mm
app.SetUserPreferenceIntegerValue(78, 2)   # swSTLQuality = fine

save_copy(os.path.join(EXP, "impeller.step"))
save_copy(os.path.join(EXP, "impeller.stl"))

# Views: hide reference geometry and sketches
for t in (4, 5, 6, 7, 13, 19, 196):
    doc.SetUserPreferenceToggle(t, False)
doc.ClearSelection2(True)
doc.ViewDisplayShaded()
doc.GraphicsRedraw2()


mv = doc.ActiveView
mv.DisplayMode = 5  # swViewDisplayMode_ShadedWithEdges


def shot(view, name, tilt_deg=0.0):
    doc.ShowNamedView2(view, -1)
    if tilt_deg:
        mv.RotateAboutCenter(math.radians(tilt_deg), 0.0)
    doc.ViewZoomtofit2()
    mv.Scale2 = mv.Scale2 * 0.7   # zoom-to-fit overshoots the visible graphics area; back off, then crop
    doc.GraphicsRedraw2()
    bmp = os.path.join(EXP, name + ".bmp")
    ok = doc.SaveBMP(bmp, 1600, 1200)
    im = Image.open(bmp).convert("RGB")
    dark = im.convert("L").point(lambda v: 255 if v < 90 else 0)   # model edge lines
    x0, y0, x1, y1 = dark.getbbox()
    assert x0 > 5 and y0 > 5 and x1 < im.width - 5 and y1 < im.height - 5, ("model clipped", (x0, y0, x1, y1))
    m = 40
    im = im.crop((max(0, x0 - m), max(0, y0 - m), min(im.width, x1 + m), min(im.height, y1 + m)))
    png = os.path.join(EXP, name + ".png")
    im.save(png)
    os.remove(bmp)
    print("view", view, tilt_deg, ok, png, im.size)


# Pictorial view: *Front (looking down -Z at the blade side) tilted 55 deg about the screen X axis,
# so the axis stands up. SolidWorks' own *Isometric assumes Y up and shows this part edge-on.
shot("*Front", "impeller_iso", -55.0)
shot("*Front", "impeller_top")
shot("*Back", "impeller_back")   # back face, shows the rotation arrows (seen from behind they read clockwise)
doc.ShowNamedView2("*Isometric", -1)
doc.ViewZoomtofit2()
doc.Save3(1, win32com.client.VARIANT(pythoncom.VT_BYREF | pythoncom.VT_I4, 0),
          win32com.client.VARIANT(pythoncom.VT_BYREF | pythoncom.VT_I4, 0))
