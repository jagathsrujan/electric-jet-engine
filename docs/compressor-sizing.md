# Compressor sizing: how the blower numbers were found

Preliminary 1D mean-line sizing of the centrifugal blower, 2026-11-10. All final numbers live in `parameters.md`; this file explains where they come from. Nothing is test-verified yet. *(interp.)* marks assumptions.

## 1. What the blower has to do

The engine has no turbine. The blower is the only thing that moves air, so it must do two jobs:

1. **Flow**: push enough air (mass flow, measured in g/s) to burn the fuel and make thrust.
2. **Pressure**: push it hard enough to overcome everything in the way: the duct, the holes in the combustion chamber liner, the flame holder, and finally the nozzle.

Flow and pressure trade against each other for a given blower and speed. Think of a hose: open the end fully and you get lots of flow but almost no pressure; block it and you get pressure but no flow. The blower's operating point is where its own curve meets the "system curve" of the engine (roughly pressure = K x flow squared).

The targets, and why:

- **Thrust**: the reference build made about 26 g cold and about 150 g fired. Thrust is momentum: F = mdot x v_exit. 150 g is 1.47 N, so at 30 g/s the exhaust must leave at about 49 m/s.
- **Mass flow 30 g/s** (0.025 m^3/s of air at 1.2 kg/m^3): a little above the reference build's 25 g/s, for margin.
- **Pressure 1.5 kPa**: the nozzle only needs the pressure that makes 50 m/s in hot gas: q = 0.5 x rho_hot x v^2 = 0.5 x 0.39 x 50^2 = about 0.5 kPa (hot gas at 900 K is about 0.39 kg/m^3 *(interp.)*). The other roughly 1 kPa is a budget for duct, liner and flame-holder losses that nobody knows yet *(interp.)*. 1.5 kPa is therefore generous; the margin is deliberate.

One consequence: with the open 50 mm nozzle of the reference build, 30 g/s needs only about 100 Pa (12.7 m/s). Cold, with no restriction, our blower would sit far to the right on its curve at high flow and low pressure. The bench test (section 8) therefore needs an adjustable restriction.

## 2. The chain: thrust to flow to pressure to tip speed to diameter and rpm to power

### 2.1 Pressure from speed: the fan equation

A spinning impeller throws air outward. The faster the rim moves, the more energy each kilogram of air gets. The key link is

    dP_tt = eta_tt x rho x lambda x U2^2

- U2 is the tip (rim) speed, U2 = pi x D2 x N / 60.
- lambda is the **work coefficient**: the fraction of U2^2 that the blades actually hand to the air as energy (explained in section 3).
- eta_tt is the **hydraulic efficiency**: the share of that energy that survives as useful total pressure; the rest is lost to friction, mixing, leakage over the blade tips and the volute.

Worked: lambda = 0.605 (section 3), eta_tt = 0.55, rho = 1.2, dP = 1500 Pa.
U2^2 = 1500 / (1.2 x 0.55 x 0.605) = 3,757, so **U2 = 61.3 m/s**.
For D2 = 0.100 m: N = 60 x 61.3 / (pi x 0.100) = **11,700 rpm**.
At the maximum 15,000 rpm U2 = 78.5 m/s, which is Mach 0.23, so air can be treated as incompressible (the pressure change is 1.5 % of atmospheric).

### 2.2 Power

    P_shaft = mdot x lambda x U2^2  +  P_disc friction
            = 0.030 x 0.605 x 61.3^2  +  about 2 W  =  68.2 + 1.9 = 70 W

The first term is the energy given to the air (the Euler work, section 3). Disc friction is the drag of the spinning back plate in the casing, estimated with a standard turbulent-disc coefficient. Overall efficiency, air power over shaft power: 1500 x 0.025 / 70 = 0.535. Torque = P / omega = 70 / 1226 rad/s = 57 mN m.

### 2.3 Scaling to other speeds: fan affinity laws

