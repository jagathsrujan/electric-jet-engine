"""Independent cross-check of docs/parameters.md sections 2-5 (centrifugal blower v1).

Run:  python -I matlab/blower_crosscheck.py
Outputs (next to this file): blower_crosscheck.csv, blower_map.csv, blower_map.png

Only the section-1 targets are taken from docs/parameters.md. Everything else is
recomputed here from first principles. A few design CHOICES that are not targets
(and so cannot be derived from them) are listed in a separate, clearly marked block;
every one of them is an assumption *(interp.)*.
"""
import csv
import os
import sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
TOL = 0.02  # flag differences above 2 %

# ============================================================================
# INPUT BLOCK A: targets, copied from docs/parameters.md section 1 (decided)
# ============================================================================
MDOT = 0.030        # kg/s   air mass flow, design point (30 g/s)
RHO = 1.2           # kg/m^3 air density
DP_TT = 1500.0      # Pa     total pressure rise, design point (1.5 kPa)
D2 = 0.100          # m      impeller outer diameter (100 mm)
N_MAX = 15000.0     # rpm    maximum operating speed
# (Q = mdot/rho = 0.025 m^3/s is recomputed below, not copied.)

# ============================================================================
# INPUT BLOCK B: design choices NOT in section 1 *(interp.)*
# These are needed to close the problem and cannot be derived from the targets.
# They are my assumptions, chosen to match the machine type named in section 1
# (single stage, backward-curved, open impeller, spiral volute). Most coincide
# with values in parameters.md, so this check is independent only in the
# arithmetic and in Z, d1, b1, inlet angles, volute schedule, and the map.
# ============================================================================
ETA_TT = 0.55       # hydraulic total-to-total efficiency (doc sec 2) *(interp.)*
BETA2B = np.radians(45.0)   # exit blade angle from tangent *(interp.)*
B2 = 6.5e-3         # exit blade width, m *(interp.)*
T_BLADE = 1.7e-3    # blade thickness, m (printed, 4 x 0.42 mm lines) *(interp.)*
T_LE = 0.8e-3       # leading-edge effective thickness, m *(interp.)*
D_HUB = 20e-3       # hub boss diameter, m *(interp.)*
INCID = 3.0         # incidence allowance, deg *(interp.)*
R3_RATIO = 1.10     # volute base circle / r2 *(interp.)*
D_OUT = 38e-3       # volute outlet duct diameter, m (sets c_v) *(interp.)*
W_VOL = 28e-3       # volute axial width, m *(interp.)*
WALL = 2.4e-3       # casing wall, m *(interp.)*
NU_AIR = 1.5e-5     # kinematic viscosity, m^2/s *(interp.)*
A_SOUND = 343.0     # speed of sound at 20 C, m/s *(interp.)*
CD_ORIFICE = 0.62   # sharp-edged orifice discharge coefficient *(interp.)*
ETA_PESS = 0.40     # pessimistic overall efficiency (doc sec 5) *(interp.)*
RPM_TABLE = [6000, 9000, 11700, 12000, 15000]  # rows of doc section 5 table
T_CONV = np.pi / 30.0   # rpm -> rad/s

