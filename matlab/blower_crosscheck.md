# Blower cross-check: independent recomputation of parameters.md sections 2-5

Script: `matlab/blower_crosscheck.py` (Python/numpy/matplotlib; MATLAB not installed). Run with `python -I matlab/blower_crosscheck.py`. Outputs: `blower_crosscheck.csv` (112 compared items), `blower_map.csv`, `blower_map.png`. Nothing here is test-verified; it checks arithmetic and internal consistency of `docs/parameters.md`, not physical truth.

## Inputs

Block A, taken from `docs/parameters.md` section 1 (decided): mdot 30 g/s, rho 1.2 kg/m^3, dP_tt 1.5 kPa, D2 100 mm, N_max 15,000 rpm. Q = mdot/rho = 25 L/s is recomputed.

Block B, design choices that are not targets and cannot be derived from them (all *(interp.)*, and mostly the same values as the doc, so they are **not** independent):
- eta_tt 0.55 *(interp.)*; exit blade angle 45 deg *(interp.)*; exit width b2 6.5 mm *(interp.)*
- blade thickness 1.7 mm, LE thickness 0.8 mm, hub 20 mm, incidence 3 deg *(interp.)*
- volute: base circle 1.10 r2, outlet duct 38 mm (sets c_v), width 28 mm, wall 2.4 mm *(interp.)*
- viscosity 1.5e-5 m^2/s, speed of sound 343 m/s, orifice Cd 0.62, pessimistic eta_o 0.40 *(interp.)*

Independent (derived here, not copied): Z (Pfleiderer, nearest odd), eye diameter (scan for minimum shroud W1s), b1, inlet speeds and angles, U2 and design rpm, slip, triangles, disc friction, volute schedule, sensitivity speeds, operating points, performance map.

## Method

- Slip: Wiesner and Stodola. Exit: Cm2 = Q/(pi D2 b2 B2); Cu2 = sigma U2 - Cm2/tan(beta2b); lambda = Cu2/U2.
- Design speed: solve dP = eta_tt rho U2 (sigma U2 - Cm2/tan beta2b) (a quadratic in U2; Cm2 does not depend on U2).
- Inlet: Cm1 from the eye annulus with leading-edge blockage at the shroud flow angle (fixed-point iteration); angles beta = atan(Cm1/(omega r)) + 3 deg at hub (10 mm), rms (sqrt((r_h^2+r_s^2)/2)) and shroud. Z <-> blockage iterated until the odd count is stable.
- Power: Euler (mdot lambda U2^2) plus one-sided turbulent disc friction (Cm = 0.0622 Re^-0.2) on the back plate *(interp.)*. Torque = P/omega.
- Volute: constant mean speed c_v = Q/(pi/4 d_out^2); A(theta) = A_t theta/360; h = A/w; r_out = r3 + h.
- System curve: K = dP/Q^2 = 2.4e6 Pa/(m^3/s)^2; this equals a sharp-edged orifice of 32.0 mm at Cd 0.62 *(interp.)*.
- Map: dP(Q,N) = eta_tt rho U2 (sigma U2 - Q/(A2 tan beta2b)) with A2 = pi D2 b2 B2, i.e. constant eta_tt and constant sigma at all flows *(interp.)*; power = Euler + disc friction (disc friction scales as N^2.8, not N^3). Speeds 6,000-15,000 rpm in 1,000 rpm steps; speeds above 12,000 rpm dashed (PLA recommended limit). Operating points are the exact intersections with K Q^2.

## Key numbers (recomputed)

| Quantity | Value |
|---|---|
| U2 at design / N | 61.3 m/s / 11,707 rpm |
| sigma (Wiesner / Stodola) | 0.819 / 0.753 |
| lambda, psi, phi | 0.605, 0.333, 0.041 |
| Cm2, Cu2, c2, W2 | 13.15, 37.08, 39.34, 27.56 m/s; actual exit flow angle 28.5 deg |
| Ns, Ds | 0.92, 3.76 |
| Euler + disc = shaft power | 68.2 + 1.9 = 70.0 W; eta_o 0.535 |
| Required rpm, 4 sensitivity cases | 12,290 / 12,760 / 13,430 / 14,080 |
| Volute | c_v 22.0 m/s, A_t 1,134 mm^2, r_out(360) 95.5 mm, casing OD 195.8 mm |
| Operating points | 6,000 rpm: 15.4 g/s, 394 Pa, 9.5 W; 12,000: 30.8 g/s, 1,576 Pa, 75.4 W; 15,000: 38.4 g/s, 2,463 Pa, 147 W |
| Zero-flow dP at design rpm | 2,032 Pa (doc sec 8 predicts 1.7-2.0 kPa *(interp.)*; slightly above its upper end because eta_tt is held constant) |

