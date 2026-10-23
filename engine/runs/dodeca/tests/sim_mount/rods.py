"""H2 (a): which straight rods pass through each opposite hole pair.

Method (exact for a rigid straight prism-shaped rod): a rod of cross-section S and direction u
passes through the object iff S, placed in the plane perpendicular to u, does not meet the
projection of the solid along u. So the 'see-through' region = disk minus the union of all
projected triangles; the largest round rod = maximum inscribed circle of the see-through
component on the axis; the largest square rod = largest square inside it (erosion test).
The direction u is optimised within 8 deg of the pair axis (the faces are not exactly parallel).

Validated in validate_rods.py on synthetic meshes with known holes (coaxial, offset, oval).

Also: idealised Jublains (Sparavigna 2012 table) and Newhall (21 x 26 ovals) cases, and the
tapered-rod seating rule.
"""
import numpy as np
import shapely
from shapely.geometry import Point, Polygon
from shapely import affinity
from concurrent.futures import ProcessPoolExecutor
from common import load_scan_mm, load_json, save_json

R_LIM = 16.0


def basis(u):
    a = np.array([1.0, 0, 0]) if abs(u[0]) < 0.9 else np.array([0, 1.0, 0])
    e1 = np.cross(u, a); e1 /= np.linalg.norm(e1)
    return e1, np.cross(u, e1)


def see_through(T, u, r_lim=R_LIM):
    """T: (F,3,3) triangles relative to the object centre. Returns the see-through polygon
    component nearest the axis through the centre (or None)."""
    e1, e2 = basis(u)
    xy = np.stack([T @ e1, T @ e2], -1)
    near = np.min(np.linalg.norm(xy, axis=2), axis=1) < r_lim + 2
    xy = xy[near]
    area = 0.5 * np.abs((xy[:, 1, 0] - xy[:, 0, 0]) * (xy[:, 2, 1] - xy[:, 0, 1]) -
                        (xy[:, 2, 0] - xy[:, 0, 0]) * (xy[:, 1, 1] - xy[:, 0, 1]))
    xy = xy[area > 1e-8]
    polys = shapely.polygons(np.concatenate([xy, xy[:, :1]], 1))
    fp = shapely.union_all(polys)
    free = Point(0, 0).buffer(r_lim, quad_segs=128).difference(fp)
    geoms = list(getattr(free, "geoms", [free]))
    geoms = [g for g in geoms if g.area > 0.5]
    if not geoms:
        return None
    g = min(geoms, key=lambda g: g.distance(Point(0, 0)))
    if g.distance(Point(0, 0)) > 4:
        return None
    return g


def mic(poly):
    c = shapely.maximum_inscribed_circle(poly, tolerance=0.005)
    return 2 * c.length, np.asarray(c.coords[0])


def largest_square(poly, n_ang=45):
    """Largest square inside a (near-convex) polygon: for each angle, bisection on side s with
    the erosion = intersection of the polygon translated by the 4 corner offsets."""
    best = (0.0, 0.0)
    for th in np.linspace(0, 90, n_ang, endpoint=False):
        P = affinity.rotate(poly, -th, origin=(0, 0))
        lo, hi = 0.0, 2 * np.sqrt(P.area)
        for _ in range(30):
            s = 0.5 * (lo + hi); h = s / 2
            E = P
            for dx, dy in ((h, h), (h, -h), (-h, h), (-h, -h)):
                E = E.intersection(affinity.translate(P, -dx, -dy))
                if E.is_empty:
                    break
            if E.is_empty or E.area < 1e-8:
                hi = s
            else:
                lo = s
        if lo > best[0]:
            best = (lo, th)
    return best


def contact_points(poly, centre, d, tol=0.03):
    xy = np.asarray(poly.exterior.coords)
    # densify
    pts = []
    for a, b in zip(xy[:-1], xy[1:]):
        k = max(2, int(np.linalg.norm(b - a) / 0.05))
        pts.append(a + (b - a) * np.linspace(0, 1, k)[:, None])
    pts = np.vstack(pts)
    r = np.linalg.norm(pts - centre, axis=1)
    on = pts[r < d / 2 + tol]
    if len(on) == 0:
        return []
    ang = np.degrees(np.arctan2(on[:, 1] - centre[1], on[:, 0] - centre[0])) % 360
    ang = np.sort(ang)
    groups = [[ang[0]]]
    for a in ang[1:]:
        if a - groups[-1][-1] < 8:
            groups[-1].append(a)
        else:
            groups.append([a])
    if len(groups) > 1 and (groups[0][0] + 360 - groups[-1][-1]) < 8:
        groups[0] = groups[-1] + groups[0]; groups.pop()
    return [float(np.mean(g) % 360) for g in groups]


def tilt_dirs(axis, tilts, n_az):
    e1, e2 = basis(axis)
    out = []
    for t in tilts:
        if t == 0:
            out.append(axis.copy()); continue
        for az in np.linspace(0, 2 * np.pi, n_az, endpoint=False):
            v = np.cos(np.radians(t)) * axis + np.sin(np.radians(t)) * (np.cos(az) * e1 + np.sin(az) * e2)
            out.append(v / np.linalg.norm(v))
    return out


_T = None


def _init(T):
    global _T
    _T = T


def _eval(u):
    g = see_through(_T, np.asarray(u))
    if g is None:
        return 0.0, None
    d, c = mic(g)
    return d, (np.asarray(g.exterior.coords), c)


