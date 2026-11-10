# Video notes: "I Built a Homemade Electric Jet Engine from Scratch!" (StarStreak Mk.I)

Source: `~/Downloads/vidssave.com I Built a Homemade Electric Jet Engine from Scratch! 720P.mp4` (7 min 19 s, 720p).
Method: 147 frames sampled every 3 s plus a Whisper transcript, analysed by three Sonnet subagents; six key frames spot-checked by hand. Notes written 2026-11-10.

The video is a thrust test, not a build guide. The maker fires a small blower-fed combustor and measures 153.9 g peak thrust.

## What the engine is

It is not a turbojet: there is no turbine. An electric blower pushes air through a combustion chamber and out a plain nozzle.

- **Blower ("supercharger"):** 3D-printed grey centrifugal blower with a volute housing, conical inlet and a black multi-vane impeller. The cover is held by a ring of small screws. Speed is set by a PWM "Speed Controller" box with a percentage display.
- **Duct:** a printed tapered tube from the blower outlet, pushed onto the chamber inlet and held with a worm-drive hose clamp. No flanges.
- **Combustion chamber:** a welded steel can made of a cylinder, a cone and a short straight exit pipe, with visible girth and seam welds. Small enough to hold in one hand; roughly 20 cm long and 8–9 cm in diameter *(estimate by eye)*.
- **Nozzle:** plain straight pipe, no convergent-divergent section.
- **Ignition:** a standard spark plug in a boss on top of the chamber near the inlet, fed by a small black high-voltage module running off batteries (about 6 V in, per the maker). The second lead clamps to the chamber body.
- **Fuel:** an orange tube runs via a brass fitting to the inlet end of the chamber, and a green gas cylinder sits in the background. Gas fuel such as propane is an *inference*; it is never named.

## Test rig

- Engine on a linear guide rail on a 2×4 block, C-clamped to a plywood bench, pushing against a load cell.
- Arduino on a breadboard reads the load cell (amplifier board looks like an HX711, *inference*) and shows `Load` and `MAXload` in grams on a 16×2 LCD. Splash screen reads "StarStreak Mk.I".
- Mesh-cased mains power supply feeds the blower's PWM controller.
- Ignition module shielded inside a steel food can under the bench.

## Timeline

| Time | Event |
|---|---|
| 0:00–1:00 | Intro; chamber fabrication footage was lost (only brief editor proxy clips of filing and TIG welding are shown) |
| 1:00–1:45 | First firing to check it works |
| 1:50–2:55 | Blower-only baseline: peaks at about 26 g at roughly 100% PWM |
| 2:57–4:50 | Ignition module freezes the Arduino and garbles the LCD from 2–3 feet away; putting the module in a steel food can fixes it |
| 4:54–6:30 | Full run: about 65 g at 95% PWM before ignition, then 140–160 g with a blue core and a pink-orange plume; `MAXload` 153.91 g |
| 6:30–7:18 | Outro; new nozzles planned next |

## Lessons for our build

- Keep the high-voltage ignition module away from the microcontroller and shield it in a grounded metal enclosure; it disrupted an Arduino at 2–3 feet.
- Measure a blower-only baseline in the same run as the fired test so the combustion gain is unambiguous.
- A hose-clamped printed duct survived short runs at the cold inlet end of the chamber.

## Caveats

- **Baseline mismatch:** the blower-only test read about 26 g, but the final run read about 65 g at 95% before the visible ignition. The video doesn't explain the difference, so the combustion gain is somewhere between roughly 90 and 130 g.
- **Noise spikes:** during the shielded-coil test the LCD showed 434–543 g, which looks like ignition interference, not thrust.
- **Not shown anywhere:** chamber internals (liner, hole pattern, injector), the blower motor and its supply voltage, the fuel regulator, and any real dimensions.
- The opening "assembly" the narrator refers to did not appear in the sampled frames.