## Result of the comparison

112 items compared; 100 agree within 2 % (most within 0.5 %). Sections 2, 4 (volute schedule) and 5 reproduce to rounding, which mainly confirms the doc is internally consistent and that the affinity laws reproduce an exact intersection of this model with K Q^2 (at constant eta and sigma they are exact except for disc friction).

## Differences above 2 %

| Item | This script | parameters.md | Diff | Likely cause |
|---|---|---|---|---|
| Eye diameter (scan optimum, rounded) | 47 mm (47.25 continuous; 46.4 without LE blockage) | 48 mm | -2.1 % | The minimum is very flat (doc itself says 47-48.5 within 1 %). I round the continuous optimum to the nearest mm; the doc evidently picked 48. Not a real disagreement. |
| Eye height b1 | 9.62 mm | 10 mm | -3.8 % | Follows from d1 = 47. Within doc rounding (rounds to 10). |
| Cm1 blocked / open | 19.29 / 17.60 m/s | 18.4 / 16.7 | +4.8 / +5.4 % | Follows from the smaller eye (47 vs 48 mm gives about 5 % less area). With d1 forced to 48 mm (`--d1 48`) Cm1 matches the doc. |
| Inlet flow angle, rms / shroud | 41.1 / 33.8 deg | 39.4 / 32.0 | +4.2 / +5.6 % | Same cause (d1 = 47 gives higher Cm1). |
| Inlet blade angle, rms / shroud | 44.1 / 36.8 deg | 42 / 35 | +4.9 / +5.1 % | Same cause. |
| Pfleiderer Z (raw) | 9.71 | 9.5 | +2.2 % | The doc does not state its r1 or beta1; I used rms r1 and beta1m. Both round to Z = 9, so the design is unchanged. |
| q_v / dP_tt | 0.194 | 0.19 | +2.3 % | Doc rounded 291.6/1500 = 0.194 to 0.19. Within rounding. |
| 6,000 rpm shaft power | 9.47 W | 9 W | +5.2 % | Doc used pure N^3 scaling from 70 W (9.4 W, printed as 9); I include the weaker Re dependence of disc friction. Within rounding. |
| 6,000 rpm pessimistic power | 12.6 W | 13 W | -2.9 % | Rounding of Q dP / 0.40 = 12.6 W (doc printed 13). Within rounding. |

With `--d1 48` the remaining flags are only: hub inlet angle (59.3 vs 61 deg blade, -2.8 %; flow angle 56.3 vs 57.6, -2.3 %), Pfleiderer Z (+2.05 %), and the three rounding items above. The hub-angle difference is not explained by d1: the doc's 57.6 deg at r = 10 mm would need Cm1 of about 19.3 m/s at the hub, which is higher than the stated 18.4 m/s shroud value. I could not reproduce it, so it is open: either the doc used a different hub Cm1 (for example more blockage at the hub) or a rounding slip. The doc uses 61 deg blade angle, which would make the hub blade about 2 deg too steep relative to a uniform Cm1 of 18.4 m/s. Small effect on performance (hub region carries little flow), but the CAD should use whichever value the designer confirms.

## Assumptions and caveats *(interp.)*

- All of block B above. The check is circular for those values: if eta_tt, beta2b, b2, Z, t are wrong, both calculations are wrong together.
- Constant eta_tt and sigma across the flow range *(interp.)*: real curves have efficiency falling away from design flow, and a stall or surge region near shutoff that this model does not show. The map is therefore optimistic at low flow and at the high-flow end. The shutoff pressure of 2.0 kPa at 11,700 rpm is the model's, not a measurement.
- Map curves end at zero pressure (free delivery); no impeller-inlet, volute, or incidence losses beyond the lumped 0.55.
- Disc friction is one-sided, hydraulically smooth, free-disc *(interp.)*; casing effects ignored.
- Incompressible, fixed density 1.2 kg/m^3, no heating or altitude correction.
- The 32 mm orifice equivalence depends on Cd = 0.62; the system curve itself (K) comes from the targets and does not depend on it.
- Not verified: no CFD, no test, no independent source for any correlation; the recomputation shares the doc's own correlations (Wiesner, Pfleiderer, disc friction), so it cannot detect a wrong model choice.
