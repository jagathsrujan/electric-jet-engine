# Handoff log

Newest entry first. Each entry: date, machine, what was done, files changed, what is needed from the other machine.

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
- ANSYS MAPDL MCP: responds; ANSYS 2024 R1 (v241) installed at `E:\ANSYS Inc241`.
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