For the same blower on the same system curve:

    flow  Q ~ N        pressure  dP ~ N^2        power  P ~ N^3        torque ~ N^2

At 15,000 rpm: Q = 0.025 x 15000/11707 = 32 L/s (38 g/s), dP = 1500 x 1.28^2 = 2,463 Pa, P = 70 x 1.28^3 = 147 W. The laws assume constant efficiency and density, so treat them as good to perhaps +/-15 % *(interp.)*. A hot-day density of 1.15 gives 4 % less pressure at the same rpm (about 2 % more rpm to recover).

### 2.4 How much to trust 0.55

Printed blowers commonly reach only 40-60 %. The biggest single loss for an open impeller is air leaking over the blade tips: roughly 1-2 efficiency points per 1 % of (tip clearance / blade width) *(interp.)*, so 0.5 mm on 6.5 mm (7.7 %) costs about 8-15 points. The 0.55 assumes clearance is held near 0.5 mm. The sensitivity table shows how the required speed grows if the assumptions are optimistic:

| Case | Required rpm for 1.5 kPa at 30 g/s |
|---|---|
| Baseline: Wiesner slip, eta_tt 0.55 | 11,700 |
| Stodola slip, eta_tt 0.55 | 12,300 |
| Wiesner slip, eta_tt 0.45 | 12,800 |
| Wiesner slip, eta_tt 0.40 | 13,400 |
| Stodola slip, eta_tt 0.40 (worst case) | 14,100 |

Even the worst case fits under 15,000 rpm, with about 6 % to spare. If the bench test lands at that end, enlarge D2 (for example 110 mm) rather than spinning faster.

## 3. Velocity triangles and the Euler equation

A velocity triangle shows three speeds at one point in the impeller, related by: **absolute velocity c = blade speed U + relative velocity W**. U is the speed of the blade itself (circular motion), W is the air's speed as seen by someone riding on the blade, and c is what a bystander sees. Each is split into a **tangential** part (Cu, along the rotation) and a **meridional** part (Cm, the through-flow: radial at the exit, axial at the inlet).

**Euler turbomachinery equation.** Energy given to the air per kilogram = U2 x Cu2 - U1 x Cu1. Air enters the eye straight in (no swirl, Cu1 = 0), so the work is just **U2 x Cu2**. Therefore lambda = Cu2 / U2. Everything in the impeller design is about getting Cu2 large without wasting energy.

**Exit triangle, in words and sketch.** The blade tip moves at U2. The blade is curved backward, so the air leaves sliding along the blade, moving backward relative to the blade (W2), while being carried forward by the rim speed (U2). The vector sum c2 is mostly tangential, with a smaller radial part set by flow continuity.

                        C  fluid leaves the impeller here
                       /|\
              c2      / | \      W2
             39.3    /  |  \     27.6
                    /   |Cm2\
                   /    |13.1 \
                  /     |      \
                 O------+-------B  ---> blade moves this way
                 |<-Cu2=37.1->|<--Wu2=24.2-->|
                 |<--------- U2 = 61.3 ------>|
         angle at B between BO and W2 = 28.5 deg (actual flow)
         the blade itself is at 45 deg; the 16.5 deg gap is slip

**Continuity** fixes the radial speed: Cm2 = Q / (pi x D2 x b2 x B2). The blades themselves block part of the exit, B2 = 1 - Z t / (pi D2 sin beta2b) = 1 - 9 x 1.7 / (pi x 100 x 0.707) = 0.931. So Cm2 = 0.025 / (pi x 0.100 x 0.0065 x 0.931) = **13.1 m/s**.

