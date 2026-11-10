# Impeller draft 2 (CAD v1)

Windows, SolidWorks 2026, 2026-11-10. Rebuilt from scratch per the Mac review in `HANDOFF.md` ("Mac · review of cross-check and impeller draft"). Open centrifugal impeller: back plate, hub, bore, 9 prismatic single-arc blades. No volute, no motor mount (they wait for the measured motor). Not simulated, not printed.

Files:
- `cad/impeller.SLDPRT` (native, overwrites draft 1)
- `cad/export/impeller.step`, `impeller.stl` (same model frame, see checks)
- `cad/export/impeller_iso.png`, `impeller_top.png`, `impeller_back.png` (SolidWorks screen captures, shaded with edges, sketches/axes/planes/origin hidden; only cropped afterwards)
- `cad/scripts/`: the build is a script, so it is reproducible
  - `blade_geometry.py`: blade arc maths (no SolidWorks)
  - `build_impeller.py`: builds and saves the part in the running SolidWorks (pywin32)
  - `export_impeller.py`: STEP, STL, view images
  - `check_impeller.py`: measures the built model (angles, CoM, volume, taper, fillets, rotation)
  - `check_parametric.py`: changes Z and bore through the equations, rebuilds, restores
  - `check_exports.py`: reads STL and STEP bounds in plain Python

Run order (interpreter `C:\Users\jagath srujan\mcp-servers\Solidworks-MCP\.venv\Scripts\python.exe`, SolidWorks open): `build_impeller.py`, `export_impeller.py`, `check_impeller.py`, `check_exports.py`.

Why scripts and not the MCP tools: the MCP has no view orientation, equation linking to dimensions, reliable pattern axis, or STL option control (draft 1 problems). The scripts attach to SolidWorks with `win32com.client.GetActiveObject("SldWorks.Application")`; the MCP server code was not changed.

## Frame and rotation direction

- Axis on Z. Back face of the back plate at Z = 0. Blades point to +Z, the inlet side. Sketch plane for plate, hub and blades: Front plane (XY).
- **Rotation: counter-clockwise viewed from the inlet side (looking down -Z onto the blades).** Viewed from the motor/back side it is clockwise.
- Blades curve backward: each blade runs clockwise as it goes outward (leading edge at polar angle 0 deg, r 24; it meets r 50 at -44.1 / -46.8 deg on its two faces, measured). That is backward-curved for counter-clockwise rotation. `impeller_top.png` is the view from the inlet side.
- Rotation arrow: engraved 0.4 mm into the back face, curved arrow pointing counter-clockwise about +Z (reads clockwise in `impeller_back.png`, which looks from behind). **Three identical arrows at 120 deg** instead of one, so the engraving does not shift the centre of mass (one arrow removes 67.8 mm^3 at r 38 mm, which alone would move the CoM about 0.08 mm, four times the 0.02 mm target).
- If the motor turns the other way, mirror the part about the Right plane; nothing else changes.

## Parameters (global variables in the part)

Source `docs/parameters.md` section 3 unless stated. "Drives" lists the dimensions linked by equations (`D1@...`).

| Variable | Value | Source | Drives |
|---|---|---|---|
| D2 | 100 mm | s3 | back plate diameter (`D1@SK_BackPlate`) |
| t_bp | 3 mm | s3 *(interp.)* | back plate thickness (`D1@BackPlate`); hub and blade extrude depth = t_bp + b1 |
| b1 | 10 mm | s3 | hub and blade height above the plate (`D1@Hub`, `D1@Blade`) |
| d_h | 20 mm | s3 *(interp.)* | hub diameter (`D1@SK_Hub`) |
| d_bore | 5.0 mm | s3, **provisional** (print 4.6, ream 5.0 *(interp.)*) | bore in plate and hub sketches (`D2@SK_BackPlate`, `D2@SK_Hub`) |
| Z | 9 | s3 | blade pattern count (`D1@BladePattern`) |
| r_fil | 1 mm | HANDOFF item 3 | root fillet (`D1@RootFillet`) |
| arrow_depth | 0.4 mm | HANDOFF item 5 | arrow engraving depth (`D1@RotationArrow`) |
| b2 | 6.5 mm | s3 | stored only: height taper sketch (coordinate table) |
| r1 | 24 mm | s3 | stored only: blade sketch (coordinate table) |
| beta1b | 35 deg | s3 *(interp.: 32 deg flow + 3 incidence)* | stored only |
| beta2b | 45 deg | s3 | stored only |
| Rb | 61.3 mm | s3 | stored only |
| t | 1.7 mm | s3 *(interp.)* | stored only |
| t_LE | 0.8 mm | s3 *(interp.)* | stored only |
| L_taper | 8 mm | s3 *(interp.)* | stored only |

