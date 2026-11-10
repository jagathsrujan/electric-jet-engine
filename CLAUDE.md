# Electric jet engine (college project)

A blower-fed combustor "electric jet engine": brushless-driven 3D-printed centrifugal blower, welded steel combustion chamber, spark ignition, gas fuel, nozzle, load-cell thrust stand. Goal: a working supervised demo with measured thrust data and a report. Read `ROADMAP.md` for phases and status, and `video-notes-starstreak-mk1.md` for the reference build.

Constraints: 1-3 months, roughly Rs 5,000-15,000, 3D printer + welding / sheet metal (no lathe), fired only in a supervised college lab.

## Two machines, one repo

Two Claude Code sessions share this repo through GitHub.

| Machine | Does | Owns |
|---|---|---|
| Mac | Planning, notes, FreeCAD checks, KiCad, Arduino firmware | `docs/`, `electronics/`, `firmware/` |
| Windows PC | SolidWorks CAD, ANSYS simulation, MATLAB calculations | `cad/`, `sim/`, `matlab/` |

Rules for both sessions:
1. `git pull --rebase` before starting work; commit and `git push` when a piece of work is done. The user has approved commits and pushes to this repo for this purpose.
2. After each piece of work, add an entry at the top of `HANDOFF.md`: date, machine, what was done, files changed, what is needed from the other machine.
3. Read the newest `HANDOFF.md` entries at the start of every session and act on requests addressed to your machine.
4. Do not edit files in folders the other machine owns; ask through `HANDOFF.md` instead. Shared files (`ROADMAP.md`, `HANDOFF.md`, `docs/`) can be edited by either, in small commits.
5. Exchange formats: geometry as STEP (plus STL for printing) in `cad/export/`; results as CSV and PNG; every result gets a short Markdown summary with inputs, method and key numbers. Native files (`.SLDPRT`, `.wbpj`, `.FCStd`) are committed but only opened on their own machine.
6. Design parameters live in `docs/parameters.md` (single source of truth). CAD, simulation and MATLAB read their numbers from there; change the file first, then the model.
7. Keep large solver output out of git (see `.gitignore`); commit the setup and the summarised results.

## Working with the user
- Work with the user step by step: explain, agree, then build. Do not jump ahead of the roadmap phase.
- Keep usage low. The top-tier model is for ideation and discussion only; delegate research, calculation, CAD, simulation and file-writing to Opus, Sonnet or Haiku subagents, cheapest that can do the job.
- Mark every assumption *(interp.)* and say what was not verified.

## Safety
This project burns gas fuel. Design for a remote fuel shut-off, no fuel flow unless the blower is running, shielded ignition electronics, and printed parts kept away from heat. Live firing happens only in the supervised lab.