**Slip.** The air does not follow the blade perfectly; between blades it lags, so Cu2 is less than the ideal. The slip factor sigma is the fraction retained. Wiesner's formula: sigma = 1 - sqrt(sin beta2b) / Z^0.7 = 1 - 0.841 / 4.66 = **0.819** (valid while r1/r2 stays under 0.527; ours is 0.48 at the shroud, 0.37 rms). Stodola's simpler formula gives 0.753 and is the pessimistic bound. Then

    Cu2 = sigma x U2 - Cm2 / tan(beta2b) = 0.819 x 61.3 - 13.1 / 1 = 37.1 m/s
    lambda = Cu2 / U2 = 0.605

(With Stodola lambda = 0.549.) This closes the loop with section 2.1, where lambda = 0.605 was used. Note that U2 and lambda depend on each other; they were solved together by iteration.

**What happens to c2.** The air leaves at c2 = 39.3 m/s, which carries 774 J/kg of kinetic energy, 34 % of the 2,273 J/kg Euler work. That is useful only if the volute slows the air down and turns it into pressure (section 5); the rest of the 0.55 efficiency is the cost of doing that imperfectly.

**Inlet triangle.** Air enters axially at Cm1 and meets the blade, moving at U1 = omega x r. U1 grows with radius, so the relative flow angle changes from hub to shroud: beta1 = atan(Cm1 / U1). Near the hub U is small and the angle is steep; at the outer edge of the eye U is high and the angle is shallow. The blade should be tilted to match, with about 3 deg extra as an incidence allowance *(interp.)*, otherwise the air hits the blade at an angle and separates.

## 4. Impeller geometry

| Item | Value | How it was found |
|---|---|---|
| D2 | 100 mm | Given; 61.3 m/s at 11,700 rpm |
| Eye diameter d1 | 48 mm | Scanning d1 for the lowest relative speed at the shroud, W1s = sqrt(Cm1^2 + U1s^2) (a big eye gives low Cm1 but high U1; a small eye the reverse). Minimum at 47-48.5 mm; first-pass 45-50 mm confirmed |
| Hub boss d_h | 20 mm | Smallest practical printed hub on a 5 mm shaft: 7.5 mm wall around the bore, room for a collet or the motor bell screws. Hub ratio d_h/d1 = 0.42, acceptable |
| Inlet height b1 | 10 mm | Continuity: eye area 1,495 mm^2 = pi x 48 x b1 |
| Inlet speed Cm1 | 18.4 m/s | 16.7 m/s open area, 18.4 with blade blockage at a leading edge tapered to 0.8 mm |
| Blade angle at inlet | 61 deg hub (r 10 mm), 42 deg rms (18.4 mm), 35 deg shroud (24 mm) | beta1 = atan(Cm1/U1) plus 3 deg |
| Exit width b2 | 6.5 mm | Sets Cm2 = 13.1 m/s; Cm1/Cm2 = 1.4 and de Haller W2/W1s = 0.79 (above 0.7, so no stall) |
| Blades | 9, 1.7 mm thick | Pfleiderer: Z = 6.5 (r2+r1)/(r2-r1) sin((beta1+beta2)/2) = 9.5. Thickness is 4 lines of a 0.4 mm nozzle |
| Exit angle beta2b | 45 deg backward | Backward-curved gives a stable curve and good efficiency; 50 deg would raise lambda by about 5 % but at the cost of more exit kinetic energy |

**Printable simplification.** A twisted blade (61 deg at the hub falling to 35 deg at the shroud) is ideal. A simple extruded 2-D blade is easier: place its leading edge at the eye radius (24 mm), where the flow is nearly radial, and give it 35 deg at the leading edge, curving to 45 deg at the exit. Expect modest incidence losses; this is the first thing to improve in v2.

**Hub and shaft.** The motor shaft is 5 mm. A printed hub with a plain bore and set-screw will creep and loosen (PLA and PETG both relax under clamping load and heat). Print the bore at 4.6 mm and ream to 5.0 mm with a drill (no lathe needed), then clamp with a metal collet/prop adapter, or bolt the back plate to the outrunner's bell. The 20 mm boss is a minimum; if the motor's bolt circle is wider, add a flange on the back plate.

