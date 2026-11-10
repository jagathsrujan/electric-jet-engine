"""Blade centreline geometry for impeller draft 2 (pure maths, no SolidWorks).

Inputs from docs/parameters.md section 3. Coordinates in mm, axis on Z, sketch on the
Front plane (XY, normal +Z = inlet side). Rotation: counter-clockwise viewed from +Z.
Backward-curved: moving outward, the blade runs clockwise (against the rotation).
"""
import math

P = dict(D2=100.0, r1=24.0, beta1b=35.0, beta2b=45.0, Rb=61.3, t=1.7, t_LE=0.8,
         L_taper=8.0, Z=9, b1=10.0, b2=6.5, t_bp=3.0, d_h=20.0, d_bore=5.0, r_fillet=1.0)


def centre(p=P):
    """Arc centre so the centreline passes (r1, 0) at beta1b from the backward tangent."""
    b = math.radians(p["beta1b"])
    # outward blade direction at P1: (sin b, -cos b); centre on the side giving beta2b at r2
    cands = []
    for s in (1, -1):
        cx = p["r1"] + s * p["Rb"] * math.cos(b)
        cy = s * p["Rb"] * math.sin(b)
        cands.append((cx, cy))
    best = min(cands, key=lambda c: abs(angle_at(c, p["Rb"], p["D2"] / 2) - p["beta2b"]))
    return best


def angle_at(c, R, r):
    """Angle from tangent of a circle (centre c, radius R) where it crosses radius r."""
    d = math.hypot(*c)
    # angle between radius vector OP and CP: law of cosines; blade angle from tangent = 90 - that
    cos_opc = (r * r + R * R - d * d) / (2 * r * R)
    return math.degrees(math.acos(max(-1, min(1, cos_opc))))


def point_at_radius(c, R, r, near):
    """Intersection of circle (c,R) with circle (0,r) closest to point 'near'."""
    cx, cy = c
    d = math.hypot(cx, cy)
    a = (r * r - R * R + d * d) / (2 * d)
    h = math.sqrt(max(0.0, r * r - a * a))
    ux, uy = cx / d, cy / d
    pts = [(a * ux - h * uy, a * uy + h * ux), (a * ux + h * uy, a * uy - h * ux)]
    return min(pts, key=lambda q: math.hypot(q[0] - near[0], q[1] - near[1]))


if __name__ == "__main__":
    c = centre()
    R = P["Rb"]
    print("centre", c, "dist", math.hypot(*c))
    print("angle r1", angle_at(c, R, 24.0), "angle r2", angle_at(c, R, 50.0))
    print("TE point", point_at_radius(c, R, 50.0, (40, -30)))
