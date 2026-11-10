# Video notes: "I Made A Powerful Hybrid Jet Engine - How much thrust does it make?" (the "Pyroflask")

Source: `~/Downloads/vidssave.com I Made A Powerful Hybrid Jet Engine - How much thrust does it make? 720P.mp4` (13 min 21 s, 720p). The on-screen credits and Thingiverse link point to the channel "AWA" (Ayden Wardell Aerospace).
Method: 200 frames sampled every 4 s (frame N is at about (N-1) x 4 s) plus a Whisper "small" transcript. Every frame was viewed; the speech was clear, so the engine data below is mostly the maker's own words. Frame numbers quoted as `f_NNN` are good to about +/- 1. Notes written 2026-11-10.

Labels used: **(said)** = stated by the maker, **(read)** = read off the screen, **(est.)** = estimated by eye, **(inference)** = my deduction, not shown in the video.

This video is more useful than the StarStreak one: it shows the chamber liner, hole pattern, fuel injector and ignition electrode in CAD sections and real photos, and it gives real thrust, weight and power numbers.

## What the engine is and how it works

- A "hybrid": an electric compressor feeds air into a combustion chamber, and the burner works like an afterburner that adds thrust to the cold-air thrust of the compressor. There is no turbine. (said)
- Name: "Pyroflask". The chamber is made from an old stainless double-walled drink bottle (flask). (said)
- Air path: motor-driven 3D-printed centrifugal compressor, then a printed volute and outlet, then a printed adapter, then the flask chamber (air jacket around a drilled inner liner), then a straight nozzle pipe.
- Fuel: gas (propane or butane) injected from a ring at the front of the liner; a spark/"emission wire" electrode lights it. Liquid fuel would need a different injector. (said)
- Result: just over 20 N fired versus about 8 N from the compressor alone; this is version 4 of the idea (V1 about 5 years ago, V2 two years later, V3 last year). (said)

## Timeline

| Time | Event |
|---|---|
| 0:00-0:12 | Teaser flames, title card "Water bottle to jet engine" |
| 0:12-0:55 | Origin: an old flask that no longer kept water cold; the double wall allows a separate liner inside an outer case; an electric compressor replaces a turbine; called "Pyroflask" |
| 0:55-1:45 | History. V1: low thrust, constant overheating, frequent flame-outs, scrapped after a couple of firings. V2: different compressor and better combustion, still weak. V3: first real thrust, aluminium impeller, 6.5 PSI boost but only 10 N because of a small nozzle |
| 1:45-2:20 | Goal: enough thrust to lift its own weight plus batteries. Compressor trade-off: too much pressure gives too little mass flow; too much flow gives unstable combustion |
| 2:19-3:38 | Tries a 5-stage 3D-printed PETG axial compressor. Open-nozzle and static-pressure tests; on-screen "Only 1.2 PSI". Surge test makes the PETG melt ("Smoke??!") |
| 3:38-4:20 | New backswept centrifugal compressor in a compact housing; new 4.2 kW motor |
| 4:21-5:45 | Chamber build: cut flask, drill liner, ring injector (CAD sections and bench photos) |
| 5:46-7:55 | Assembly on the test stand, servo fuel valve, first test at dusk; combustion very stable over a wide fuel-flow range; very loud |
| 8:01-8:50 | Scale camera exposure made the first data unreadable, so a second test session was run |
| 8:49-9:30 | Result: just over 20 N at full combustion, about 8 N with compressor only |
| 9:32-9:50 | Weights and thrust-to-weight |
| 9:48-10:20 | Endurance, no hot spots; power use 2.9 kW |
| 10:21-10:55 | Safety warning, hazard-zone diagram, Arduino controller failsafes |
| 10:56-11:55 | Planned improvements, conclusion |
| 12:08-13:21 | Credits; the Whisper text at 7:06-7:27 and 8:25-8:35 is a looped hallucination over music and is not content |

## Hardware, component by component