# ============================================================================
# Reference values copied from docs/parameters.md (for comparison only)
# key: (label, section, doc_value, unit, decimals printed in the doc)
# ============================================================================
DOC = {
    "eta_o": ("Overall efficiency", "2", 0.535, "-", 3),
    "sigma": ("Slip factor Wiesner", "2", 0.819, "-", 3),
    "sigma_S": ("Slip factor Stodola", "2", 0.753, "-", 3),
    "lambda": ("Work coefficient", "2", 0.605, "-", 3),
    "psi": ("Head coefficient", "2", 0.333, "-", 3),
    "phi": ("Flow coefficient", "2", 0.041, "-", 3),
    "cm2_u2": ("Cm2/U2", "2", 0.215, "-", 3),
    "Ns": ("Specific speed", "2", 0.92, "-", 2),
    "Ds": ("Specific diameter", "2", 3.76, "-", 2),
    "Mtip": ("Tip Mach, 15,000 rpm", "2", 0.23, "-", 2),
    "U2": ("Tip speed, design", "3", 61.3, "m/s", 1),
    "N_des": ("Design speed", "3", 11700, "rpm", -2),
    "U2max": ("Tip speed, 15,000 rpm", "3", 78.5, "m/s", 1),
    "Z": ("Number of blades (Pfleiderer raw)", "3", 9.5, "-", 1),
    "B2": ("Exit blockage factor", "3", 0.931, "-", 3),
    "Cm2": ("Exit meridional speed", "3", 13.1, "m/s", 1),
    "Cu2": ("Exit tangential speed", "3", 37.1, "m/s", 1),
    "c2": ("Exit absolute speed", "3", 39.3, "m/s", 1),
    "c2_angle": ("c2 flow angle from radial", "3", 70.5, "deg", 1),
    "W2": ("Exit relative speed", "3", 27.6, "m/s", 1),
    "beta2_act": ("Actual exit flow angle (tangent)", "3", 28.5, "deg", 1),
    "d1": ("Eye diameter (min W1s)", "3", 48, "mm", 0),
    "b1": ("Eye height b1", "3", 10, "mm", 0),
    "Cm1": ("Inlet meridional speed (blocked)", "3", 18.4, "m/s", 1),
    "Cm1_open": ("Inlet meridional speed (open)", "3", 16.7, "m/s", 1),
    "beta1h": ("Inlet blade angle, hub", "3", 61, "deg", 0),
    "beta1m": ("Inlet blade angle, rms", "3", 42, "deg", 0),
    "beta1s": ("Inlet blade angle, shroud", "3", 35, "deg", 0),
    "flow1h": ("Inlet flow angle, hub", "3", 57.6, "deg", 1),
    "flow1m": ("Inlet flow angle, rms", "3", 39.4, "deg", 1),
    "flow1s": ("Inlet flow angle, shroud", "3", 32.0, "deg", 1),
    "W1s": ("Inlet relative speed, shroud", "3", 34.7, "m/s", 1),
    "dehaller": ("De Haller W2/W1s", "3", 0.79, "-", 2),
    "A_t": ("Volute throat area", "4", 1134, "mm^2", 0),
    "c_v": ("Volute mean speed", "4", 22.0, "m/s", 1),
    "q_v": ("Volute dynamic pressure", "4", 292, "Pa", 0),
    "q_frac": ("q_v / dP_tt", "4", 0.19, "-", 2),
    "r3": ("Base circle radius", "4", 55, "mm", 0),
    "tongue_gap": ("Tongue radial clearance", "4", 5, "mm", 0),
    "casing_od": ("Casing outer diameter", "4", 195, "mm", 0),
    "P_euler": ("Euler power, design", "2", 68.2, "W", 1),
    "P_disc": ("Disc friction, design", "2", 1.9, "W", 1),
    "P_shaft": ("Shaft power, design", "5", 70, "W", 0),
    "dP_N15": ("dP at 15,000 rpm", "5", 2463, "Pa", 0),
    "N_stod": ("Req. rpm, Stodola slip, eta 0.55", "5", 12300, "rpm", -2),
    "N_e45": ("Req. rpm, Wiesner, eta_tt 0.45", "5", 12800, "rpm", -2),
    "N_e40": ("Req. rpm, Wiesner, eta_tt 0.40", "5", 13400, "rpm", -2),
    "N_worst": ("Req. rpm, Stodola, eta_tt 0.40", "5", 14100, "rpm", -2),
}
DOC_VOLUTE = {  # theta: (A mm^2, h mm, r_out mm)
    45: (142, 5.1, 60.1), 90: (284, 10.1, 65.1), 135: (425, 15.2, 70.2),
    180: (567, 20.2, 75.2), 225: (709, 25.3, 80.3), 270: (850, 30.4, 85.4),
    315: (992, 35.4, 90.4), 360: (1134, 40.5, 95.5)}