def best_rod(T, axis, pool):
    dirs = tilt_dirs(axis, [0, 1, 2, 3, 4, 6, 8], 12)
    res = list(pool.map(_eval, [d.tolist() for d in dirs]))
    k = int(np.argmax([r[0] for r in res]))
    u = dirs[k]
    # local refinement
    for step in (0.5, 0.25, 0.1):
        cand = [u] + tilt_dirs(u, [step], 8)[1:]
        rr = list(pool.map(_eval, [d.tolist() for d in cand]))
        j = int(np.argmax([r[0] for r in rr]))
        if rr[j][0] > res[k][0]:
            u = cand[j]; res[k] = rr[j]
    d_axis = res[0][0]
    return dict(d_best=res[k][0], u_best=u, tilt_best_deg=float(np.degrees(np.arccos(np.clip(u @ axis, -1, 1)))),
                d_along_axis=d_axis, poly=Polygon(res[k][1][0]), centre=res[k][1][1])


# ----------------------------------------------------------------- idealised published pieces
def ellipse(a_full, b_full, angle=0.0, centre=(0, 0)):
    e = Point(0, 0).buffer(0.5, quad_segs=256)
    e = affinity.scale(e, a_full, b_full)
    e = affinity.rotate(e, angle, origin=(0, 0))
    return affinity.translate(e, *centre)


def published_cases():
    out = {}
    # Jublains poles 26 x 21.5 and 25.5 x 21.5 (Sparavigna 2012 Table, from Guillier et al. 2008);
    # relative orientation of the two ovals and centre offsets are unpublished -> swept.
    for rel in (0, 30, 60, 90):
        for off in (0.0, 1.0, 2.0):
            P = ellipse(26.0, 21.5).intersection(ellipse(25.5, 21.5, rel, (off, 0)))
            d, c = mic(P)
            s, th = largest_square(P, 30)
            out[f"Jublains_pole rel{rel}deg off{off}mm"] = dict(d_round=d, square_side=s)
    # Newhall: two ovals 21 x 26 (Guggenberger, via evidence FACT 3)
    for rel in (0, 90):
        P = ellipse(26.0, 21.0).intersection(ellipse(26.0, 21.0, rel))
        d, c = mic(P); s, th = largest_square(P, 30)
        out[f"Newhall_pole rel{rel}deg"] = dict(d_round=d, square_side=s)
    # Jublains ringed pairs (A_i <-> B_{4-i}); coaxial circles -> min diameter
    A = [21.5, 16.5, 21.0, 11.5, 17.0]; B = [10.5, 15.5, 22.0, 17.0, 22.0]
    for i in range(5):
        da, db = A[i], B[4 - i]
        out[f"Jublains_ring pair {da}/{db}"] = dict(d_round=min(da, db), square_side=min(da, db) / np.sqrt(2))
    return out


def taper_rule(d_low, d_up, L):
    """Rod entering from below through the hole of aperture d_low, towards d_up at distance L.
    Returns k* = (d_low - d_up)/L: taper (diameter per length) that seats in both holes at once;
    gentler tapers jam in the upper hole only, steeper ones in the lower hole only."""
    return (d_low - d_up) / L


def main(name="saalburg"):
    print("=== scan:", name)
    g = load_json(f"scan_geometry_{name}.json")
    m = load_scan_mm(name)
    c = np.asarray(g["centre"]); N = np.asarray(g["normals"]); opp = g["opposite"]
    h_out = np.asarray(g["h_out"]); t = np.asarray(g["wall_t_plane"])
    T = m.vertices[m.faces] - c
    holes = g["holes"]
    rows = []
    pairs = sorted({tuple(sorted((i, opp[i]))) for i in range(12)})
    with ProcessPoolExecutor(max_workers=14, initializer=_init, initargs=(T,)) as pool:
        for (i, j) in pairs:
            axis = N[i] - N[j]; axis /= np.linalg.norm(axis)
            r = best_rod(T, axis, pool)
            s_side, s_ang = largest_square(r["poly"])
            wmin = min(np.ptp(np.asarray(r["poly"].exterior.coords) @ np.array([np.cos(a), np.sin(a)]))
                       for a in np.linspace(0, np.pi, 180, endpoint=False))
            cp = contact_points(r["poly"], r["centre"], r["d_best"])
            L = h_out[i] + h_out[j] - 0.5 * (t[i] + t[j])
            di, dj = holes[i]["d_mic"], holes[j]["d_mic"]
            row = dict(pair=(i, j), d_i=di, d_j=dj, ell_i=(holes[i]["ell_major"], holes[i]["ell_minor"]),
                       ell_j=(holes[j]["ell_major"], holes[j]["ell_minor"]),
                       rod_round_along_axis=r["d_along_axis"], rod_round_best=r["d_best"],
                       best_tilt_deg=r["tilt_best_deg"], square_side=s_side, see_through_width_min=wmin,
                       see_through_area=r["poly"].area, n_contacts=len(cp), contact_angles=cp,
                       L_midwall=L, taper_both_seat_k=abs(di - dj) / L,
                       taper_half_angle_deg=float(np.degrees(np.arctan(abs(di - dj) / (2 * L)))))
            rows.append(row)
            print("pair %2d-%2d  holes %.2f/%.2f  round rod along axis %.2f, best %.2f (tilt %.1f deg)  "
                  "square %.2f  contacts %d  L %.1f  taper k*=%.3f (half-angle %.2f deg)" % (
                      i, j, di, dj, r["d_along_axis"], r["d_best"], r["tilt_best_deg"], s_side, len(cp),
                      L, row["taper_both_seat_k"], row["taper_half_angle_deg"]))
    save_json(f"rods_{name}.json", dict(scan_pairs=rows))


if __name__ == "__main__":
    import sys
    for nm in (sys.argv[1:] or ["saalburg", "hunt"]):
        main(nm)
    pub = published_cases()
    for k, v in pub.items():
        print("%-40s round %.2f  square %.2f" % (k, v["d_round"], v["square_side"]))
    save_json("rods_published.json", pub)
