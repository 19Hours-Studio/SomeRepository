"""Measure the Saalburg / Kleiner Feldberg dodecahedron scan (FMb 2103, Fraunhofer IGD GLB, metres).

Outputs results/scan_geometry.json and prints a table.

Steps (each validated on a synthetic mesh in validate_geom.py):
 1. merge texture-seam vertices -> one watertight shell (genus 11 = 12 holes through a hollow shell);
 2. 20 knob tips = radial maxima >20 deg apart; regular dodecahedron fitted to them (Hungarian + Kabsch);
 3. the 12 outer face planes fitted robustly to outward-facing vertices; centre refined so that
    the 12 plane offsets are as equal as possible;
 4. wall thickness = rays cast from the outer face surface inward along -n (first exit), plus
    the offset between robust outer and inner plane fits;
 5. hole aperture = complement of the projected footprint of every triangle in the wall slab of
    that face (projection along the face normal) -> polygon of the free opening through the whole
    wall; reported: equivalent diameter, maximum inscribed circle (largest perpendicular rod),
    minimum width and maximum length (caliper-like), direct least-squares ellipse fit;
 6. engraved rings: radial profile of the outer surface height around the hole centre; grooves =
    local minima of the binned profile deeper than 0.04 mm relative to the neighbouring maxima;
 7. knobs: sphere fit to the outermost 1.2 mm cap (tip radius), protrusion beyond the face planes.
"""
import sys
import numpy as np
import shapely
from shapely.geometry import Polygon, Point
from shapely.ops import unary_union
from scipy.optimize import linear_sum_assignment, least_squares
from common import (load_scan_mm, canonical_vertices, canonical_face_normals, save_json,
                    R_IN, R_CIRC, PENT_IN, PENT_CIRC)


def frame(n):
    a = np.array([1.0, 0, 0]) if abs(n[0]) < 0.9 else np.array([0, 1.0, 0])
    e1 = np.cross(n, a); e1 /= np.linalg.norm(e1)
    e2 = np.cross(n, e1)
    return e1, e2


def kabsch(A, B):
    H = A.T @ B
    U, S, Vt = np.linalg.svd(H)
    d = np.sign(np.linalg.det(Vt.T @ U.T))
    return Vt.T @ np.diag([1, 1, d]) @ U.T


def knob_tips(V, n_tips=20, min_sep_deg=20.0):
    r = np.linalg.norm(V, axis=1)
    d = V / r[:, None]
    tips = []
    for i in np.argsort(-r):
        if len(tips) == n_tips:
            break
        if any(d[i] @ d[j] > np.cos(np.radians(min_sep_deg)) for j in tips):
            continue
        tips.append(i)
    return np.array(tips)


def fit_orientation(tipdirs, seed=0, n_starts=300):
    from scipy.spatial.transform import Rotation as Rot
    cv = canonical_vertices(); cv /= np.linalg.norm(cv, axis=1, keepdims=True)
    rng = np.random.default_rng(seed)
    best = None
    for _ in range(n_starts):
        R = Rot.random(random_state=int(rng.integers(1 << 30))).as_matrix()
        for _ in range(15):
            ri, ci = linear_sum_assignment(-(cv @ R.T) @ tipdirs.T)
            R = kabsch(cv[ri], tipdirs[ci])
        err = np.degrees(np.arccos(np.clip(np.sum((cv[ri] @ R.T) * tipdirs[ci], 1), -1, 1)))
        if best is None or err.mean() < best[0]:
            best = (err.mean(), R, err.max())
    return best


def fit_planes(m, c, N, iters=6, cone_deg=12.0):
    VN = m.vertex_normals
    for _ in range(iters):
        V = m.vertices - c
        Vd = V / np.linalg.norm(V, axis=1)[:, None]
        lab = np.argmax(VN @ N.T, 1)
        dirlab = np.argmax(Vd @ N.T, 1)
        newN, dist, rms, npts = [], [], [], []
        for i, n in enumerate(N):
            sel = (lab == i) & (dirlab == i) & (VN @ n > np.cos(np.radians(cone_deg))) & (Vd @ n > 0.5)
            P = V[sel]
            for _ in range(6):
                cen = P.mean(0)
                _, _, Vt = np.linalg.svd(P - cen, full_matrices=False)
                nn = Vt[2] * np.sign(Vt[2] @ n)
                res = (P - cen) @ nn
                mad = 1.4826 * np.median(np.abs(res - np.median(res)))
                P = P[np.abs(res - np.median(res)) < 2.5 * mad + 1e-9]
            newN.append(nn); dist.append(nn @ cen); rms.append(np.std((P - cen) @ nn)); npts.append(len(P))
        N = np.array(newN); dist = np.array(dist)
        A = np.hstack([N, np.ones((12, 1))])
        sol, *_ = np.linalg.lstsq(A, dist, rcond=None)
        c = c + sol[:3]
    V = m.vertices - c
    h_out = np.array([N[i] @ (m.vertices[0] * 0) + d - N[i] @ sol[:3] for i, d in enumerate(dist)])
    return c, N, h_out, np.array(rms), np.array(npts)


