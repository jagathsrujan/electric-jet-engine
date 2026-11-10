# Handoff log

Newest entry first. Each entry: date, machine, what was done, files changed, what is needed from the other machine.

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
