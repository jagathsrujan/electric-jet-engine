# Roadmap: electric jet engine (college project)

Goal: a working demo on a thrust stand with measured thrust data and a report. 1-3 months, roughly Rs 5,000-15,000, 3D printer + welding / sheet metal, fired in a supervised college lab.

Each subsystem gets a v1 "master prototype" before the next one starts.

## Phase 1: Compressor
1. Learn the compressor types
2. Choose the type
3. Sizing and specs (mass flow, pressure rise, diameter, speed)
4. Motor, gearing (if any) and electronics for the compressor alone
5. Build and bench-test compressor v1 (flow, pressure, current against speed)

## Phase 2: Combustion chamber
Design (flame holder / liner, fuel injection, ignition), build v1, cold-flow test, then fired test.

## Phase 3: Nozzle
Design and build v1; one iteration on exit area.

## Phase 4: Electronics and systems
Controls and safety for each subsystem: blower speed control, fuel valve and shut-off, ignition (shielded), sensors, interlocks.

## Phase 5: Thrust stand
Guide rail, load cell, data logging; final cold and fired thrust runs.

## Two-machine workflow
- Mac (this workspace): planning, notes, FreeCAD checks, KiCad, Arduino.
- Windows PC: SolidWorks, ANSYS, MATLAB through their MCP servers.
- Sync method and handoff rules: to be agreed.

## Status
- [x] Video analysed (`video-notes-starstreak-mk1.md`)
- [x] Scope agreed
- [x] Phase 1 steps 1-3: centrifugal chosen and sized (`docs/parameters.md`)
- [x] Phase 1 step 4: drive chosen: DYS D3536-5 1450 KV, Skywalker 40A V2, 12 V 30 A supply at 13-14 V (`docs/motor-selection.md`); parts not yet bought
- [ ] Phase 1 step 5: impeller and volute CAD (Windows), compressor controller (Mac), print and bench-test v1
