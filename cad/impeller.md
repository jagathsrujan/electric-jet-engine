# Impeller draft (CAD v0)

Windows, SolidWorks 2026, 2026-11-10. Open centrifugal impeller with back plate, hub and bore. No volute, no motor mount. Draft only: not simulated, not printed, not checked against the motor.

Files: `cad/impeller.SLDPRT` (native), `cad/export/impeller.step`, `cad/export/impeller.stl`, `cad/export/impeller_iso.png`, `cad/export/impeller_top.png`.

## Parameters (source: `docs/parameters.md` section 3 unless stated)

Global variables with these names exist in the part's equation table. **They are not linked to sketch dimensions** (see "Limitations"), so changing one does not change the geometry yet.

| Variable | Value | Source | Modelled as |
|---|---|---|---|
| D2 | 100 mm | s3 | Back plate OD; blade tip radius 50 mm |
| Z | 9 | s3 | 9 blades, 40 deg apart |
| beta2b | 45 deg | s3 | Exit blade angle from tangent, exact (see below) |
| t | 1.7 mm | s3 | Constant blade thickness (2 concentric arcs, offset +/- 0.85 mm) |
| t_LE | 0.8 mm | s3 | **Not modelled** (leading edge is square, 1.7 mm) |
| d1 | 48 mm | s3 (under review by Mac) | Eye diameter: start radius of the blade-height taper (r = 24 mm) |
| b1 | 10 mm | s3 (under review) | Blade and hub height above the back plate for r <= 24 mm |
| b2 | 6.5 mm | s3 | Blade height at r = 50 mm |
| d_h | 20 mm | s3 | Hub diameter, 10 mm tall boss above the back plate (hub top at z = 13 mm) |
| d_bore | 5.0 mm | s3 | **PROVISIONAL.** Through bore, drawn at the nominal 5.0 mm (doc says print 4.6 and ream) |
| t_bp | 3 mm | s3 | Back plate thickness, z = 0 to 3 mm |
| Hub flange | none | HANDOFF (Mac) | **PROVISIONAL / not modelled.** The hub is a plain 20 mm boss. The motor bolt circle (16 x 19 mm, 4 x M3 *(interp.)*) is not in the model yet |
| beta1_LE | 42 deg | s3 beta1m | Blade inlet angle used to define the arc (see below). Parameter for the hub-angle review |
| r1_LE | 18.4 mm | s3 (rms radius) | Blade leading-edge radius |
| R_blade | 49.8453 mm | computed | Blade centreline arc radius |

## Modelling method

Axis is Z. Back plate on the Front plane (z 0 to 3), hub boss (z 3 to 13), blades, then a taper cut.

1. **Back plate:** circle 100 mm, bore 5 mm, extruded 3 mm.
2. **Hub:** annulus 20 / 5 mm, extruded 10 mm from the plate top.
3. **Blades:** one sketch on the plate top holding all 9 blade outlines, one extrude of 10 mm. Each outline is two concentric arcs (R +/- 0.85 mm) closed by a straight leading edge and a straight chord at r = 50 mm. Blade centreline arc: centre at (-18.642, -33.353) mm, radius R = 49.845 mm, leading edge at (18.4, 0), trailing edge at 51.9 deg clockwise (viewed from +Z) at r = 50. Clockwise outward means backward curved for counter-clockwise rotation viewed from the blade side (+Z). Rotation sense is *(interp.)*; mirror the model if the motor turns the other way.
4. **Height taper:** revolve cut (Top plane sketch) of the region above a straight line from (r 24, z 13) to (r 50, z 9.5), which gives blade height 10 mm at the eye falling linearly to 6.5 mm at the tip. Hub is unaffected (r < 24).

Blade centreline angles measured from the tangent (computed from the arc geometry, `cos(beta) = (r^2 + R^2 - c^2) / (2 R r)`, c = distance from origin to arc centre; not measured back from the SolidWorks model):

| Radius | Angle from tangent |
|---|---|
| r = 50 mm (exit) | 45.00 deg (matches beta2b) |
| r = 18.4 mm (leading edge) | 42.00 deg (matches beta1m) |
| r = 24 mm (eye edge) | 48.0 deg |

The doc asks for 61 / 42 / 35 deg at hub / rms / shroud, i.e. a blade twisting by 26 deg from hub to shroud. A constant-height extruded 2D arc has one angle per radius, so it can match the doc only at one radius. I chose the rms value (42 deg at 18.4 mm). At the shroud radius (24 mm) this arc is 48 deg, 13 deg steeper than the doc's 35 deg. Hub (r = 10 mm) has no blade in this model because the leading edge starts at 18.4 mm. A true 3D inlet twist is not modelled.