**Tip clearance.** The open impeller leaks air from the high-pressure side back over the blade tops, so the gap between blade edge and cover matters. The H2D gives roughly +/-0.1-0.2 mm on a 100 mm part, and a flat 100 mm PLA plate can warp 0.2 mm, so a nominal **0.5 mm** (0.3-0.8 acceptable) is realistic; below 0.3 mm the blades will rub when the rotor grows 0.1-0.2 mm at speed or the printed parts warm up. Ways to hit it without a lathe: print the blades slightly tall and sand their tips flat by rubbing the impeller on sandpaper stuck to glass; set the gap with 0.1 mm shim washers between motor plate and housing; check with feeler gauges.

## 5. Volute

The volute is the spiral casing that collects air from the whole rim and delivers it to one outlet pipe. Its jobs: collect the flow, slow it down so kinetic energy becomes pressure, and keep the flow smooth.

**Sizing rule.** Choose one mean speed c_v for the whole spiral. At angle theta from the tongue, the volute has carried the flow from theta/360 of the rim, so its cross-section area is

    A(theta) = Q x (theta / 360) / c_v = A_t x theta / 360

Pick c_v = 22 m/s, the speed in the 38 mm outlet duct. That is well below the 39 m/s coming off the impeller, so the volute slows the air by 44 %, recovering pressure. Then A_t = 0.025 / 22 = 1,134 mm^2 (a 38 mm round duct). Dynamic pressure at 22 m/s is 292 Pa, 19 % of the total, so the outlet duct size is not free: a smaller duct would make speed and loss climb quickly. A short conical diffuser (included angle 10 deg or less) afterwards recovers a little more if the combustor inlet is wider.

**Cross-section.** Use a rectangle of constant axial width w = 28 mm (back wall flush with the back plate, extra width on the cover side), with h = A / w growing from 0 to 40.5 mm. Base circle r3 = 55 mm. The eight stations are in `parameters.md` section 4: for example 90 deg gives A = 284 mm^2, h = 10.1 mm, r_out = 65.1 mm; 360 deg gives 1,134 mm^2, h = 40.5 mm, r_out = 95.5 mm. A free-vortex schedule (speed falling as 1/r) is equivalent in principle and would give a slightly smaller spiral (r_out about 89 mm at 360 deg, from conserving angular momentum with Cu2 r2 = 1.86 m^2/s). Constant speed was chosen as easier to explain and draw. Round the section's inner corners with 3-5 mm fillets, and flare the wall smoothly from the 7 mm impeller gap to the 28 mm width.

**Tongue.** The tongue is where the spiral closes on itself. A very small gap to the impeller gives a little more pressure but a loud whistle at blade-passing frequency (9 x 250 Hz = 2.25 kHz at 15,000 rpm). A bigger gap is quieter and more forgiving. Use a **5 mm radial gap (5 % of D2)**, tip radius 1.5 mm. After 0.1-0.2 mm rotor growth it is still 4.8 mm.

## 6. Stress and safety

A printed impeller fails differently from a metal one. The material is weakest across layers and softens when warm. The load comes from the spinning rim: it tries to stretch the plate (hoop stress) and fling each blade outward.

- **Thin-ring bound.** rho x U2^2 = 1250 x 78.5^2 = 7.7 MPa at 15,000 rpm for PLA (7.8 for PETG). This is the stress in a free ring, an upper bound for the plain plate.
- **Plate with a small bore.** Disc theory gives (3+nu)/4 x rho x U2^2 = 6.5 MPa at the 5 mm bore (nu = 0.35). The first-pass 7.7 MPa is thus the right order of magnitude and slightly conservative for the plain plate.
- **Design stress.** Real peaks are higher: screw holes and the bore (x1.5) and the mass of the blades pulling on the rim (x1.25) *(interp.)*. Design hoop stress = 6.5 x 1.5 x 1.25 = **12.1 MPa** (PLA), 12.3 (PETG) at 15,000 rpm.
- **Blade root.** Each blade (1.6 g at 35 mm radius) pulls with 138 N at 15,000 rpm, carried as shear between layers over its 60 x 1.7 mm base: **1.35 MPa**. This is the weak-layer-adhesion check.

