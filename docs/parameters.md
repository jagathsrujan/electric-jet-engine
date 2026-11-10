# Design parameters: centrifugal blower v1

Single source of truth. CAD, simulation and MATLAB read their numbers from here; change this file first, then the model. Derivation and teaching are in `compressor-sizing.md`.

Status: preliminary 1D mean-line sizing, 2026-11-10. Nothing here is test-verified yet. *(interp.)* marks every assumed or estimated value. Values were computed with the scripts used for `compressor-sizing.md` (not stored in the repo), so they are consistent with each other.

Conventions: angles are measured from the **tangent** (blade moving direction), so 90 deg would be a radial blade and smaller means more backward curved. Pressures are total (stagnation) gauge pressures. Subscripts: 1 = impeller inlet (eye), 2 = impeller exit, s = shroud side, h = hub.

## 1. Targets (decided)

| Parameter | Symbol | Value | Unit | Note |
|---|---|---|---|---|
| Air mass flow, design point | mdot | 30 | g/s | Decided |
| Air density | rho | 1.2 | kg/m^3 | 20 C sea level; 35 C lab gives 1.15 (-4 % pressure at same rpm) *(interp.)* |
| Volume flow, design point | Q | 0.025 | m^3/s | mdot / rho |
| Total pressure rise, design point | dP_tt | 1.5 | kPa | Decided |
| Impeller outer diameter | D2 | 100 | mm | Decided |
| Maximum operating speed | N_max | 15,000 | rpm | Decided |
| Machine type | | single stage, backward-curved, open impeller with back plate, spiral volute, direct drive | | Decided |
| Fired thrust goal this supports | F | about 1.5 (150 g) | N | Reference build; implies nozzle exit speed about 50 m/s at 30 g/s *(interp.)* |
| Hot nozzle dynamic pressure | q_noz | about 0.5 | kPa | Hot gas 900 K, rho 0.39 kg/m^3 *(interp.)*; remaining about 1 kPa is the loss/margin budget *(interp.)* |

## 2. Efficiency and slip assumptions

| Parameter | Symbol | Value | Unit | Note |
|---|---|---|---|---|
| Hydraulic total-to-total efficiency | eta_tt | 0.55 | - | dP_tt / (rho lambda U2^2). Printed blowers: 0.40-0.60 *(interp.)* |
| Overall shaft-to-air efficiency | eta_o | 0.535 | - | Q dP_tt / shaft power, includes disc friction (computed) |
| Slip factor (Wiesner) | sigma | 0.819 | - | 1 - sqrt(sin beta2b) / Z^0.7 |
| Slip factor (Stodola, pessimistic) | sigma_S | 0.753 | - | 1 - pi sin beta2b / Z; used only for sensitivity |
| Work coefficient | lambda | 0.605 | - | Cu2 / U2 from the exit triangle |
| Head coefficient | psi_tt | 0.333 | - | (dP_tt/rho) / U2^2 |
| Flow coefficient | phi | 0.041 | - | Q / (U2 D2^2) |
| Meridional coefficient | Cm2/U2 | 0.215 | - | |
| Specific speed | Ns | 0.92 | - | omega sqrt(Q) / (dP/rho)^0.75 |
| Specific diameter | Ds | 3.76 | - | D2 (dP/rho)^0.25 / sqrt(Q); Cordier fit gives about 3.0 (+26 %), see sizing doc |
| Tip Mach number, 15,000 rpm | M_tip | 0.23 | - | Incompressible treatment is valid (density change under 2 %) |

## 3. Impeller