DOC_OP = {  # rpm: (U2, Q L/s, mdot g/s, dP Pa, P W, torque mNm, P_pess W, T_pess mNm)
    6000: (31.4, 12.8, 15.4, 394, 9, 15, 13, 20),
    9000: (47.1, 19.2, 23.1, 887, 32, 34, 43, 45),
    11700: (61.3, 25.0, 30.0, 1500, 70, 57, 94, 76),
    12000: (62.8, 25.6, 30.8, 1576, 75, 60, 101, 80),
    15000: (78.5, 32.0, 38.4, 2463, 147, 94, 197, 126)}
OP_COLS = ["U2 (m/s)", "Q (L/s)", "mdot (g/s)", "dP_tt (Pa)", "Shaft power (W)",
           "Torque (mN m)", "Power eta0.40 (W)", "Torque eta0.40 (mN m)"]
OP_DEC = [1, 1, 1, 0, 0, 0, 0, 0]

# ============================================================================
# Calculation
# ============================================================================
Q = MDOT / RHO
sb = np.sin(BETA2B)
tb = np.tan(BETA2B)
r2 = D2 / 2


def slip_wiesner(z):
    return 1 - np.sqrt(sb) / z**0.7


def slip_stodola(z):
    return 1 - np.pi * sb / z


def blockage2(z):
    return 1 - z * T_BLADE / (np.pi * D2 * sb)


def solve_speed(sigma, eta, z):
    """U2 from dP = eta*rho*U2*(sigma*U2 - Cm2/tan b); Cm2 is fixed by Q, independent of U2."""
    cm2 = Q / (np.pi * D2 * B2 * blockage2(z))
    k = cm2 / tb
    a = eta * RHO * sigma
    b = -eta * RHO * k
    u2 = (-b + np.sqrt(b * b + 4 * a * DP_TT)) / (2 * a)
    return u2, cm2


def disc_power(omega):
    """One-sided turbulent free-disc friction on the back plate (Cm = 0.0622 Re^-0.2)."""
    re = omega * r2**2 / NU_AIR
    cmom = 0.0622 * re**-0.2
    return 0.5 * cmom * RHO * omega**3 * r2**5


# ---- blade count / eye diameter / inlet: small fixed-point loop (Z <-> LE blockage) ----
Z = 9
for _ in range(6):
    sigma = slip_wiesner(Z)
    U2, Cm2 = solve_speed(sigma, ETA_TT, Z)
    omega = U2 / r2
    d_scan = np.linspace(30e-3, 70e-3, 40001)
    cm_open_scan = Q / (np.pi / 4 * (d_scan**2 - D_HUB**2))
    d1_open_opt = d_scan[np.argmin(np.hypot(cm_open_scan, omega * d_scan / 2))]
    cm_scan = cm_open_scan.copy()
    for _j in range(40):    # include leading-edge blockage in the scan
        fl_s = np.arctan(cm_scan / (omega * d_scan / 2))
        cm_scan = cm_open_scan / (1 - Z * T_LE / (np.pi * d_scan * np.sin(fl_s)))
    d1_opt = d_scan[np.argmin(np.hypot(cm_scan, omega * d_scan / 2))]
    d1 = round(d1_opt * 1000) / 1000        # whole mm *(interp.)*
    if len(sys.argv) > 1:                   # optional override: --d1 48 (mm), for sensitivity
        d1 = float(sys.argv[sys.argv.index('--d1') + 1]) / 1000
    r1s = d1 / 2
    cm1_open = Q / (np.pi / 4 * (d1**2 - D_HUB**2))
    cm1 = cm1_open
    for _i in range(50):                    # LE blockage at the shroud flow angle
        fl = np.arctan(cm1 / (omega * r1s))
        cm1 = cm1_open / (1 - Z * T_LE / (np.pi * d1 * np.sin(fl)))
    r_h = D_HUB / 2
    r_m = np.sqrt((r1s**2 + r_h**2) / 2)
    flow = {k: np.degrees(np.arctan(cm1 / (omega * r))) for k, r in
            (("h", r_h), ("m", r_m), ("s", r1s))}
    beta1m = flow["m"] + INCID
    z_pf = 6.5 * (r2 + r_m) / (r2 - r_m) * np.sin(np.radians((beta1m + 45.0) / 2))
    Z_new = int(2 * round((z_pf - 1) / 2) + 1)   # nearest odd integer
    if Z_new == Z:
        break
    Z = Z_new