**Parametric, partly.** Plate, hub, bore, heights, blade count, fillet and arrow depth follow the equations; `check_parametric.py` set Z = 7 and d_bore = 6, rebuilt (volume 30,888 to 29,744 mm^3, CoM still on axis at 3.7e-8 mm) and restored. **The blade outline and the height-taper profile are not linked**: they were drawn from coordinates computed in `blade_geometry.py`. To change r1, the angles, Rb, t, t_LE or b2, edit `blade_geometry.py` (`P`) and rerun `build_impeller.py`; the coordinate table below is what it drew for the current values.

## Method (feature tree)

1. `SK_BackPlate` / `BackPlate`: circle D2 and bore circle on Front plane, extruded t_bp (Z 0 to 3).
2. `SK_Hub` / `Hub`: annulus d_h / d_bore, extruded 13 mm from Z = 0 (top at Z 13).
3. `SK_Blade` / `Blade`: one blade outline on Front plane, extruded 13 mm from Z = 0 (merges with the plate). Outline: 0.8 mm leading-edge line at r1, two straight taper flanks to the full 1.7 mm thickness 8 mm along the centreline, two arcs concentric with the centreline arc (R 61.3 +/- 0.85 mm), closed by an arc on the D2 circle.
4. `RootFillet`: 1 mm fillet on all 5 root edges of the seed blade (two side arcs, two taper flanks, leading edge).
5. `Axis_Z`: reference axis at the intersection of the Top and Right planes (= model Z axis).
6. `BladePattern`: circular pattern of `Blade` + `RootFillet` about `Axis_Z`, 9 equal instances over 360 deg.
7. `SK_HeightTaper` / `HeightTaper`: revolve cut about Z removing everything above the line (r 24, Z 13) to (r 50, Z 9.5), i.e. blade height 10 mm at r1 falling linearly to 6.5 mm at D2 *(interp.: linear in r; the doc gives only end values)*.
8. `SK_Arrow` / `RotationArrow` and `ArrowPattern`: arrow cut 0.4 mm into the back face from Z = 0, patterned 3 times about `Axis_Z`.

Sketches and the axis are hidden in the saved part.

## Coordinate table (blade sketch, Front plane, mm; seed blade; others are rotated by 40 deg steps)

| Point | X | Y | r |
|---|---|---|---|
| Centreline arc centre C | -26.2140 | -35.1602 | 43.8568 |
| Centreline at leading edge | 24.0000 | 0.0000 | 24.0000 |
| LE corner, outer side (R + 0.4) | 24.3277 | 0.2294 | 24.3287 |
| LE corner, inner side (R - 0.4) | 23.6723 | -0.2294 | 23.6735 |
| Taper end, outer side (R + 0.85) | 28.9024 | -6.4408 | 29.6114 |
| Taper end, inner side (R - 0.85) | 27.3948 | -7.2264 | 28.3319 |
| Exit, outer side (on D2) | 35.9347 | -34.7663 | 50.0000 |
| Exit, inner side (on D2) | 34.2221 | -36.4533 | 50.0000 |
| Centreline at exit | 35.0842 | -35.6244 | 50.0000 |

Side arcs: centre C, radii 62.15 and 60.45 mm, drawn clockwise from taper end to exit. Taper end lies 8 mm of arc (0.1305 rad about C) from the leading edge. The centre is found from: centreline through (r1, 0) at beta1b from the backward tangent, radius Rb (`blade_geometry.centre`).

Height-taper profile (Top plane, r, Z): (20, 13), (24, 13), (50, 9.5), (55, 9.5), (55, 23), (20, 23), revolved 360 deg about Z.

Arrow (Front plane, polar, mm/deg): shaft annulus r 36 to 40 from 200 to 245 deg; head base r 33.5 to 42.5 at 245 deg; tip r 38 at 262 deg. Copies at +120 and +240 deg.

## Checks (measured from the built model by `check_impeller.py` / `check_exports.py`)