def fit_ellipse(x, y):
    """Fitzgibbon-Pilu-Fisher direct least-squares ellipse; returns centre, (major, minor) full
    axes, angle of the major axis (rad)."""
    D = np.c_[x * x, x * y, y * y, x, y, np.ones_like(x)]
    S = D.T @ D
    C = np.zeros((6, 6)); C[0, 2] = C[2, 0] = 2; C[1, 1] = -1
    w, v = np.linalg.eig(np.linalg.solve(S, C))
    w = np.real(w); v = np.real(v)
    a = None
    for k in range(6):
        ak = v[:, k]
        if 4 * ak[0] * ak[2] - ak[1] ** 2 > 0:
            a = ak; break
    A, B, Cc, Dd, E, F = a
    M0 = np.array([[F, Dd / 2, E / 2], [Dd / 2, A, B / 2], [E / 2, B / 2, Cc]])
    M = np.array([[A, B / 2], [B / 2, Cc]])
    x0, y0 = np.linalg.solve(2 * M, [-Dd, -E])
    lam, vec = np.linalg.eigh(M)
    detM0, detM = np.linalg.det(M0), np.linalg.det(M)
    ax = np.sqrt(-detM0 / (detM * lam))
    order = np.argsort(-ax)
    ax = ax[order]; vec = vec[:, order]
    ang = np.arctan2(vec[1, 0], vec[0, 0])
    return (x0, y0), (2 * ax[0], 2 * ax[1]), ang


def width_length(poly, n_ang=180):
    """Minimum width (caliper) and maximum caliper length of a convex-ish polygon (deg steps)."""
    xy = np.asarray(poly.exterior.coords)
    ws = []
    for t in np.linspace(0, np.pi, n_ang, endpoint=False):
        u = np.array([np.cos(t), np.sin(t)])
        p = xy @ u
        ws.append(p.max() - p.min())
    ws = np.array(ws)
    return ws.min(), ws.max()


def hole_aperture(m, c, n, h_out, h_in, r_max=13.5, slab_extra=(1.0, 0.6)):
    """Free opening through the wall of one face, projected along n, in the face frame."""
    e1, e2 = frame(n)
    T = m.vertices[m.faces] - c                       # (F,3,3)
    h = T @ n
    xy = np.stack([T @ e1, T @ e2], -1)
    rr = np.linalg.norm(xy.mean(1), axis=1)
    sel = (h.max(1) > h_in - slab_extra[0]) & (h.min(1) < h_out + slab_extra[1]) & (rr < r_max + 3)
    tris = [Polygon(t) for t in xy[sel]]
    tris = [t for t in tris if t.area > 1e-9]
    fp = unary_union(tris)
    disk = Point(0, 0).buffer(r_max, 256)
    free = disk.difference(fp)
    geoms = getattr(free, "geoms", [free])
    # the opening = the free component nearest the axis (largest one containing points near 0)
    hole = max(geoms, key=lambda g: g.area if g.distance(Point(0, 0)) < 3 else 0)
    if hole.distance(Point(0, 0)) > 3:
        return None
    return hole, (e1, e2)


def ring_profile(m, c, n, centre_xy, e1, e2, h_out, rmin, rmax=15.5, binw=0.2):
    V = m.vertices - c
    VN = m.vertex_normals
    Vd = V / np.linalg.norm(V, axis=1)[:, None]
    sel = (VN @ n > np.cos(np.radians(35))) & (Vd @ n > 0.75) & (np.abs(V @ n - h_out) < 1.0)
    P = V[sel]
    x, y = P @ e1 - centre_xy[0], P @ e2 - centre_xy[1]
    rho = np.hypot(x, y)
    z = P @ n - h_out
    bins = np.arange(rmin, rmax + binw, binw)
    idx = np.digitize(rho, bins)
    prof = np.array([np.median(z[idx == k]) if np.sum(idx == k) >= 4 else np.nan
                     for k in range(1, len(bins))])
    rc = 0.5 * (bins[1:] + bins[:-1])
    # grooves: local minima at least 0.04 mm below the max of the profile within +-0.8 mm
    grooves = []
    for k in range(2, len(prof) - 2):
        if np.isnan(prof[k]):
            continue
        win = prof[max(0, k - 4):k + 5]
        if prof[k] == np.nanmin(prof[max(0, k - 2):k + 3]) and np.nanmax(win) - prof[k] > 0.04:
            grooves.append((round(float(rc[k]), 2), round(float(np.nanmax(win) - prof[k]), 3)))
    return rc, prof, grooves