sigma = slip_wiesner(Z)
sigma_S = slip_stodola(Z)
B2f = blockage2(Z)
U2, Cm2 = solve_speed(sigma, ETA_TT, Z)
N_des = U2 / r2 / T_CONV
omega = U2 / r2
Cu2 = sigma * U2 - Cm2 / tb
lam = Cu2 / U2
c2 = np.hypot(Cu2, Cm2)
W2 = np.hypot(Cm2, U2 - Cu2)
beta2_act = np.degrees(np.arctan2(Cm2, U2 - Cu2))
W1s = np.hypot(cm1, omega * r1s)
b1 = (d1**2 - D_HUB**2) / (4 * d1)
Pe = MDOT * lam * U2**2
Pd = disc_power(omega)
Pshaft = Pe + Pd
U2max = np.pi * D2 * N_MAX / 60
Ns = omega * np.sqrt(Q) / (DP_TT / RHO) ** 0.75
Ds = D2 * (DP_TT / RHO) ** 0.25 / np.sqrt(Q)


def req_rpm(sig, eta):
    u, _ = solve_speed(sig, eta, Z)
    return u / r2 / T_CONV


# volute (constant mean speed, rectangular section)
c_v = Q / (np.pi / 4 * D_OUT**2)
A_t = Q / c_v
r3 = R3_RATIO * r2
vol = []
for th in DOC_VOLUTE:
    A = A_t * th / 360
    h = A / W_VOL
    vol.append((th, A * 1e6, h * 1e3, (r3 + h) * 1e3))
r_out360 = r3 + A_t / W_VOL

vals = {
    "eta_o": Q * DP_TT / Pshaft, "sigma": sigma, "sigma_S": sigma_S, "lambda": lam,
    "psi": DP_TT / RHO / U2**2, "phi": Q / (U2 * D2**2), "cm2_u2": Cm2 / U2,
    "Ns": Ns, "Ds": Ds, "Mtip": U2max / A_SOUND, "U2": U2, "N_des": N_des,
    "U2max": U2max, "Z": z_pf, "B2": B2f, "Cm2": Cm2, "Cu2": Cu2, "c2": c2,
    "c2_angle": np.degrees(np.arctan2(Cu2, Cm2)), "W2": W2, "beta2_act": beta2_act,
    "d1": d1 * 1e3, "b1": b1 * 1e3, "Cm1": cm1, "Cm1_open": cm1_open,
    "beta1h": flow["h"] + INCID, "beta1m": beta1m, "beta1s": flow["s"] + INCID,
    "flow1h": flow["h"], "flow1m": flow["m"], "flow1s": flow["s"], "W1s": W1s,
    "dehaller": W2 / W1s, "A_t": A_t * 1e6, "c_v": c_v,
    "q_v": 0.5 * RHO * c_v**2, "q_frac": 0.5 * RHO * c_v**2 / DP_TT, "r3": r3 * 1e3,
    "tongue_gap": 0.05 * D2 * 1e3, "casing_od": 2 * (r_out360 + WALL) * 1e3,
    "P_euler": Pe, "P_disc": Pd, "P_shaft": Pshaft,
    "dP_N15": DP_TT * (N_MAX / N_des) ** 2,
    "N_stod": req_rpm(sigma_S, ETA_TT), "N_e45": req_rpm(sigma, 0.45),
    "N_e40": req_rpm(sigma, 0.40), "N_worst": req_rpm(sigma_S, 0.40),
}

# ---- system curve and operating points (blower curve intersect K Q^2) ----
K = DP_TT / Q**2
A2 = np.pi * D2 * B2 * B2f   # effective exit area
d_orifice = np.sqrt(4 / np.pi * Q * np.sqrt(RHO / (2 * DP_TT)) / CD_ORIFICE)