## Approximations and deviations from the doc

- Blade is a pure 2D extrusion (no inlet twist, no leading-edge taper, no fillets).
- Blade height taper is linear in radius, starting at the eye radius; the doc gives only the two end values.
- Blades start at r = 18.4 mm, not at the hub (r = 10 mm), so the region r = 10 to 18.4 mm is an open flat plate.
- Not patterned by the circular-pattern tool: see "Limitations".
- No tip clearance (eps = 0.5 mm) applies yet: that belongs to the volute fit.
- No balance features.

## Printability (back plate down, blades up)

- Minimum thicknesses in the model: blade 1.7 mm (about 4 perimeters at 0.42 mm), back plate 3 mm, hub wall 7.5 mm, trailing-edge chord about 2.4 mm.
- Gap between neighbouring blades at the tip is 2 pi 50 / 9 = 34.9 mm; the minimum passage near the leading edge is about 11 mm. No overhangs, no supports. The bore is vertical; print at 4.6 mm and ream *(interp., from doc)*.
- The model is a single solid; blade-to-plate joints have no fillets. Adding a 0.5 to 1 mm fillet at the blade roots is advisable (not done).

## Mass (assumed PLA *(interp.)*)

SolidWorks has no PLA entry in its material library (3 matches only for "PLA": plain carbon steel, 7075 and plasticized PVC, all irrelevant), so no material was assigned (SolidWorks reports 1000 kg/m^3 by default).

| Quantity | Value |
|---|---|
| Volume (`sw_get_mass_properties`) | 32,024 mm^3 (32.02 cm^3) |
| Mass at PLA 1,250 kg/m^3 (`parameters.md` s6) | **40.0 g** (hand-multiplied from the volume) |
| Doc estimate | about 50 g, mostly solid, so the CAD is 20 % lighter |
| Mass at default 1,000 kg/m^3 | 32.0 g |
| Moment of inertia Izz at 1,000 kg/m^3 | 3.634e-5 kg m^2, so about 4.5e-5 at PLA (doc: 5.5e-5) |
| Centre of mass offset from axis | about 0.12 mm (x -0.112, y 0.048) |

STL cross-check: the exported STL volume is 31,990 mm^3, within 0.1 % of the model.

## Not verified / known issues

- **Static imbalance in the CAD:** a symmetric 9-blade part should have its centre of mass on the axis, but the model's is 0.12 mm off. That is about 4.8 g mm at 40 g against the 1 g mm target. The first blade (extruded alone before the other eight were added to the sketch) added 669 mm^3 in an earlier test build, while the average over all nine in this build is 706 mm^3, so one blade may differ slightly. The cause was not found; geometry looks uniform in the viewport. Re-check before any print or balance study.
- The blade angles above are calculated, not measured in SolidWorks.
- The STL is exported by SolidWorks with the origin shifted into the positive octant (bounding box 0..100 mm in X/Y, 20..33 mm in Z), so it is not centred on the bore axis. Re-centre when importing into a slicer if needed. The STEP is in model coordinates (axis through the origin, back plate bottom at z = 0).
- Back plate, hub and bore are real geometry, but the bore and any hub flange are provisional until the motor is in hand.
- Hub inlet angle (61 deg in the doc, under review): not used by the geometry.
- The 5 mm bore is drawn at nominal size, not the 4.6 mm print size.
- Nothing about strength, balance, or flow has been checked.

## Limitations of the tooling (what the SolidWorks MCP could not do)

- **Global variables are not linked to sketch dimensions.** The tools draw by coordinates, so the names exist in the equation table but nothing is driven by them. To make the model truly parametric, someone needs to bind dimensions to the variables in the SolidWorks GUI.
- **Circular pattern failed to give a correct result.** `sw_circular_pattern` picked an axis offset from the true axis (blades landed off-centre, centre of mass 1.2 mm off) or errored, and could not be told to use a pattern spacing without collapsing the total angle. Instead all 9 blade outlines were computed (rotated copies of one blade at 40 deg steps) and drawn in one sketch. There is no pattern feature in the tree.
- **No isometric capture:** `sw_capture_viewport` captures the current view only, and there is no tool to change it (the model was in the top view). `impeller_top.png` is the SolidWorks capture (top view); `impeller_iso.png` is rendered from the exported STL with matplotlib (not SolidWorks).
- No PLA material in the SolidWorks library.
- A first revolve cut sketched with y > 0 on the Top plane failed because Top plane sketch y maps to -Z; it was redone with y < 0. An unused sketch remains in the tree.