### Compressor (centrifugal, 3D printed)
- Type: centrifugal with "a fairly aggressive back-sweep angle" and a compact housing, "flow-optimized"; designed to use all of the motor's power through the bottle opening. (said) The video says it is "not my highest pressure variant" but moves enough air that no nozzle inserts were needed to build chamber pressure. (said)
- Impeller: bright green 3D print with a metal bullet-shaped hub nose and a retaining screw. About 10 backswept blades, an open (unshrouded) design (est. by eye, `f_167`). Diameter not stated; roughly 100-120 mm by eye (est.), judged against a 40 mm motor can and a printed part box of about 154 x 190 x 88 mm in Cura (read, partly legible, `f_168`).
- Housing: printed volute with a round inlet, an outlet that sweeps into the white adapter, and a flat back plate. A Cura screen shows 1 day 20 h 13 min and 1789 g / 599.98 m of filament for the main housing, and 219 g / 73.39 m for a second part (read). All printed parts use solid (100 %) infill for strength and pressure tolerance. (said, and `f_168`)
- Earlier compressors: V3 had an aluminium impeller (said); an earlier blue printed impeller of about 12 blades with a white ribbed cover plate held by small screws appears around 1:08 (est.).
- Axial failure: 5-stage printed PETG axial with tight tip clearances, stators in a green printed barrel held with screws; it made only 1.2 PSI (read, on-screen caption) and melted in surge from compression heating. (said)

### Motor, ESC and battery
- New motor: Rocket-RC 4092-920KV, 4 poles, inrunner can style, rated 4.2 kW continuous, rated for 50,000 rpm. (said and read, `f_064`) Old motor: Surpace Hobby 4076, 2000 KV, 2800 W (read). The maker thinks 44 % more power could be pushed through the same motor with a higher voltage or bigger impeller. (said)
- Mount: 6 mm thick aluminium motor/heat-sink plate bolted to the housing with a ring of screws; the motor was "only slightly warm" after nearly 10 minutes of testing, so he wants a carbon-fibre plate instead (said; `f_172`-`f_173`). The motor sits in a grooved black collar/cooling sleeve at the centre of the volute. A grub-screw shaft collar is machined for the shaft (`f_063`).
- ESC: a large red-sleeved brushless ESC; part of its label is legible as "...150A... 5-12S No BEC" (read, `f_053`, partly blurred, so treat as uncertain).
- Battery: "a 12 cell lithium battery" (said). On screen there are 4S 14.8 V 5200 mAh packs, labelled 80C, and a bench of eight packs (read, `f_154`-`f_155`). Three 4S 5200 mAh packs in series would make the 12S pack (inference).
- Panel meter readings during tests (read, small display with "V" and "A" markers):
  - V3 test: 45.8 V, 37.6 A (`f_011`).
  - Another compressor run: 44.7 V, 54.8 A (`f_062`).
  - Final fired run: 42.3 V, 67.1 A, then 42.0 V, 66.7 A (`f_152`-`f_153`). 42 V x 67 A is about 2.8 kW, matching his "2.9 kilowatts". (said)
- Runtime: 3-4 minutes on one pack set. (said) Check (inference): 5.2 Ah x 0.8 usable / 67 A is about 3.7 min, consistent.

### Combustion chamber (the part we most wanted to see)
- Material and origin: stainless double-walled flask. Outer wall, inner wall and bottom cap; "very old and slightly tapered". (said)
- How it was cut (said, with bench shots `f_071`-`f_074`): cut off the bottom cap with a Dremel cutting disc, wire-brush off the paint, belt-sand away the welds so the inner wall slides out, cut off the threaded neck. The inner wall becomes the liner; the outer wall is the pressure case. The inner wall's own neck forms the exit tube.
- Overall shape (CAD `f_007`, `f_068`, `f_067`): tapered outer case, wide at the compressor end and narrowing toward a short domed shoulder that necks into a straight nozzle pipe. The liner is a straight, constant-diameter can inside it, with an annular air gap between liner and case.
- Estimated size (est., scaled from the CAD assuming the 35 mm callout on `f_010` is the nozzle pipe): outer case about 60-70 mm wide at the large end, liner about 40-45 mm outer diameter and 140-150 mm long, case plus nozzle about 200 mm. Treat these as rough; the only number actually shown is "35.00 mm" on the nozzle pipe in CAD (it is not stated whether this is inner or outer diameter).
- Liner hole pattern (said, and CAD `f_007`, `f_010`, `f_079`-`f_080`, `f_082`):
  - Rings of round holes around the circumference, drilled by hand with a cordless drill after marking a grid with a marker pen (`f_075`-`f_077`).
  - Sparse, small holes near the fuel injector at the front, with hole size and density increasing steadily toward the nozzle end (said).
  - Each hole is bent inward toward the oncoming air (scoops) to help mixing (said).
  - A number of film-cooling rings: rows of very small, tightly spaced holes on the inside of the liner, shown with red arrows near the rear shoulder (`f_080`) (said and CAD).
  - "Thin bent gaps" around where the nozzle pipe leaves the case, to feed cooling air along the walls (said, arrows at both ends of the liner in `f_078`).
  - Hole counts and diameters are not given. By eye the large rings near the rear have roughly a dozen holes each, about 8-10 mm across (est., from `f_082`, very rough).