def blower_dp(q, n_rpm):
    u = np.pi * D2 * n_rpm / 60
    return np.maximum(0.0, ETA_TT * RHO * u * (sigma * u - q / (A2 * tb)))


def euler_power(q, n_rpm):
    u = np.pi * D2 * n_rpm / 60
    return RHO * q * u * (sigma * u - q / (A2 * tb))


def op_point(n_rpm):
    u = np.pi * D2 * n_rpm / 60
    bb = ETA_TT * RHO * u / (A2 * tb)
    cc = -ETA_TT * RHO * sigma * u**2
    q = (-bb + np.sqrt(bb * bb - 4 * K * cc)) / (2 * K)
    dp = K * q * q
    om = n_rpm * T_CONV
    p = euler_power(q, n_rpm) + disc_power(om)
    pp = q * dp / ETA_PESS
    return dict(rpm=n_rpm, U2=u, Q=q * 1e3, mdot=q * RHO * 1e3, dP=dp, P=p, T=p / om * 1e3,
                Ppess=pp, Tpess=pp / om * 1e3)


ops = [op_point(n) for n in RPM_TABLE]

# ============================================================================
# Comparison table
# ============================================================================
rows = []


def add(section, name, mine, doc, unit, dec):
    rel = (mine - doc) / doc
    rounding_ok = abs(mine - doc) <= 0.5 * 10.0 ** (-dec) + 1e-12
    rows.append(dict(section=section, item=name, mine=mine, doc=doc, unit=unit,
                     rel_pct=100 * rel, flag=abs(rel) > TOL, rounding=rounding_ok))


for key, (label, sec, dv, unit, dec) in DOC.items():
    add(sec, label, vals[key], dv, unit, dec)
for th, A, h, ro in vol:
    dA, dh, dro = DOC_VOLUTE[th]
    add("4", f"Volute {th} deg: A", A, dA, "mm^2", 0)
    add("4", f"Volute {th} deg: h", h, dh, "mm", 1)
    add("4", f"Volute {th} deg: r_out", ro, dro, "mm", 1)
for o in ops:
    d = DOC_OP[o["rpm"]]
    mine = [o["U2"], o["Q"], o["mdot"], o["dP"], o["P"], o["T"], o["Ppess"], o["Tpess"]]
    for c, m, dv, dec in zip(OP_COLS, mine, d, OP_DEC):
        add("5", f"{o['rpm']} rpm: {c}", m, dv, "", dec)


def fmt(x):
    return f"{x:.4g}" if abs(x) < 1e4 else f"{x:.0f}"


print(f"Inputs: mdot={MDOT*1e3:.0f} g/s rho={RHO} dP={DP_TT:.0f} Pa D2={D2*1e3:.0f} mm Nmax={N_MAX:.0f}")
print(f"Eye optimum: {d1_open_opt*1e3:.2f} mm without LE blockage, {d1_opt*1e3:.2f} mm with it")
print(f"Derived: Q={Q*1e3:.3f} L/s  Z={Z} (Pfleiderer raw {z_pf:.2f})  K={K:.3g}  "
      f"equivalent orifice d={d_orifice*1e3:.1f} mm (Cd {CD_ORIFICE})\n")
hdr = f"{'Sec':<3} {'Item':<42} {'Mine':>9} {'Doc':>9} {'Diff %':>8}  Flag"
print(hdr)
print("-" * len(hdr))
for r in rows:
    flag = ""
    if r["flag"]:
        flag = ">2%" + (" (within doc rounding)" if r["rounding"] else "")
    print(f"{r['section']:<3} {r['item']:<42} {fmt(r['mine']):>9} {fmt(r['doc']):>9} "
          f"{r['rel_pct']:>+8.2f}  {flag}")
nflag = sum(r["flag"] for r in rows)
nround = sum(r["flag"] and r["rounding"] for r in rows)
print(f"\n{len(rows)} items compared, {nflag} differ by more than 2 %, "
      f"{nround} of those are within the doc's printed rounding.")