def sphere_fit(P):
    def res(p):
        return np.linalg.norm(P - p[:3], axis=1) - p[3]
    p0 = np.r_[P.mean(0), np.std(P)]
    s = least_squares(res, p0)
    return s.x[:3], abs(s.x[3]), np.sqrt(np.mean(s.fun ** 2))


def measure(m, verbose=True):
    out = {}
    c = m.center_mass.copy()
    V = m.vertices - c
    tips = knob_tips(V)
    td = V[tips] / np.linalg.norm(V[tips], axis=1)[:, None]
    err, R, errmax = fit_orientation(td)
    N0 = canonical_face_normals() @ R.T
    c, N, h_out, rms, npts = fit_planes(m, c, N0)
    V = m.vertices - c
    opp = [int(np.argmin(N @ n)) for n in N]
    out["centre"] = c; out["normals"] = N; out["h_out"] = h_out
    out["plane_rms"] = rms; out["opposite"] = opp
    out["orientation_fit_err_deg"] = (float(err), float(errmax))
    G = np.clip(N @ N.T, -1, 1)
    out["adjacent_normal_angles_deg"] = [sorted(np.degrees(np.arccos(G[i]))[np.argsort(-G[i])[1:6]].tolist())
                                         for i in range(12)]
    # ---------------- wall thickness by rays and by inner plane fit
    VN = m.vertex_normals
    Vd = V / np.linalg.norm(V, axis=1)[:, None]
    lab = np.argmax(Vd @ N.T, 1)
    t_ray, t_plane, h_in = [], [], []
    import trimesh
    for i, n in enumerate(N):
        seli = (lab == i) & (VN @ (-n) > np.cos(np.radians(25))) & (Vd @ n > 0.85)
        hi = np.median(V[seli] @ n) if seli.sum() > 20 else h_out[i] - 1.3
        h_in.append(hi); t_plane.append(h_out[i] - hi)
        selo = np.where((lab == i) & (VN @ n > np.cos(np.radians(15))) & (np.abs(V @ n - h_out[i]) < 0.5)
                        & (Vd @ n > 0.80))[0]
        rng = np.random.default_rng(i)
        selo = rng.choice(selo, min(300, len(selo)), replace=False)
        orig = m.vertices[selo] - n * 0.02
        loc, ri, _ = m.ray.intersects_location(orig, np.repeat(-n[None], len(orig), 0), multiple_hits=True)
        ts = []
        for k in range(len(orig)):
            dd = (orig[k] - loc[ri == k]) @ n
            dd = dd[dd > 0.05]
            if len(dd):
                ts.append(dd.min() + 0.02)
        ts = np.array(ts)
        ts = ts[ts < 4.0]
        t_ray.append([float(np.percentile(ts, 10)), float(np.median(ts)), float(np.percentile(ts, 90)), int(len(ts))])
    out["h_in"] = h_in; out["wall_t_plane"] = t_plane; out["wall_t_ray_p10_med_p90_n"] = t_ray
    # ---------------- holes
    holes = []
    for i, n in enumerate(N):
        res = hole_aperture(m, c, n, h_out[i], h_in[i])
        if res is None:
            holes.append(None); continue
        hole, (e1, e2) = res
        mic = shapely.maximum_inscribed_circle(hole, tolerance=0.005)
        mic_c = np.asarray(mic.coords[0]); d_mic = 2 * mic.length
        d_eq = 2 * np.sqrt(hole.area / np.pi)
        wmin, lmax = width_length(hole)
        xy = np.asarray(hole.exterior.coords)[:-1]
        (x0, y0), (amaj, amin), ang = fit_ellipse(xy[:, 0], xy[:, 1])
        # outer-surface opening (rim at the outer face): section 0.15 mm below the outer plane
        o = c + n * (h_out[i] - 0.15)
        d_outer = None
        sec = m.section(plane_origin=o, plane_normal=n)
        if sec is not None:
            loops = []
            for ent in sec.discrete:
                P = ent - o
                pol = Polygon(np.c_[P @ e1, P @ e2])
                if pol.is_valid and pol.contains(Point(x0, y0)) and pol.area < 900:
                    loops.append(pol)
            if loops:
                lp = min(loops, key=lambda p: p.area)
                d_outer = 2 * np.sqrt(lp.area / np.pi)
        rc, prof, grooves = ring_profile(m, c, n, (x0, y0), e1, e2, h_out[i], rmin=d_eq / 2 + 0.3)
        holes.append(dict(face=i, d_eq=d_eq, d_mic=d_mic, mic_centre=mic_c, width_min=wmin, length_max=lmax,
                          ell_major=amaj, ell_minor=amin, ell_angle_deg=np.degrees(ang),
                          centre_offset=np.hypot(x0, y0), centre_xy=(x0, y0), d_outer_rim=d_outer,
                          grooves=grooves, profile_r=rc, profile_z=prof,
                          poly=np.asarray(hole.exterior.coords), e1=e1, e2=e2))
    out["holes"] = holes
    # ---------------- knobs
    cv = canonical_vertices(); cv /= np.linalg.norm(cv, axis=1, keepdims=True)
    vdirs = cv @ R.T
    knobs = []
    for j, vdir in enumerate(vdirs):
        ang = np.degrees(np.arccos(np.clip(Vd @ vdir, -1, 1)))
        selk = ang < 12
        P = V[selk]; rP = P @ vdir
        tip = rP.max()
        cap = P[rP > tip - 1.2]
        cen, rad, rmsk = sphere_fit(cap)
        body = P[rP > tip - 3.0]
        cenb, radb, _ = sphere_fit(body)
        faces_of = list(np.argsort(-(N @ vdir))[:3])
        prot = [float(tip * (vdir @ N[f]) - h_out[f]) for f in faces_of]  # tip height above each plane
        knobs.append(dict(dir=vdir, tip_r=float(tip), tip_xyz=(V[selk][np.argmax(rP)]).tolist(),
                          cap_radius=float(rad), cap_rms=float(rmsk), body_radius=float(radb),
                          faces=[int(f) for f in faces_of], height_above_planes=prot))
    out["knobs"] = knobs
    # edge length estimate from face plane offsets (regular-solid relation)
    out["edge_from_inradius"] = float(np.mean(h_out) / R_IN)
    tipx = np.array([k["tip_xyz"] for k in knobs])
    from scipy.spatial.distance import cdist
    Dk = cdist(tipx, tipx); np.fill_diagonal(Dk, np.inf)
    out["knob_tip_nn_spacing"] = np.sort(Dk, 1)[:, :3]
    out["volume_mm3"] = float(m.volume)
    out["area_mm2"] = float(m.area)
    out["is_watertight"] = bool(m.is_watertight); out["euler"] = int(m.euler_number)
    return out