| Check at 15,000 rpm | PLA | PETG |
|---|---|---|
| In-plane stress / allowable (0.6 x datasheet: 30 / 24 MPa) | 12.1 / 30: **SF 2.5** | 12.3 / 24: **SF 1.95** |
| Blade-root shear / interlayer allowable (8 / 10 MPa) | 1.35 / 8: SF 5.9 | 1.37 / 10: SF 7.3 |
| Softening temperature | 55-60 C | 75-80 C |
| Rotor growth at tip | 0.11 mm | 0.19 mm |

Print the impeller back plate down with blades up, so the hoop stress lies along the strong print direction. Use at least 4-5 perimeters and 100 % infill on the plate and hub, dry filament, and the top end of the nozzle temperature range for layer bonding.

**Recommended maximum speed.** Stress alone allows PLA about 13,600 rpm at safety factor 3. But PLA softens at 55-60 C and creeps under load; an outrunner and its hub warm up. Recommend **PLA: 12,000 rpm, runs of 60 s or less, hub temperature below 45 C.** That is only 2.5 % above the design point, so a PLA prototype can map the curve but may not reach 1.5 kPa if efficiency is poor. **PETG: 14,000 rpm** (safety factor 2.2) until a spin test passes, then up to the 15,000 rpm target. These are judgments based on assumed print strengths, not test data.

**Predicted burst.** Hoop failure at about 27,000 rpm (PLA) and 24,000 rpm (PETG), plus or minus 30 %.

**Spin and burst test recommendation.**
1. Print three impellers in each material with identical settings; tag them.
2. Spin test (proof): spin one to 1.2 x its intended maximum (PLA 14,400, PETG 18,000 rpm), hold 60 s. Pass: no cracks or delamination, tip diameter grows by less than 0.3 mm, no vibration change.
3. Burst test on a sacrificial one: step up 1,000 rpm at a time to failure. Acceptance: at least 22,500 rpm (1.5 x N_max). If the motor and ESC cannot reach that, stop at the proof speed.
4. Do both behind a shield (for example a steel box or thick polycarbonate), run remotely, nobody in the plane of the rotor. PLA shatters; a 10 g fragment at 80 m/s carries about 32 J.
5. Balance every impeller on a prop balancer before spinning to a residual of 1 g mm or less (about G25).

## 7. Predicted performance

At the design point and four requested speeds, from the affinity laws. "Pessimistic" assumes overall efficiency 0.40 at the same flow and pressure.

| rpm | U2 (m/s) | Q (L/s) | mdot (g/s) | dP_tt (Pa) | Shaft power (W) | Torque (mN m) | Power, eta 0.40 (W) | Torque, eta 0.40 (mN m) |
|---|---|---|---|---|---|---|---|---|
| 6,000 | 31.4 | 12.8 | 15.4 | 394 | 9 | 15 | 13 | 20 |
| 9,000 | 47.1 | 19.2 | 23.1 | 887 | 32 | 34 | 43 | 45 |
| 11,700 (design) | 61.3 | 25.0 | 30.0 | 1,500 | 70 | 57 | 94 | 76 |
| 12,000 | 62.8 | 25.6 | 30.8 | 1,576 | 75 | 60 | 101 | 80 |
| 15,000 | 78.5 | 32.0 | 38.4 | 2,463 | 147 | 94 | 197 | 126 |

If efficiency and slip turn out at the pessimistic end (eta_tt 0.40, Stodola), pressures are about 0.69 times these (for example 1,700 Pa at 15,000 rpm). At low speed (6,000 rpm) the real efficiency is lower than assumed because the flow is less turbulent and clearance leakage matters more; expect the 6,000 rpm row to be optimistic.