with open(os.path.join(HERE, "blower_crosscheck.csv"), "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["section", "item", "this_script", "parameters_md", "unit", "diff_pct",
                "flag_gt_2pct", "within_doc_rounding"])
    for r in rows:
        w.writerow([r["section"], r["item"], f"{r['mine']:.6g}", f"{r['doc']:.6g}", r["unit"],
                    f"{r['rel_pct']:.3f}", int(r["flag"]), int(r["rounding"])])

# ============================================================================
# Performance map
# ============================================================================
speeds = list(range(6000, 15001, 1000))
cmap = plt.get_cmap("viridis")
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(9, 9), sharex=True)
map_rows = []
q_sys = np.linspace(0, 0.06, 300)
for i, n in enumerate(speeds):
    u = np.pi * D2 * n / 60
    q0 = sigma * u * A2 * tb   # zero-pressure flow
    q = np.linspace(0, q0, 120)
    dp = blower_dp(q, n)
    p = euler_power(q, n) + disc_power(n * T_CONV)
    col = cmap(i / (len(speeds) - 1) * 0.85)
    ls = "-" if n <= 12000 else "--"
    ax1.plot(q * RHO * 1e3, dp, ls, color=col, lw=1.6, label=f"{n:,} rpm")
    ax2.plot(q * RHO * 1e3, p, ls, color=col, lw=1.6)
    qo = op_point(n)
    ax1.plot(qo["mdot"], qo["dP"], "o", color=col, ms=5, mec="k", mew=0.6, zorder=5)
    ax2.plot(qo["mdot"], qo["P"], "o", color=col, ms=5, mec="k", mew=0.6, zorder=5)
    for qq, d_, pp in zip(q, dp, p):
        map_rows.append([n, qq * RHO * 1e3, qq * 1e3, d_, pp, ""])
    map_rows.append([n, qo["mdot"], qo["Q"], qo["dP"], qo["P"], "operating_point_on_system_curve"])
ax1.plot(q_sys * RHO * 1e3, K * q_sys**2, color="#d62728", lw=2.2,
         label=f"system curve dP = K Q^2\n(~{d_orifice*1e3:.0f} mm orifice)")
ax1.plot(MDOT * 1e3, DP_TT, "*", color="#d62728", ms=14, mec="k", zorder=6,
         label="design point (30 g/s, 1.5 kPa)")
ax1.set_ylabel("Total pressure rise dP_tt (Pa)")
ax1.set_ylim(0, 3200)
ax1.set_title("Blower v1 predicted map (1D model, constant eta_tt = 0.55; unverified)")
ax1.grid(alpha=0.3)
ax1.legend(fontsize=8, ncol=2, loc="upper right")
ax2.set_xlabel("Air mass flow (g/s)")
ax2.set_ylabel("Shaft power (W)  [Euler + disc friction]")
ax2.set_xlim(0, 75)
ax2.set_ylim(0, 400)
ax2.grid(alpha=0.3)
ax2.text(0.02, 0.92, "dashed: above the 12,000 rpm PLA recommended maximum;\n"
         "dots: intersection with system curve", transform=ax2.transAxes, fontsize=8, va="top")
fig.tight_layout()
fig.savefig(os.path.join(HERE, "blower_map.png"), dpi=150)

with open(os.path.join(HERE, "blower_map.csv"), "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["rpm", "mdot_g_per_s", "Q_L_per_s", "dP_tt_Pa", "shaft_power_W", "note"])
    for r in map_rows:
        w.writerow([r[0], f"{r[1]:.4f}", f"{r[2]:.4f}", f"{r[3]:.2f}", f"{r[4]:.3f}", r[5]])

print(f"\nOperating points on the system curve (K = {K:.3g} Pa/(m^3/s)^2):")
for n in speeds:
    o = op_point(n)
    print(f"  {o['rpm']:>6} rpm  mdot {o['mdot']:5.1f} g/s  dP {o['dP']:6.0f} Pa  P {o['P']:6.1f} W")
print(f"Zero-flow dP at design rpm: {float(blower_dp(0, N_des)):.0f} Pa")
print("Wrote blower_crosscheck.csv, blower_map.csv, blower_map.png in", HERE)