def main(name="saalburg"):
    m = load_scan_mm(name)
    g = measure(m)
    print("=== scan:", name)
    opp = g["opposite"]
    print("watertight", g["is_watertight"], "euler", g["euler"], "volume mm3 %.0f" % g["volume_mm3"])
    print("orientation fit err (mean,max deg)", np.round(g["orientation_fit_err_deg"], 2))
    print("edge length from mean inradius %.2f mm; face-to-face (mean) %.2f mm" %
          (g["edge_from_inradius"], 2 * np.mean(g["h_out"])))
    print("face h_out  t_plane  t_ray(p10,med,p90,n)  d_eq  d_mic  wmin  lmax  ell(maj x min)  off  d_rim  grooves(r,depth)")
    for i in range(12):
        hh = g["holes"][i]
        print("%2d(%2d) %5.2f %5.2f  %s  %5.2f %5.2f %5.2f %5.2f  %5.2f x %5.2f  %4.2f  %s  %s" % (
            i, opp[i], g["h_out"][i], g["wall_t_plane"][i], np.round(g["wall_t_ray_p10_med_p90_n"][i], 2),
            hh["d_eq"], hh["d_mic"], hh["width_min"], hh["length_max"], hh["ell_major"], hh["ell_minor"],
            hh["centre_offset"], None if hh["d_outer_rim"] is None else round(hh["d_outer_rim"], 2),
            hh["grooves"]))
    print("knob tips: r (mm)", np.round([k["tip_r"] for k in g["knobs"]], 2))
    print("knob cap radius", np.round([k["cap_radius"] for k in g["knobs"]], 2))
    print("knob body radius", np.round([k["body_radius"] for k in g["knobs"]], 2))
    print("knob tip height above its 3 face planes", np.round([np.mean(k["height_above_planes"]) for k in g["knobs"]], 2))
    print("knob nn spacing", np.round(g["knob_tip_nn_spacing"].mean(), 2))
    save_json(f"scan_geometry_{name}.json", g)


if __name__ == "__main__":
    for nm in (sys.argv[1:] or ["saalburg", "hunt"]):
        main(nm)