- Front of the liner: a short inward-turned or conical lip with two small angled tabs (CAD `f_078`) acts as a simple flame-holding/recirculation step; no swirler or vane ring is visible in this build (the swirl-vane diagram at `f_006` is a generic reference from avationstackexchange, not his hardware).
- Wall thickness: not stated; the CAD shows thin sheet, similar to ordinary flask steel (est. well under 1 mm).

### Fuel and injection
- Fuel: gaseous (propane and butane named). (said) A standard white propane cylinder is shown (`f_174`). The thrust dropped slightly late in a run "as the fuel tank was depressurized". (said)
- Injector: an annular ring made from a bent copper tube, with 8 holes of 2 mm drilled around its circumference, slid into the front of the liner and fastened with wire ties. (said, `f_085`-`f_086`, `f_082`) The copper ring fits just inside the front lip of the liner, and a copper feed pipe leaves through the white adapter (CAD `f_068`-`f_078`). Total hole area is about 25 mm2 (inference: 8 x pi x 1 mm2).
- Control hardware (labelled in `f_175`): solenoid shutoff valve, servo-driven throttling valve (a brass valve with a servo arm), then a fuel check valve, then clear tubing and a copper pipe into the adapter. A quick-connect brass coupling and a yellow hose bring gas from the cylinder. Fuel for a 3-minute run weighs about 200 g. (said)
- A set of brass industrial spray nozzles appears (`f_084`, "image from amazon") when he says liquid fuel would need a different injector (said); that is a suggestion, not what he used.

### Ignition
- A 3D-printed adapter has a "built-in emission wire": a thin wire/electrode moulded in, entering through a red lead at the adapter and bending in toward the liner front near the injector ring (said, CAD `f_078`, photos `f_053`, `f_082`). The spark source is not named; the controller has an IGNITION push button.

### Nozzle
- Plain straight stainless pipe, 35 mm (CAD callout), no convergent or divergent section and no nozzle inserts. (CAD `f_010`; said "didn't need any nozzle inserts"). The V3 version had a smaller nozzle that gave high pressure but only 10 N. (said)

### Printed adapter, joints, fasteners
- White 3D-printed adapter between volute outlet and flask: round, with radial screw holes around its face and a ribbed black coupling ring at the volute side (`f_058`, `f_061`, `f_053`). The flask outer case is attached with a ring of small black screws (`f_053`); a clamp-style joint on the volute side with an M-size hex screw (`f_053`, `f_054`).
- Back plate: round plate held with a ring of countersunk screws (aluminium now, carbon-fibre CAD later, `f_172`-`f_173`).
- Foil: aluminium foil is wrapped around the fuel line / adapter area as a heat shield (`f_017`, `f_053`).
- The printed adapter and housing are at the cold (compressor) end; the case and liner are steel.

### Control electronics
- Arduino-based handheld controller on a ~3 m cable, with: IGNITION button, POWER and ARMED LEDs, a fuel-flow knob (also labelled OXY FLOW in the printed legend), PUMP ON/OFF switch, and a 0-100 % throttle slider (`f_163`). (read)
- Fail-safes: any loss of power or signal shuts down the engine and the fuel system. (said)
- Other: a pressure gauge on the rig (Hoke Phoenix dial, 10 PSI maximum, calibrated in pounds per square inch and ounces, `f_011`, `f_044`), clear sensing tube from the chamber; an action camera on a tripod.

## Test rig and measured numbers

