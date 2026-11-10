# Handoff log

Newest entry first. Each entry: date, machine, what was done, files changed, what is needed from the other machine.

---

## 2026-11-10 · Windows · impeller draft

**Done:** First SolidWorks draft of the impeller only (Sonnet subagent), from `docs/parameters.md` section 3. It is an open impeller: D2 100 mm, 3 mm back plate, 9 circular-arc blades 1.7 mm thick (arc radius 49.8 mm, from r 18.4 mm to the tip). Blade angles from geometry: 45 deg at the exit and 42 deg at the leading edge (rms value). At the eye edge the angle is 48 deg; the doc's shroud value is 35 deg. A single arc cannot give the doc's hub-to-shroud twist. Blade height is 10 mm out to r 24 mm, tapering to 6.5 mm at the tip. Hub 20 mm; bore 5 mm. Bore and hub flange are provisional until the motor is measured. Volume is 32.0 cm³, about 40 g in PLA *(interp., 1,250 kg/m³)*.

**Known gaps:**
- **Not parametric:** global variables exist but do not drive the sketches (the tools draw by coordinates).
- **No pattern feature:** the 9 blades are drawn individually in one sketch.
- **Imbalance:** the centre of mass is 0.12 mm off the axis (about 4.8 g·mm against a 1 g·mm target). The cause is not found.
- **STL position:** the STL is shifted to positive coordinates; the STEP is in model coordinates.
- **Not modelled:** leading-edge taper and blade-root fillets.
- **Iso picture:** `impeller_iso.png` is rendered from the STL with matplotlib, not a SolidWorks view.

Nothing was simulated, printed or fitted to the motor.

**Files:** `cad/impeller.SLDPRT`, `cad/impeller.md`, `cad/export/impeller.step`, `.stl`, `impeller_iso.png`, `impeller_top.png`

**Needed from Mac:** Review the blade angles: is 48 deg at the eye acceptable for a draft, or do you want a twisted (3D) blade? The hub inlet angle and 48 mm eye questions from the previous entry are still open.

---

## 2026-11-10 · Windows · blower cross-check (impeller CAD blocked)

**Done:** Independent Python cross-check of `docs/parameters.md` sections 2-5 (Sonnet subagent; kept in `matlab/`, not renamed). 100 of 112 values agree within 2 %. Most of the 12 outliers trace to the eye diameter: the script's optimum is 47 mm vs the doc's 48 mm (flat optimum; with `--d1 48` they match). **One unexplained:** the hub inlet angle (doc 61 deg blade / 57.6 deg flow; script 59.3 / 56.3 deg even with a 48 mm eye). Performance map 6,000-15,000 rpm with the 32 mm orifice curve is in `matlab/blower_map.png`. The model holds efficiency and slip constant, so the map is optimistic off-design *(interp.)*. Nothing was tested or run in CFD, and the script uses the same correlations as the doc, so it cannot catch a wrong model choice.

**Impeller CAD: not started.** The SolidWorks MCP connection failed on this PC (SolidWorks was not open when the session began). It needs a reconnect; then the impeller draft goes ahead as requested.

**Files:** `matlab/blower_crosscheck.py`, `.md`, `.csv`, `matlab/blower_map.csv`, `.png`

**Needed from Mac:** Check the hub inlet angle in section 3 (please show how 61 deg was derived) and confirm the 48 mm eye stays before the CAD uses them.

---

## 2026-11-10 · Mac · motor research and second reference video

**Done:** Researched drive parts (Sonnet subagent, web prices checked 2026-11-10; nothing bought or bench-tested). The user confirmed this set on 2026-11-10: DYS D3536-5 1450 KV outrunner (5 mm shaft), Hobbywing Skywalker 40A V2 ESC, 12 V 30 A adjustable supply trimmed to about 13-14 V. Also added notes on a second reference build (the "Pyroflask"), which shows a combustion liner hole pattern and fuel control useful for Phase 2.

**Files:** `docs/motor-selection.md`, `docs/video-notes-hybrid-jet.md`

**Needed from Windows:** For the impeller draft, treat these as provisional parameters until the motor is in hand and measured: shaft 5 mm, motor body 35 mm diameter, mounting pattern 16 x 19 mm with 4 x M3 *(interp., taken from a different seller's D3536 page)*. Shaft protrusion and prop-adapter dimensions are unknown; keep them as parameters. Earlier requests still stand.

---

## 2026-11-10 · Mac · compressor sizing

**Done:** User chose a single-stage centrifugal blower, backward-curved, direct brushless drive. Preliminary 1D mean-line sizing written (Sonnet subagent; arithmetic spot-checked, nothing tested or simulated). Headline: 30 g/s, 1.5 kPa, D2 100 mm, 9 blades at 45 deg, 11,700 rpm design, 15,000 rpm max, about 70 W shaft at design.

**Files:** `docs/parameters.md` (source of truth), `docs/compressor-sizing.md` (teaching write-up)

**Needed from Windows:**
1. Cross-check calculation: MATLAB was not found on your PC, so use Python (in `matlab/` is fine; rename the folder to `calc/` if you prefer and note it here). Write an independent script that takes the targets in `docs/parameters.md` section 1, recomputes sections 2-5 (slip, velocity triangles, geometry, operating points) and reports any value that differs by more than 2 %. Save a performance-map plot (pressure and shaft power against flow for 6,000-15,000 rpm with the 32 mm-orifice system curve) as PNG plus CSV, with a short Markdown summary. If the user confirms MATLAB is installed somewhere you did not look, use that instead.
2. SolidWorks: a draft of the impeller only (section 3), driven by a parameter table matching `docs/parameters.md`. Leave the hub flange and bore as parameters: the motor is not chosen yet. Export STEP to `cad/export/` and an isometric PNG. Do not start the volute or motor mount yet.
3. No ANSYS work yet.

---

## 2026-11-10 · Windows

**Done:** Cloned the repo to `C:\Projects\electric-jet-engine` (a long path failed with "Filename too long"; keep the clone path short). Checked the tools on this PC:
- SolidWorks MCP: connected, SolidWorks 2026 (revision 34.0.0).
- ANSYS MAPDL MCP: responds; ANSYS 2024 R1 (v241) installed at `E:\ANSYS Inc\v241`.
- ANSYS Fluent MCP: server responds (PyFluent backend), no Fluent session started yet.
- MATLAB: not found on this PC and no MATLAB MCP server *(not verified beyond `C:\Program Files` and `E:\`)*. Calculations may need Python or another route.
- KiCad MCP also responds here, but `electronics/` is owned by the Mac.

**Files:** `HANDOFF.md`

**Needed from Mac:** Compressor sizing targets in `docs/parameters.md`; decide where MATLAB-type calculations should run.

---

## 2026-11-10 · Mac

**Done:** Analysed the reference video, agreed scope with the user, wrote the roadmap, set up this shared repo. Compressor type recommended: single-stage centrifugal, backward-curved blades, direct brushless drive (user has not confirmed yet).

**Files:** `CLAUDE.md`, `ROADMAP.md`, `HANDOFF.md`, `video-notes-starstreak-mk1.md`

**Needed from Windows:** Nothing to build yet. Please confirm in a new entry that the repo cloned, and list which MCP servers respond (SolidWorks, ANSYS, MATLAB) with their versions. Compressor sizing targets will follow in `docs/parameters.md`.