| Check | Target | Measured | Note |
|---|---|---|---|
| Blade inlet angle at r 24 | 35 deg | 34.999 to 35.002 deg (all 9 blades) | From the side-face cylinders of each blade: centre and radius read from the model, angle = acos((r^2 + R^2 - c^2) / (2 r R)) |
| Blade exit angle at r 50 | 45 deg | 45.003 to 45.004 deg (all 9) | 0.004 deg over because Rb is rounded to 61.3 mm |
| Centreline arc radius | 61.3 mm | 61.300 mm (side faces 60.450 / 62.150) | |
| Blade thickness | 1.7 mm | 1.700 mm | |
| Centre-of-mass radial offset | < 0.02 mm | **2.3e-8 mm** (x 2.1e-8, y 8.4e-9); CoM Z = 2.961 mm | draft 1 was 0.12 mm |
| Volume | | 30,888.2 mm^3 | |
| Mass at PLA 1,250 kg/m^3 *(interp.)* | doc about 50 g | **38.6 g** | volume x density; the part has no material assigned (no PLA in the SolidWorks library) |
| Izz at PLA *(interp. density)* | doc 5.5e-5 kg m^2 | 4.47e-5 kg m^2 | from SolidWorks inertia scaled to 1,250 kg/m^3 |
| Leading-edge width | 0.8 mm | 0.800 mm (distance between the LE corner edges) | |
| Taper length | 8 mm | 8.000 mm of arc (chord 7.994 mm); thickness at taper end 1.700 mm | |
| Root fillets | 1 mm, every root | 27 R1 cylinder faces (LE + 2 flanks per blade) + 18 tori (2 side arcs per blade) = all 5 root edges on all 9 blades; corner edges start at Z 4.0 = plate top + 1 mm | **Not stopped short anywhere**, including the 0.8 mm tapered tip |
| Rotation | CCW from inlet, backward blades | LE at 0 deg, blade reaches r 50 at -44.1 / -46.8 deg (clockwise) | backward-curved for CCW |
| Arrow | 0.4 mm deep on back face | 67.8 mm^3 per arrow removed, 3 arrows | visible in `impeller_back.png` |
| Model bounding box | | X -50..50, Y -50..50, Z 0..13 mm | |
| STL bounds (binary, mm, 6,382 triangles) | axis on Z, back face Z 0 | X -50.000..50.000, Y -49.981..49.936, Z 0.000..13.000; volume 30,840 mm^3 (-0.16 %, tessellation) | "do not translate to positive space" set |
| STEP bounds (AP214, mm) | same frame | points X -50.000..50.000, Y -49.981..48.833, Z 0.000..13.000 | Y max below 50 because the rim is stored as a circle, not points |
| Parametric test | | Z 7, bore 6: rebuilds, CoM 3.7e-8 mm; restored to 30,888.2 mm^3 | |

Blade heights: 10 mm at the leading edge (inner LE corner Z 3 to 13), 9.956 mm at the outer LE corner (the cone starts at r 24 exactly), 6.5 mm at r 50.

## Printability (back plate down, blades up)

- Blades stand straight up; no overhangs except the 0.4 mm arrow engraving on the bed face (a short bridge over 4 mm, fine on most printers *(interp.)*).
- Minimum features: leading edge 0.8 mm (about 2 lines at 0.42 mm *(interp.)*), blade 1.7 mm, plate 3 mm, hub wall 7.5 mm.
- Root fillets 1 mm to strengthen the blade-to-plate joint across layers.

## Not verified

- Nothing simulated, printed or balanced. The CoM check is ideal CAD geometry; print imbalance will be far larger and still needs the 1 g mm static balance.
- Mass and inertia depend on the PLA density *(interp.)* and assume 100 % infill.
- Bore and any hub flange are provisional until the motor is in hand; no flange is modelled.
- Blade outline and taper profile are not equation-driven (see Parameters).
- The STL is a fine-quality tessellation; slicer import was not tried.
- Images are SolidWorks graphics-area captures (`SaveBMP`), cropped with Pillow; the "iso" image is the `*Front` view tilted 55 deg so the axis stands up, because SolidWorks' `*Isometric` assumes Y up and shows this part on its side.
- The export script turns off the display of planes, axes, origins and sketches in this part's options and switches the view to shaded-with-edges; it also sets application STL export options (binary, mm, fine, no positive translation), which stay set in SolidWorks.