| Parameter | Symbol | Value | Unit | Note |
|---|---|---|---|---|
| Outer diameter | D2 | 100 | mm | |
| Tip speed, design point | U2 | 61.3 | m/s | At 11,700 rpm |
| Tip speed, 15,000 rpm | U2_max | 78.5 | m/s | |
| Exit blade width | b2 | 6.5 | mm | Clear passage height at exit |
| Number of blades | Z | 9 | - | Pfleiderer gives 9.5 *(interp.)*; odd count |
| Exit blade angle (from tangent) | beta2b | 45 | deg | Backward-curved |
| Blade thickness | t | 1.7 | mm | 4 perimeter lines of 0.42 mm *(interp.)* |
| Leading-edge effective thickness | t_LE | 0.8 | mm | Taper the first 8 mm of each blade *(interp.)* |
| Exit blockage factor | B2 | 0.931 | - | 1 - Z t / (pi D2 sin beta2b) |
| Exit meridional speed | Cm2 | 13.1 | m/s | |
| Exit tangential speed (absolute) | Cu2 | 37.1 | m/s | sigma U2 - Cm2 / tan beta2b |
| Exit absolute speed | c2 | 39.3 | m/s | Flow angle 70.5 deg from radial |
| Exit relative speed | W2 | 27.6 | m/s | Actual flow angle from tangent 28.5 deg (slip) |
| Eye (leading-edge) diameter | d1 | 48 | mm | Within 1 % of minimum shroud relative speed (optimum 47-48.5 mm) |
| Hub boss diameter | d_h | 20 | mm | Printed hub around a 5 mm shaft; wall 7.5 mm around the bore *(interp.)* |
| Shaft bore | d_bore | 5.0 | mm | Motor shaft 5 mm. Print 4.6 mm, ream to 5.0 *(interp.)*; fit a metal collet or screw to the motor bell, do not rely on a printed set-screw grip alone |
| Eye axial-to-radial height | b1 | 10 | mm | Continuity: pi d1 b1 = pi/4 (d1^2 - d_h^2) |
| Inlet meridional speed | Cm1 | 18.4 | m/s | At the shroud, with leading-edge blockage; 16.7 without |
| **Blade form (v1, decided 2026-11-10)** | | 2D prismatic, single circular arc | | Blades stand straight up from the back plate so the impeller prints without supports; no hub-to-shroud twist |
| Blade leading-edge radius | r1 | 24 | mm | At the eye radius, where the flow has turned radial; leading edge is a vertical line, full height b1 |
| Inlet blade angle at r1 (from tangent) | beta1b | 35 | deg | Flow angle 32.0 + 3 deg incidence *(interp.)* |
| Blade arc radius | R_b | 61.3 | mm | (r2^2 - r1^2) / (2 (r2 cos beta2b - r1 cos beta1b)); gives 35 deg at r1 and 45 deg at r2 |
| Reference only: twisted-blade inlet angles | | 59 / 42 / 35 | deg | Hub (r 10) / rms (r 18.4) / shroud (r 24) for a 3D inducer; not used in v1. Hub value corrected from 61 after the Windows cross-check (atan(18.4 / 12.26) + 3) |
| Inlet relative speed, shroud | W1s | 34.7 | m/s | |
| De Haller ratio | W2/W1s | 0.79 | - | Limit 0.7 for no blade stall |
| Back plate thickness | t_bp | 3 | mm | *(interp.)* |
| Blade axial tip clearance, nominal | eps | 0.5 | mm | Acceptable 0.3-0.8; eps/b2 = 7.7 % *(interp.)* |
| Impeller mass | m | about 50 | g | PLA, mostly solid *(interp.)* |
| Impeller moment of inertia | I | 5.5e-5 | kg m^2 | *(interp.)* |
| Print orientation | | back plate down, blades up | | Hoop stress then lies along the strong print direction |
| Residual imbalance target | | at most 1 | g mm | Static balance on a prop balancer; about G25 *(interp.)* |

## 4. Volute

| Parameter | Symbol | Value | Unit | Note |
|---|---|---|---|---|
| Type | | single spiral, constant mean speed, rectangular section | | |
| Base circle radius | r3 | 55 | mm | 1.10 r2 *(interp.)* |
| Tongue (cutwater) radius | r_t | 55 | mm | On the base circle |
| Tongue radial clearance | | 5 | mm | 5 % of D2; leave 4.8 mm after 0.1-0.2 mm rotor growth *(interp.)* |
| Tongue tip radius | | 1.5 | mm | *(interp.)* |
| Section width (axial) | w | 28 | mm | Back wall flush with the back plate; extra width is on the cover side *(interp.)* |
| Throat area (at 360 deg) | A_t | 1,134 | mm^2 | Q / c_v |
| Mean speed in volute | c_v | 22.0 | m/s | Dynamic pressure 292 Pa = 19 % of dP_tt |
| Outlet duct (round) | d_out | 38 | mm | Same area as the throat (28 x 40.5 mm rectangle transitions to 38 mm round over at least 40 mm) |
| Outlet duct speed | | 22.0 | m/s | |
| Casing outer diameter | | about 195 | mm | 2 (95.5 mm + 2.4 mm wall) |

Area schedule, A(theta) = A_t * theta / 360, h = A / w, outer radius r_out = r3 + h. Angle theta is measured from the tongue in the direction of rotation.

| Station | theta (deg) | A (mm^2) | h (mm) | r_out (mm) |
|---|---|---|---|---|
| 1 | 45 | 142 | 5.1 | 60.1 |
| 2 | 90 | 284 | 10.1 | 65.1 |
| 3 | 135 | 425 | 15.2 | 70.2 |
| 4 | 180 | 567 | 20.2 | 75.2 |
| 5 | 225 | 709 | 25.3 | 80.3 |
| 6 | 270 | 850 | 30.4 | 85.4 |
| 7 | 315 | 992 | 35.4 | 90.4 |
| 8 | 360 | 1,134 | 40.5 | 95.5 |

## 5. Operating points (fan affinity laws from the design point)

Valid only along the system curve dP = K Q^2, K = 2.4e6 Pa/(m^3/s)^2 (a fixed restriction, equal to a sharp-edged orifice of about 32 mm). Fixed density, efficiency assumed constant *(interp.)*. The pessimistic columns assume overall efficiency 0.40 at the same flow and pressure.