- Rig (CAD `f_044`-`f_050`, photos `f_121`, `f_126`): engine on 2020 aluminium extrusion rails inside a white sheet-metal housing, pushing against a red/black digital kitchen scale (Taylor); a rubber stop sits between engine and scale. Reading is by camera, which is why the first run's data were lost to exposure problems. (said)
- Thrust numbers (said unless marked):
  - Compressor only (cold): about 8 N.
  - Fired: "just over 20 Newtons" at full combustion, with small losses as batteries ran down and the tank depressurized.
  - Scale readings seen on screen (read): 1690 g and 1970 g in the fired run (`f_139`-`f_140`); 1970 g is 19.3 N (inference), so "just over 20 N" is probably a peak not caught in a sampled frame or a rounding. A blurred 570 g reading (`f_141`) cannot be interpreted.
  - V3 (previous best): 10 N with 6.5 PSI boost. (said)
  - Axial attempt: 1.2 PSI. (read)
- Weight: engine 1.37 kg on a scale (read, `f_144`), batteries and controller about 800 g, fuel about 200 g, total about 2370 g (on-screen sum). Thrust-to-weight of the power system: said "0.9", while an on-screen caption says 0.8; 20 N / 23.2 N is 0.86 (inference), so both are roundings.
- Electrical power: about 2.9 kW on 12S, readings 42.0-42.3 V and 66.7-67.1 A. (said, read)
- Temperatures: the only figure is a caption "approx. 1200 C" on archive footage of the early version's nozzle glowing white-hot. (read) For this version he says there were no obvious hot spots in the chamber or nozzle, and film cooling did its job. (said) The motor was only slightly warm after nearly 10 minutes of testing. (said)
- rpm: not measured or shown. The motor is rated 50,000 rpm. (said) At 920 KV and 42 V the no-load speed would be about 38,000 rpm (inference); loaded speed is unknown.
- Run time: "no time limitations" thermally; limited only by battery (3-4 min per pack set). (said)
- Noise: "one of my loudest contraptions", louder than his rocket engines. (said)

### Back-of-envelope (inference only; none of this is in the video)
- With a 35 mm nozzle (about 9.6 cm2) and 8 N cold thrust, the ideal relation F = 2 x A x dP gives a chamber pressure of roughly 4 kPa (0.6 PSI) and an air flow of roughly 90-100 g/s. This assumes the 35 mm is the inner diameter and a perfect nozzle.
- Fuel of about 200 g in 3 minutes is about 1.1 g/s, which is roughly 50 kW of heat, so the exhaust would be only a few hundred kelvin hotter than the inlet, giving a very lean overall mixture. The fired-to-cold thrust ratio is about 2.5.

## Problems and fixes

| Problem | Fix or outcome |
|---|---|
| V1: low thrust, constant overheating, flame-outs | Scrapped. Rebuilt with better compressor and liner (V2, V3, then this) |
| V1/V2: white-hot nozzle near melting | Film cooling rings, graded holes and liner in a double-wall case; this version has no hot spots |
| V3: high pressure but only 10 N | Small nozzle restricted flow; the new design favours air flow over pressure |
| Printed axial compressor: low pressure, PETG melted in surge | Abandoned; went back to a centrifugal design |
| Thrust data unreadable (camera exposure on the scale) | Second test session |
| Fuel tank depressurising as it empties | Small thrust loss; accepted (possible switch to a liquid-fuel pump later) |
| Weight | Several hundred grams could be saved with less infill, a carbon-fibre motor plate and liquid fuel instead of heavy brass valves (said) |

## What this teaches our build

Compare StarStreak Mk.I (153.9 g peak fired, about 26 g blower-only baseline, roughly 20 cm welded steel can) and our plan (30 g/s, 1.5 kPa, 100 mm printed impeller, 12,000-15,000 rpm, welded steel chamber, gas fuel, load cell).