**Motor consequence.** Speed range 6,000-15,000 rpm with no-load speed of at least 17,000 rpm; shaft power 147 W expected and 197 W pessimistic at 15,000 rpm; torque 94-126 mN m. A continuous rating of 300 W or more gives margin. The first-pass "300 W class" is retained. The motor must be controllable down to about 3,000 rpm for test sweeps.

## 8. What the bench test of v1 should measure

The test compares measured numbers against section 7.

1. **Rig.** Blower outlet to a straight 38 mm pipe at least 10 diameters long, ending in an adjustable restriction (a sliding plate, or interchangeable orifice plates; about 32 mm diameter represents the engine at 1.5 kPa and 25 L/s, and a fully open pipe gives the high-flow end *(interp.)*). The cold 50 mm nozzle alone is not a representative load.
2. **Measure at each throttle setting, at 6,000, 9,000 and 12,000 rpm (15,000 only for PETG after its spin test):**
   - speed (hall or optical pickup, or ESC telemetry);
   - static pressure in the pipe against ambient (U-tube water manometer, 1.5 kPa is about 150 mm of water, or a +/-5 kPa differential sensor);
   - flow: pitot traverse in the straight pipe, or calibrated orifice;
   - electrical input power (supply voltage x current);
   - ambient pressure and temperature (for density), motor and hub temperature.
3. **Compute:** total pressure (static plus 0.5 rho v^2), shaft power (electrical power x about 0.8 for motor and ESC *(interp.)*), overall efficiency Q dP / P_shaft.
4. **Compare:** pressure and power at design flow against section 7. Acceptance: total pressure within +/-25 % of prediction and a measured speed for 1.5 kPa at 30 g/s of 13,500 rpm or lower. Also check that points at 6,000, 9,000 and 12,000 rpm fall on the same normalised curve (dP/N^2 against Q/N); if they do, the affinity laws hold and the extrapolation to 15,000 rpm is credible.
5. **Also record:** pressure at zero flow (predicted about 1.7-2.0 kPa at 11,700 rpm *(interp.)*, a direct check of the slip assumption); tip clearance before and after; vibration and noise; whether the impeller or the volute tongue rubs; any hot spots.
6. **Update `parameters.md`** with the measured eta, sigma and the real speed needed, and re-size if the speed for 1.5 kPa exceeds the recommended limit for the material.

## 9. Specific speed check (Cordier)

Specific speed Ns = omega sqrt(Q) / (dP/rho)^0.75 = 1226 x 0.1581 / 1250^0.75 = 0.92, and specific diameter Ds = D2 (dP/rho)^0.25 / sqrt(Q) = 0.1 x 5.946 / 0.1581 = 3.76. Ns near 1 is squarely the radial-impeller range, so a centrifugal blower is the right choice (axial machines sit above about 3). The Cordier line is an empirical envelope of best-efficiency machines; a common fit is Ds = 2.8 Ns^-0.8, giving 3.0 at Ns = 0.92. Our impeller is 26 % larger than the Cordier optimum at this speed (79 mm) because Cordier machines are loaded harder (head coefficient 0.53 versus our 0.33), which only works with efficiencies above 80 %. Ours is deliberately larger, slower and more lightly loaded, matching the low efficiency expected from a printed open impeller. A 65 mm impeller at 15,000 rpm would sit on the Cordier line, but its exit passages would be only about 4-5 mm *(interp.)*, so a 0.5 mm clearance would be over 10 % of the width, which does not suit FDM, and the stress would be harder to carry. The fit has a wide band (+/-20 %), so treat this as a plausibility check, not proof.

## 10. Where this differs from the first-pass hand estimate

