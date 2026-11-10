# Motor, ESC and supply selection: centrifugal blower v1

Status: research note, prices and stock checked 2026-11-10 (India, INR, GST included unless stated). Nothing here is bought or bench-tested. *(interp.)* marks every assumption or own calculation; the last section lists what is unverified. Requirements come from `parameters.md` section 7; derivation in `compressor-sizing.md`.

## 1. Requirements recap

| Item | Value |
|---|---|
| Load | 100 mm PLA/PETG open impeller, about 50 g, J = 5.5e-5 kg m^2, direct drive |
| Loaded speed range | 6,000-15,000 rpm (sweeps from 3,000) |
| No-load speed at supply voltage | at least 17,000 rpm |
| Shaft power at 15,000 rpm | 147 W expected, 197 W pessimistic |
| Torque at 15,000 rpm | 94 / 126 mN m (scales with rpm^2) |
| Motor class | at least 300 W continuous, 5 mm shaft preferred |
| Duty | bench, supervised lab, runs of a few minutes (PLA runs 60 s or less per the structural section) |
| Budget | whole engine Rs 5,000-15,000; drive about Rs 3,000-5,000 |

Derived numbers used below *(interp.)*: Kt (mN m per A) = 9549 / KV. Electrical input at 15,000 rpm about 245 W pessimistic (shaft 197 W + copper 12 W + no-load loss about 36 W), about 190 W expected.

## 2. Check of the chosen design direction

The direction (35xx outrunner, 12 V mains supply, hobby ESC, Arduino PWM, independent rpm sensor) holds up. Findings that change details:

1. **12 V with a 1,450 KV motor works but with thin voltage margin.** Worked example for the DYS D3536-5 (R = 0.023 ohm, no-load current 3.5 A, both from the Robu listing): at 15,000 rpm back-EMF is 10.3 V; pessimistic load needs about 22.6 A in the phases, giving 10.3 + 0.5 (copper) + 0.3 (ESC, wire, connector, assumed) = about 11.2 V, i.e. about 93 % throttle on a stiff 12.0 V supply. The full-throttle loaded ceiling is about 16,000 rpm, only 6-8 % above 15,000. Nominal no-load speed is 1450 x 12 = 17,400 rpm, about 17,100 after drops, which only just meets the 17,000 requirement, and cheap hobby motors often miss their KV label by 5-10 % *(interp.)*. Mitigation: the recommended 12 V supply is listed as adjustable by plus or minus 20 %; trim it to about 13 V (still inside the ESC 3-4S limit of 16.8 V). That gives a ceiling near 17,300 rpm loaded. Measure the real KV first (section 9, check list).
2. **The listed "no-load speed at supply voltage 17,000" requirement forces KV x V >= 17,000.** At 12 V that means KV of about 1,420 or more. A 1,000 KV motor on 12 V (Turbo 3536 is even printed as "rated 12,000 rpm at 12 V") cannot reach 15,000 loaded. It needs 18-24 V.
3. **Hobbywing Skywalker V2 ESCs are 3-4S only** (40 A and 50 A models) so they cannot take a 24 V supply. Higher voltage means a different, 6S-capable ESC.
4. **Do not use an INA226 breakout as-is.** Typical INA226 modules carry a 0.1 ohm shunt (about 3.2 A full scale, *(interp.)*, the Robu listing does not state it). At 20 A it would burn the shunt. Use a hall sensor module (ACS758, 50 A) or fit an external shunt of about 2 mohm (44 mV at 22 A, inside the INA226 82 mV range) *(interp.)*.
5. **MPXV7002DP is plus or minus 2 kPa full scale**, but the blower reaches 2.46 kPa at 15,000 rpm (`parameters.md` section 5). It would clip above about 13,500 rpm. Use a 0-4 kPa class part (MPXV5004DP) or, for the 0-2.5 kPa bench test, a water U-tube manometer (2.46 kPa = 251 mm of water) *(interp.)*. It is also an SMD part that needs a breakout board.
6. **Heat.** About 48 W of loss in a 102 g motor with no prop airstream is a lot: adiabatic rise could approach 1 K/s *(interp.)*, an upper bound since heat also flows into the mount and air. The "prop-rated" 655 W figure assumes a prop in free airflow. Keep full-speed runs short, leave the bell exposed to air (not buried in the printed housing), watch bell and hub temperature (PLA hub below 45 C per sizing doc). This matches the 60 s PLA run limit already set.