| rpm | U2 (m/s) | Q (L/s) | mdot (g/s) | dP_tt (Pa) | Shaft power (W) | Torque (mN m) | Power, eta 0.40 (W) | Torque, eta 0.40 (mN m) |
|---|---|---|---|---|---|---|---|---|
| 6,000 | 31.4 | 12.8 | 15.4 | 394 | 9 | 15 | 13 | 20 |
| 9,000 | 47.1 | 19.2 | 23.1 | 887 | 32 | 34 | 43 | 45 |
| 11,700 (design) | 61.3 | 25.0 | 30.0 | 1,500 | 70 | 57 | 94 | 76 |
| 12,000 | 62.8 | 25.6 | 30.8 | 1,576 | 75 | 60 | 101 | 80 |
| 15,000 | 78.5 | 32.0 | 38.4 | 2,463 | 147 | 94 | 197 | 126 |

Speed needed to reach 1.5 kPa at 30 g/s if the assumptions are wrong *(interp.)*:

| Case | Required rpm |
|---|---|
| Baseline: Wiesner slip, eta_tt 0.55 | 11,700 |
| Stodola slip, eta_tt 0.55 | 12,300 |
| Wiesner slip, eta_tt 0.45 | 12,800 |
| Wiesner slip, eta_tt 0.40 | 13,400 |
| Stodola slip, eta_tt 0.40 (worst case) | 14,100 |

## 6. Structural limits

Print values are conservative *(interp.)*; replace with coupon test results when available. Allowable = derated value to design against; ultimate = expected as-printed failure value.

| Parameter | PLA | PETG | Unit | Note |
|---|---|---|---|---|
| Density | 1,250 | 1,270 | kg/m^3 | |
| Young's modulus | 3.5 | 2.1 | GPa | *(interp.)* |
| Glass transition / soft limit | 55-60 | 75-80 | deg C | PLA creeps near a warm motor *(interp.)* |
| In-plane ultimate (as printed) | 40 | 32 | MPa | *(interp.)* |
| In-plane allowable | 30 | 24 | MPa | 0.6 x datasheet 50 / 40 *(interp.)* |
| Interlayer ultimate (across layers) | 12 | 15 | MPa | *(interp.)* |
| Interlayer allowable | 8 | 10 | MPa | *(interp.)* |
| Thin-ring bound rho U2^2 at 15,000 rpm | 7.7 | 7.8 | MPa | Upper bound, not the real peak |
| Disc hoop stress at 5 mm bore, 15,000 rpm | 6.5 | 6.6 | MPa | (3+nu)/4 rho U2^2, nu 0.35 |
| Design hoop stress, 15,000 rpm | 12.1 | 12.3 | MPa | x1.5 holes, x1.25 blade mass *(interp.)* |
| Safety factor on allowable, 15,000 rpm | 2.5 | 1.95 | - | Hoop stress governs |
| Safety factor on allowable, 12,000 rpm | 3.9 | 3.1 | - | |
| Blade-root interlayer shear, 15,000 rpm | 1.35 | 1.37 | MPa | Blade 1.6 g at 35 mm radius *(interp.)* |
| Safety factor on interlayer allowable, 15,000 rpm | 5.9 | 7.3 | - | |
| Radial rotor growth at tip, 15,000 rpm | 0.11 | 0.19 | mm | rho w^2 r^3 / E |
| Predicted burst speed | 27,000 | 24,000 | rpm | Hoop failure; plus or minus 30 % *(interp.)* |
| **Recommended maximum speed** | **12,000** | **14,000** | rpm | PLA limited by softening and creep, short runs (60 s or less); PETG provisional until spin test passes |
| Speed allowed after spin test passes | n/a | 15,000 | rpm | |
| Spin-test speed (1.2 x intended maximum) | 14,400 | 18,000 | rpm | 60 s hold, shielded |
| Burst-test acceptance | at least 22,500 | at least 22,500 | rpm | 1.5 x N_max *(interp.)* |

## 7. Motor requirement (no model chosen)

| Parameter | Value | Unit | Note |
|---|---|---|---|
| Working speed range, loaded | 6,000-15,000 | rpm | Variable by ESC; test sweeps start at 3,000 |
| No-load speed at supply voltage | at least 17,000 | rpm | Allows for 10-15 % load droop *(interp.)* |
| Shaft power at 15,000 rpm, expected | 147 | W | |
| Shaft power at 15,000 rpm, pessimistic | 197 | W | eta 0.40 |
| Shaft power at design point | 70 (94 pessimistic) | W | |
| Torque at 15,000 rpm, expected / pessimistic | 94 / 126 | mN m | Torque scales with rpm^2 |
| Torque at design point | 57 (76 pessimistic) | mN m | |
| Continuous rating (motor class) | at least 300 | W | 1.5 x pessimistic *(interp.)* |
| Electrical input at 15,000 rpm | about 185-250 | W | Shaft power / 0.8 combined motor and ESC efficiency *(interp.)* |
| Shaft | 5 mm | | |
| Mounting | outrunner bell or shaft adapter; bolt circle sets the minimum hub flange | | Hub 20 mm OD is a minimum; add a flange on the back plate if the bell screws sit outside it |
| Spin-up energy to 15,000 rpm | about 68 | J | 0.5 I w^2 |
