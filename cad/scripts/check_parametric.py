"""Prove the equations drive the model: set Z = 7 and d_bore = 6, rebuild, measure, restore, rebuild."""
import math
import win32com.client

app = win32com.client.GetActiveObject("SldWorks.Application")
doc = app.ActiveDoc
em = doc.GetEquationMgr


def find(name):
    for i in range(em.GetCount):
        if em.Equation(i).startswith(f'"{name}"'):
            return i
    raise KeyError(name)


def meas(tag):
    doc.ForceRebuild3(False)
    mp = doc.Extension.CreateMassProperty
    c = mp.CenterOfMass
    print(f"{tag}: volume {mp.Volume*1e9:.1f} mm^3, CoM offset {math.hypot(c[0], c[1])*1e3:.2e} mm")


meas("baseline Z=9, bore 5")
iz, ib = find("Z"), find("d_bore")
em.Equation(iz, '"Z" = 7'); em.Equation(ib, '"d_bore" = 6')
meas("Z=7, bore 6")
em.Equation(iz, '"Z" = 9'); em.Equation(ib, '"d_bore" = 5.0')
meas("restored")