1. **Liner layout to copy.** This is the missing piece in the StarStreak video: a drilled inner can inside an outer jacket, with rings of holes that start small and sparse at the injector and grow bigger and denser toward the exit, scoop-bent inward, plus small film-cooling holes and a narrow gap where the liner meets the nozzle neck. It is simple enough to make by hand with a drill and a marker grid. Scale the total hole area to our flow and pressure drop: the maker's engine passes roughly three times our air flow (inference, section above) at a higher pressure, so our holes will be fewer or smaller overall. We should also not copy his hole counts since none are given.
2. **Fuel injector.** A bent copper ring with 8 x 2 mm holes works for gas at his flow; ours burns much less fuel, so start with fewer or smaller holes (total area well below his roughly 25 mm2, to be sized from our fuel flow and regulator pressure) and keep the hole area on the cylinder side large enough to avoid choking the supply.
3. **Fuel control and safety.** He uses a solenoid shutoff, a servo throttling valve, a check valve and an Arduino controller with failsafes that cut fuel on any power or signal loss. Adopt the same three-valve pattern. This also supports the StarStreak lesson on keeping HV ignition wiring away from the microcontroller; here the controller is handheld on a long cable.
4. **Ignition.** An electrode embedded in the printed adapter next to the injector ring is a neat, repeatable way to place the spark, and it needs no hole in the steel can. Confirm that the printed part near the spark stays cool (it did here, in the cold inlet air).
5. **Stainless flask as a chamber.** A DIY alternative to welding. Our welded steel can can still copy the double-skin idea: a perforated inner liner with an air gap to the outer wall.
6. **Compressor.** His printed centrifugal impeller works with a backswept design and solid infill; the axial printed attempt failed (low pressure, melted in surge). Keep to the centrifugal route and do not run in surge. His tip speeds are far higher than ours: if his impeller is about 110 mm at roughly 35,000 rpm, the tip speed is about 200 m/s (est.), compared with about 63-78 m/s for our 100 mm at 12,000-15,000 rpm (inference). That is why he gets several kPa and we are targeting 1.5 kPa.
7. **Pressure versus flow.** V3 shows high boost with a small nozzle gave only 10 N, while the newer high-flow design gave 20 N. For our nozzle size, aim for flow first; check the flow and pressure points against the compressor sizing notes.
8. **Cold versus hot gain.** Here the fired thrust is about 2.5 times the cold thrust (about 8 N to about 20 N). StarStreak's own run suggests roughly 2.4 times (about 65 g to about 154 g). A fired result of about 2.5 times our cold thrust would be a reasonable expectation (inference).
9. **Measurement.** Use a scale or load cell in line with a linear rail, and have a camera framing the scale with fixed exposure; he lost a first run to unreadable scale footage. Record cold and fired thrust in the same session.
10. **Gas supply.** The tank depressurised and thrust fell slightly late in the run. For propane, expect cooling of the cylinder at higher draw; a regulator and a larger cylinder or warm water bath help (general knowledge, not from the video).
11. **Hazard zones (said and diagram).** Flame up to 80 cm; radiant-heat zone 1 m around the flame and 5 m behind it; centrifugal debris hazard in line with the impeller, 10 m or a shield; intake zone 2 m; he stood about 3 m to the side. Our test plan should include the same exclusion areas and a debris shield.
12. **Motor power.** His motor can supply 4.2 kW; ours should be sized from our smaller 30 g/s load rather than copied.

## Not shown / uncertain

- Impeller diameter, exact blade count, back-sweep angle, tip clearance, inducer size and volute dimensions are not stated (blade count of about 10 and diameter of 100-120 mm are by-eye estimates).
- Liner hole diameters, hole counts per ring, ring spacing, open-area fractions and wall thickness are not given; the 35 mm figure is the only dimension on screen, and it is unclear whether it is inner or outer.
- Exact chamber pressure of the final engine (the gauge is present but no legible reading for the fired run), rpm, exhaust temperature and fuel flow rate or regulator pressure.
- The spark source and its voltage, and how the liner is retained in the case (the CAD shows it located by the printed adapter and the neck; the method is not described).
- ESC brand and rating (label only partly legible), battery cell count (12S is said; 3 x 4S 5200 mAh is my inference).
- The thrust reading of "just over 20 N" is not clearly visible in the sampled frames; the 1970 g reading is the closest legible number.
- The "power system thrust-to-weight" is said to be 0.9 but the caption says 0.8 (my calculation gives 0.86).
- Whisper transcript quality: segments at 7:06-7:27 and 8:25-8:35 are repeated hallucinations over silent footage. The frame-numbered times are approximate (+/- 1 frame, 4 s).