| First pass | Result here |
|---|---|
| 61 m/s, 11,700 rpm | Confirmed: 61.3 m/s, 11,707 rpm. Added the sensitivity: up to 14,100 rpm if slip and efficiency are at the pessimistic end |
| About 2.4 kPa at 15,000 rpm | 2.46 kPa: rounding only |
| About 70 W design, 140 W at 15,000 rpm | 70 W confirmed (68.2 W Euler + 1.9 W disc friction); 147 W at 15,000 rpm; pessimistic 197 W |
| Motor about 300 W | Retained, now stated as shaft rating at 1.5 x pessimistic power |
| Eye 45-50 mm | 48 mm confirmed by minimum W1s; hub 20 mm; blade angles at hub 61 deg, shroud 35 deg added |
| b2 6-7 mm, 8-10 blades, 45-50 deg, 1.6-2 mm | b2 6.5, Z = 9, 45 deg (low end), 1.7 mm; leading edge taper to 0.8 mm added, because otherwise blockage raises inlet speed to 20.4 m/s and the diffusion ratio gets worse |
| Outlet 38 mm, 22 m/s | Arithmetic confirmed; but 22 m/s is 19 % of the pressure rise, so the duct size is tied to the volute throat and a diffuser may be needed |
| Rim stress about 7.7 MPa | A bound; plate theory gives 6.5 MPa, design value with holes and blades 12.1 MPa. The real limits are layer adhesion, creep and PLA softening, which set the recommended speeds (PLA 12,000, PETG 14,000 rpm provisional) |

## 11. Not verified

- No CFD, no test. Slip (Wiesner), efficiency 0.55, disc friction and the Cordier fit are textbook correlations, normally calibrated on metal machines.
- Print strengths and interlayer values are conservative typical numbers, not measured on this printer and filament.
- Hot-gas numbers (900 K, 50 m/s) and the 1 kPa loss budget are guesses until the combustor exists.
- The volute is sized by a simple 1D rule; its real efficiency and the 5 mm tongue effect are unknown.
- Burst speed estimate is hoop-only, plus or minus 30 %.
- No motor chosen; the hub flange depends on its bolt circle.

## Key checks

- Q = 0.025 m^3/s, mdot = 30 g/s, dP_tt = 1.5 kPa at 11,700 rpm, U2 = 61.3 m/s.
- At 15,000 rpm: U2 = 78.5 m/s, dP about 2.46 kPa, 147 W (197 W pessimistic), 94 mN m.
- Exit triangle: Cm2 = 13.1, Cu2 = 37.1, W2 = 27.6, c2 = 39.3 m/s; lambda = 0.605, sigma = 0.819; blade 45 deg, flow 28.5 deg.
- D2 100 mm, b2 6.5 mm, Z = 9, t 1.7 mm, eye 48 mm, hub 20 mm, shaft bore 5.0 mm.
- Blade inlet angles 61 deg hub, 42 deg rms, 35 deg shroud; de Haller 0.79 (at least 0.7).
- Volute throat 1,134 mm^2 = 38 mm round at 22 m/s; r3 = 55 mm, w = 28 mm, r_out 95.5 mm at 360 deg; tongue gap 5 mm.
- Tip clearance 0.5 mm nominal (0.3-0.8); rotor growth 0.11 mm (PLA) / 0.19 mm (PETG) at 15,000 rpm.
- Hoop stress 6.5 MPa plate, 12.1 MPa design; SF 2.5 (PLA) and 1.95 (PETG) at 15,000 rpm.
- Recommended maximum: PLA 12,000 rpm (60 s runs), PETG 14,000 rpm until spin test passes; burst at least 22,500 rpm.
- Ns = 0.92, Ds = 3.76 (Cordier about 3.0); radial impeller is the right type.
- Motor: 6,000-15,000 rpm, no-load at least 17,000 rpm, at least 300 W continuous, 94-126 mN m at 15,000 rpm.
- Bench test: pressure within +/-25 % of Section 7 and 1.5 kPa reached at 13,500 rpm or lower.