## 3. Supply options compared

| Option | Motor KV | No-load at supply | Pros | Cons |
|---|---|---|---|---|
| A. 12 V mains SMPS, trimmed to about 13 V | about 1,450 | 17,400 (12 V) to 18,900 (13 V) | no battery risk, repeatable, cheapest, ESC 3-4S works | thin margin at 12.0 V; about 21 A DC at worst case; regen and inrush need care (section 5) |
| B. 4S LiPo (14.8 V nominal, 16.8 V full) | 1,000-1,250 | 14,800-21,000 | stiff supply, absorbs regen | LiPo fire risk, charging, sags with state of charge, repeatability; the user rejected it |
| C. 24 V mains SMPS (24 V 15 A, 360 W) | about 1,000 | about 24,000 | half the current (about 10 A), large headroom (ESC at about 62-65 % at 15,000 rpm), low sag | needs a 6S-capable ESC (Skywalker V2 40/50 A is 3-4S only), motor R and I0 not published, regen at 24 V is harsher |

Recommendation: A for the first build. C is the runner-up if A shows too little margin.

## 4. Motor candidates (sold in India)

Mounting-pattern notes: "16x19 M3x4" is read as four M3 holes (one pair 16 mm apart, the perpendicular pair 19 mm apart, the usual cross-type pattern) *(interp.)*. Verify with calipers on delivery.

| Motor | KV | Max power (listing) | Max current | Cells / voltage | Shaft | Mount | Weight | Price, stock | URL |
|---|---|---|---|---|---|---|---|---|---|
| **DYS D3536-5** | 1,450 | 655 W | 45 A (Robu), 45.2 A (Evelta) | 2-4S, 7.4-14.8 V | 5 mm | 16 x 19 mm, M3 x 4 (from Flash Hobby's D3536 page, not on the Indian listings) | 102 g incl. connectors (Robu); 103 g (Evelta) | Robu Rs 2,169, in stock; Electropi Rs 1,563 + 18 % GST = Rs 1,844, 4 in stock; Electronicscomp Rs 1,549 + GST, out of stock; Evelta Rs 1,501, sold out | https://robu.in/product/dys-d3536-5-1450kv-bldc-motor/ , https://www.electropi.in/dys-d3536-5-1450kv-bldc-motor , https://electronicscomp.com/dys-d3536-5-1450kv-bldc-motor , https://evelta.com/d3536-1450kv-brushless-motor-cw-ccw-for-fixed-wing-multicopter-quadcopter-drone/ |
| Surpass Hobby C3542 14-pole | 1,450 | not listed | not listed | operating 12 or 24 V, rated 18,000 / 36,000 rpm | 5.0 mm x 15 mm | not listed | 142 g | Ingenium Rs 2,850, out of stock; Robu Rs 2,999, out of stock | https://ingeniumdrives.in/product/surpass-hobby-c3542-14pole-outrunner-brushless-motor-for-fixed-wing-aircraft%cf%865-015mm-4-0mm-connector-1450-kv/ |
| Turbo 3536 (12N14P) | 1,000 | not listed | not listed | 12 or 24 V, rated 12,000 rpm at 12 V / 24,000 at 24 V | 5.0 x 53.5 mm | 19 x 25 mm, M3 x 4 | 105 g | Ingenium Rs 2,700, in stock | https://ingeniumdrives.in/product/turbo-3536-outrunner-brushless-motor-1000kv/ |
| DYS D3536-8 | 1,000 | 432 W (Flash Hobby page for 1000 KV) | not seen | 2-4S | 5 mm *(interp., same series)* | 16 x 19 *(interp.)* | about 102 g *(interp.)* | Robu Rs 2,119-2,169 (price shown in the "you may also like" block; its own page was not opened) | https://robu.in/product/dys-d3536-8-1000-kv-bldc-motor/ *(URL guessed from the D3536-5 slug pattern, not opened)* |

Rejected: Surpass C3536 910 KV and 1,050 KV (shaft 4 mm, Rs 3,150 Ingenium; Robu Rs 2,539 / Rs 2,189 out of stock), Surpass C3530 (shaft 4 mm), A2212 / 2212 class (3.17 mm shaft, too little power). Robu's Surpass C3536 and C3530 pages show "4.0 mm" shafts; Ingenium's C3536 910 KV title says "5mm shaft" but its spec table says 4 mm, so the 4 mm reading is used.

### Check against the requirement (12 V supply unless stated)

| Motor | No-load at 12 V | 15,000 rpm reachable on 12 V? | Phase current at 197 W pessimistic | Prop-rated power believable without prop airflow? |
|---|---|---|---|---|
| DYS D3536-5 | 17,400 nominal | yes, about 93 % throttle, ceiling about 16,000 rpm | about 22.6 A (DC side about 21 A) vs 45 A rating | 655 W is a burst figure at 14.8 V in an airstream. Our load is about 37 % of it in power, 50 % in current, but the no-load loss makes about 48 W of heat with no airflow. Fine for runs of a minute or so, watch temperature *(interp.)* |
| Surpass C3542 | 17,400 nominal | same as above (same KV), resistance and I0 unknown | about 22 A *(interp.)* | no power rating published; out of stock |
| Turbo 3536 1000 KV | 12,000 | no (needs EMF 15 V), works only on 24 V: about 15 A phase, about 10 A DC | n/a at 12 V | no rating published; motor R and I0 not listed |
| DYS D3536-8 1000 KV | 12,000 | no on 12 V; usable on 4S or 18-24 V | n/a | 432 W per Flash Hobby page |

Torque constant check, DYS D3536-5: Kt = 9549 / 1450 = 6.59 mN m/A, so 126 mN m needs 19.1 A for torque plus about 3.5 A for losses.

## 5. ESC and 12 V supply

### ESC

| ESC | Rating | Voltage | BEC | Brake | Price, URL |
|---|---|---|---|---|---|
| **Hobbywing Skywalker 40A V2** | 40 A continuous, 60 A peak | 3-4S LiPo | 5 V 5 A switch-mode | programmable: Disabled / Normal / Reverse / Linear Reverse; leaflet marks Disabled as the factory default | Rs 1,769, in stock: https://robu.in/product/hobbywing-skywalker-40a-v2-esc-fixed-wing/ |
| Hobbywing Skywalker 50A V2 | 50 A / 70 A | 3-4S LiPo | 5 V 5 A | same family | Rs 2,439, in stock: https://robu.in/product/hobbywing-skywalker-50a-v2-esc-fixed-wing/ |
| SimpliFly 30A | 30 A | 2-6S | not stated | not checked | Rs 889, in stock: https://robu.in/product/simplifly-esc-30a/ (flight-controller style, OneShot125 / DShot; plain servo PWM and brake setting not verified) |

Specifications for the Skywalker V2 are from the Hobbywing leaflet (https://cdn.shopify.com/s/files/1/0109/9702/files/SKYWALKER_V2_Leafiet_ENs.pdf); the Robu page itself only gives "3-4S", 40 A and wire gauge (input 14 AWG, output 16 AWG). 40 A covers the 21 A worst case with about 2x margin. Programming is by LED Program Box or throttle stick from a transmitter; the Arduino can also send the stick sequence *(interp.)*, but the exact procedure was not extracted.

Settings to apply: brake Disabled (check, do not trust the default), low-voltage cutoff Low or Disabled (a 12 V supply dipping under load could otherwise trigger "3S cutoff"), cell count set manually (the auto-detect may mistake a trimmed 13 V supply, *(interp.)*), start-up Normal or Soft, timing Medium.

### Supply

| Item | Spec | Price | URL |
|---|---|---|---|
| **12 V 30 A 360 W metal SMPS** (ElectronicsComp EC-2391) | 100-264 V AC input, output adjust plus or minus 20 %, overload / over-voltage / short protection with auto-recovery, free-air convection (no fan), indoor use only, 137 in stock | Rs 989 + 18 % GST = Rs 1,167 | https://www.electronicscomp.com/12v-30amp-smps-dc-metal-power-supply-nwp-india |
| Alternative | Sharvi Electronics 12 V 30 A 360 W, Rs 1,299 ex GST | | https://sharvielectronics.com/product/12v-30a-360-watt-ac-dc-enclosed-switching-single-output-power-supply/ (price from search snippet; page not opened) |
| 24 V 15 A 360 W (runner-up) | ElectronicsComp EC-2395, Rs 1,279 + GST = Rs 1,509, 17 in stock | | https://www.electronicscomp.com/24v-15amp-smps-dc-metal-power-supply-nwp-india (price from search snippet) |

Worst-case DC load is about 21 A (252 W), 70 % of the rating, and the spin-up adds about 7 A for a 2 s ramp to 15,000 rpm (J x alpha / Kt, alpha = 785 rad/s^2, *(interp.)*), so about 28 A, just under 30 A. A 0.5 s ramp would demand about 26 A extra and trip the supply, so ramps must be 2 s or longer.

### Known problems of an ESC on a switching supply, and the fixes

| Problem | Why | Fix |
|---|---|---|
| Supply over-current shutdown or hiccup | 360 W units have no spare for a hard start; cheap units trip around 105-135 % *(interp.)* | Ramp throttle slowly (about 2-3 s from idle to 15,000 rpm), never step; derate: keep expected current under about 24 A |
| Regenerative voltage spikes on deceleration | The ESC cannot push energy back through an SMPS; the bus rises. A capacitor absorbs very little (4,700 uF raised from 12 to 15.6 V stores only about 0.2 J, against about 70 J of rotor energy) | Slow ramp-down (let the fan load decelerate the rotor); keep brake disabled; try ESC active freewheeling Off if spikes appear; put a 12 V bleeder across the bus (for example a 10 ohm 25 W resistor, about 14 W at 12 V, *(interp.)*) or a sealed lead-acid battery floating on the bus; check the bus with a meter in peak-hold or scope during rapid throttle cuts; ESC limit is 16.8 V |
| Input ripple and long leads | PWM current of about half the load is chopped by the ESC; the supply is too far away to supply it | At least 4 x 1,000 uF 25 V low-ESR capacitors within 5 cm of the ESC input, short thick leads (12 AWG), twisted pair |
| Inrush and plug-in sparking | ESC input capacitors charge on connecting | Switch the AC side, not the DC plug; or use an XT60 anti-spark; power the ESC only after the supply is stable |
| False low-voltage cutoff | Supply sag looks like a dying battery | Cutoff Low or Disabled; trim supply to about 13 V |
| Mains safety | Open-frame screw terminals on a mains unit | Enclose, earth the metal case, E-stop on the AC side (a DPST 10 A switch is fine at about 3 A mains draw), cover the terminals |

## 6. Impeller to shaft attachment

What is known: the DYS motor ships with "1 prop adapter" and an X-type motor holder (Robu and Electropi listings); the adapter type and thread are not described in the text, and pictures were not readable. Retail "A2212 collet prop adapter" parts (Robu Rs 69) are for 3.17 mm shafts and do not fit. No Indian listing for a 5 mm collet adapter was found; US sources (Scorpion 5 mm threaded adapter, M6 x 1.0; MPI / Dualsky collet types, about USD 6-8) may not ship to India.

| Option | Description | For 15,000 rpm printed hub |
|---|---|---|
| 1. Metal collet or cone adapter on the 5 mm shaft with M6/M8 thread, impeller sandwiched between metal flange and nut | grips the whole shaft by friction through metal, printed part only squeezed | **Best.** Add a short metal compression sleeve (aluminium or brass tube a few tenths of a mm shorter than the hub) and washers of 14 mm OD or more so PLA creep cannot loosen it. Use a nyloc nut or threadlocker |
| 2. Bolt the back plate to the bell top screws | no shaft grip needed | Good if the bell has threaded holes. Not yet known; measure the real motor. Hub flange then has to clear that bolt circle (20 mm hub OD is a minimum) |
| 3. Printed bore (print at 4.6 mm, ream to 5.0 mm) with set screw | | Poor: set screw marks the shaft and the plastic relaxes |

Nut direction *(interp., derived)*: the impeller lags the shaft during acceleration and under load, so a right-hand nut self-tightens when the motor turns counter-clockwise as seen from the impeller side. Choose rotation by swapping two phase wires, and match the blade sense (backward-curved blades fix the rotation the impeller needs).

## 7. Speed measurement (independent of the ESC)

| Method | Pulses per rev | Frequency at 15,000 rpm | Pros | Cons |
|---|---|---|---|---|
| **Optical reflective** (IR reflective module aimed at a strip of reflective or white tape on a black back face) | 1 | 250 Hz | no mass on the rotor, no interference from motor magnets, trivial for an Arduino interrupt | lab light flicker (100 Hz mains lighting) and sunlight can disturb: shroud the sensor, use a narrow beam, debounce |
| Hall sensor (A3144 module, Rs 29) plus 1-2 small neodymium magnets in the hub | 1-2 | 250-500 Hz | cheap, immune to light | adds rotor mass (balance it with an opposite magnet or dummy mass); stray field from the motor bell can disturb it; the A3144 is a unipolar latch so magnet polarity matters |
| Phase-wire sensing (one motor phase through a divider and comparator or opto-isolator) | pole pairs per rev (7 if the motor is 12N14P *(interp.)*) | about 1,750 Hz | no rotor changes | needs level conditioning, depends on pole count, independent of impeller but not of the motor |

Recommendation: optical reflective as the primary reading (period measurement in micros, averaged), with the phase wire optionally logged as a cross-check against slip or skipped teeth. The ESC's own rpm output is not used.

## 8. Electronics block list (compressor alone)

Mains outlet (earthed, RCD) -> E-stop (DPST, mains side) -> 12 V 30 A SMPS (trimmed to about 13 V) -> fuse 30 A -> hall current sensor (ACS758-50B, in the + lead) -> bulk capacitors at the ESC -> ESC -> motor.
Arduino Nano (powered from USB; if the ESC BEC red wire is connected, do not also power from USB) provides: servo PWM (1,000-2,000 us) to the ESC, rpm interrupt input, ADC for current sensor and a voltage divider on the bus, ADC for the pressure sensor, a watchdog that drops throttle to 1,000 us if serial stops, and the ramp limiter in firmware (acceleration at most 15,000 rpm in 2 s).
Pressure sensor: manometer for the first tests; electronic sensor later. Common ground only at one point.

## 9. Recommendation

**Recommended set (first build):** DYS D3536-5 1450 KV + Hobbywing Skywalker 40A V2 + 12 V 30 A metal SMPS.

| | Rs |
|---|---|
| Motor (Robu, in stock) | 2,169 |
| ESC (Robu, in stock) | 1,769 |
| 12 V 30 A SMPS (ElectronicsComp, GST included) | 1,167 |
| **Drive total (motor, ESC, supply)** | **5,105** |
| With the motor from Electropi (Rs 1,844 incl. GST) | 4,780 |
| Supporting electronics (section 10: capacitors, Nano, hall sensor, current sensor, E-stop, wire and connectors) | about 1,100 |
| **Whole compressor electronics without a pressure sensor** | **about 6,200** |
| With an MPXV7002DP chip from Robu (needs breakout) | about 9,200 |

The three-item drive is about Rs 100-300 over the Rs 3,000-5,000 target; shipping not included. It is dominated by cheap, widely sold parts, and the motor can be bought from several shops.

**Runner-up (24 V route):** Turbo 3536 1000 KV (Rs 2,700, Ingenium) + 24 V 15 A SMPS (Rs 1,509) + SimpliFly 30 A 2-6S ESC (Rs 889) = about Rs 5,100. Benefits: half the current, big voltage headroom. Risks: motor R and I0 unknown, ESC brake / PWM handling not verified, harsher regen. Fall back to this if the measured KV or sag on the 12 V route leaves less than about 5 % speed margin. (A 4S LiPo with 1000 KV is also possible but was excluded by the safety choice.)

### Mounting dimensions of the recommended motor (DYS D3536-5)

| Dimension | Value | Source |
|---|---|---|
| Body diameter x length | 35 x 36 mm | Robu ("35x36m"), Flash Hobby ("35*36mm") |
| Shaft diameter | 5 mm | Robu, Evelta, Electropi |
| Shaft length | "5.0 x 53.5 mm" in the Flash Hobby spec; not stated whether this is total length or how far it protrudes from the bell; Surpass C3542 for comparison is 5.0 x 15 mm | Flash Hobby page |
| Mounting hole pattern | 16 x 19 mm, 4 x M3 | Flash Hobby D3536 page (matched to the DYS motor on size, 102 g and 655 W) *(interp.)* |
| Weight | 102 g with connectors | Robu |
| Poles | "12" per Robu, 12N14P per related Turbo/Surpass pages *(interp.)* | Robu |

Not given anywhere: bell height and bell top-face hole pattern, shaft protrusion, base boss diameter, depth allowed for the M3 screws (use short screws, about 4-5 mm, to avoid touching the windings *(interp.)*). The CAD hub and motor mount should leave these as parameters until the real motor is measured.

## 10. Bill of materials

Prices from the cited pages on 2026-11-10 unless marked.

| Item | Spec | Source URL | Price (Rs) |
|---|---|---|---|
| Motor | DYS D3536-5 1450 KV, 5 mm shaft, 2-4S, 102 g, supplied with prop adapter and X mount | https://robu.in/product/dys-d3536-5-1450kv-bldc-motor/ | 2,169 |
| ESC | Hobbywing Skywalker 40A V2, 3-4S, 5 V 5 A BEC, brake programmable | https://robu.in/product/hobbywing-skywalker-40a-v2-esc-fixed-wing/ | 1,769 |
| Power supply | 12 V 30 A 360 W metal SMPS, adjustable plus or minus 20 % | https://www.electronicscomp.com/12v-30amp-smps-dc-metal-power-supply-nwp-india | 1,167 (989 + GST) |
| Bulk capacitors | 4 x 1000 uF 25 V Rubycon 25PK, radial, near ESC | https://robu.in/product/25pk1000mefc10x16-rubycon-aluminum-electrolytic-capacitor-1000uf-25v-20-radial/ | 112 (4 x 28) |
| Microcontroller | Arduino Nano clone, ATmega328P, CH340, unsoldered | https://robu.in/product/arduino-nano-board-3-0-with-ch340-chip-unsoldered/ | 199 |
| Current sensor | MCU-758 ACS758LCB-050B hall module, plus or minus 50 A | https://robu.in/product/mcu-758-hall-current-sensor-acs758lcb-050b-pff-t-linear-current-sensor-module/ | 369 |
| Voltage monitor (optional) | INA226 module (bus voltage; shunt must be replaced for 20 A use); listing out of stock | https://robu.in/product/ina226-voltage-current-and-power-monitor-module/ | 139 |
| Hall rpm sensor (alternate) | A3144 module | https://robu.in/product/hall-magnetic-sensor-module/ | 29 |
| Optical rpm sensor | IR reflective module (TCRT5000 type) and tape | not checked | about 50 *(interp.)* |
| E-stop | LAY37 mushroom button, 1NO 1NC, 10 A contacts, latching | https://robu.in/product/ac-660v-10a-lay37-dpst-emergency-stop-push-button-switch/ | 109 |
| Wire, fuse, connectors | 12 AWG, 30 A fuse, XT60, heat shrink | not checked | about 300 *(interp.)* |
| Pressure sensor, option A | MPXV7002DP, plus or minus 2 kPa (clips above about 13,500 rpm); chip needs breakout | https://robu.in/product/pressure-sensor-mpxv7002dp-differential-1-v-kpa-2-kpa-2-kpa-4-75-v-5-25-v/ | 2,979 |
| Pressure sensor, option B | water U-tube manometer (clear tube, ruler), 0-250 mm water | not checked | about 100 *(interp.)* |
| Impeller adapter | 5 mm shaft collet adapter, M6 or M8 thread | not found in India; ask seller, or use the one supplied with the motor | not priced |

## 11. Unverified / check before buying

- **Motor specs from image-only fields.** Robu and Electropi attach spec images (dimension and spec drawings) that could not be read; mounting pattern and shaft protrusion are not confirmed for the DYS listings. The 16 x 19 mm M3 x 4 pattern is from the Flash Hobby D3536 page and assumed identical. Ask the seller for the dimension drawing or measure on arrival.
- **Motor KV.** The label 1,450 KV may be 5-10 % off; spin on the bench and measure back-EMF or phase frequency before relying on the 17,000 rpm no-load requirement at 12 V.
- **I0 and resistance.** 3.5 A and 0.023 ohm are Robu's numbers; the voltage at which the 3.5 A was measured is not given; the Turbo and Surpass motors list neither.
- **Pole count.** Robu says "12"; it is probably 12N14P (14 magnet poles); this sets the phase-sensor frequency (7 pole pairs assumed).
- **Prop adapter type** supplied with the DYS motor (collet or cone, thread size) is not stated in text.
- **Bell top holes**, bell height, shaft length outside the bell: unknown.
- **Stock and prices** change daily; Robu (motor, ESC) and Ingenium were opened with current stock shown; Electronicscomp and Electropi motor listings were opened; Sharvi, Evelta stock states and the 24 V supply price come from search snippets or an unclear stock badge.
- **ESC.** Hobbywing leaflet gives the settings table but this note did not confirm the throttle-range calibration procedure, whether plain 1,000-2,000 us arming works without a calibration step, or the program-box price. The "brake Disabled by default" reading assumes the asterisks in the extracted leaflet text align with the items in order *(interp.)*.
- **Skywalker V2 and the 12 V supply**: cell auto-detect with a trimmed 13 V supply and the true cutoff voltage are unverified.
- **SimpliFly 30 A:** brake behaviour and servo-PWM input not confirmed.
- **12 V SMPS:** over-current trip point, over-voltage trip level, inrush current, ripple, and the reasoning for "no fan at 360 W" are not stated on the listing; the adjust range of plus or minus 20 % is as printed and may really be about 10 %. Check it before trimming to 13 V.
- **Regen on deceleration** is unmeasured; whether active freewheeling or brake settings change it needs a bus voltage test at the first run.
- **Thermal:** bell temperature at 15,000 rpm is an estimate; not measured.
- **INA226 module shunt value** assumed 0.1 ohm; the Robu listing is out of stock and does not state it.
- **Optical and Hall sensor prices** (other than A3144) and the manometer cost are estimates.
- **MPXV5004DP** (the right range) was not found in stock in India in this search (Robu lists only a 3.3 V MP3V5004DP, out of stock).
- **Nut-tightening direction** and the compression-sleeve advice are engineering judgement, not from a source.
