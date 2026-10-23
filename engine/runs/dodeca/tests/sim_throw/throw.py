"""H1 physical test: MuJoCo throws of the two scanned dodecahedra (and fair dice for validation).

Body: the scan's convex hull for contact (on a flat surface only the knob tips can touch) and the
scan's own closed hollow shell for mass, centre of mass and inertia (uniform density; the face
statistics do not depend on the density value). Face normals and knob directions come from
../sim_mount/results/scan_geometry_<name>.json (validated tool, see ../sim_mount/validate_geom.py).
Surfaces: contact parameters are ASSUMED and swept (no measured values for bronze on Roman cloth,
wood or earth were looked up); `python throw.py drop` measures the restitution each one gives.
Usage: python throw.py drop | python throw.py run <body> <surface> <protocol> <n> [dt]
"""
import json, os, sys, time
import numpy as np
import mujoco

HERE = os.path.dirname(os.path.abspath(__file__))
SURF = {  # friction, solref (timeconst s, dampratio)
    "wood":  (0.40, (0.002, 0.30)),
    "board": (0.30, (0.002, 0.20)),
    "cloth": (0.80, (0.010, 1.00)),
    "earth": (0.70, (0.005, 1.00)),
}
PROTO = {  # release height above touching (m), horizontal speed (m/s), spin (rad/s)
    "toss": ((0.10, 0.30), (0.3, 1.5), (5.0, 25.0)),
    "drop": ((0.05, 0.15), (0.0, 0.1), (0.0, 2.0)),
    "cup":  ((0.05, 0.15), (0.5, 2.0), (15.0, 40.0)),
}


def regular_dodeca(r_in):
    p = (1 + 5 ** 0.5) / 2
    V = [(x, y, z) for x in (-1, 1) for y in (-1, 1) for z in (-1, 1)]
    for a in (-1, 1):
        for b in (-1, 1):
            V += [(0, a / p, b * p), (a / p, b * p, 0), (a * p, 0, b / p)]
    V = np.array(V, float)
    N = np.array([(0, a * p, b) for a in (-1, 1) for b in (-1, 1)] + [(a, 0, b * p) for a in (-1, 1) for b in (-1, 1)]
                 + [(a * p, b, 0) for a in (-1, 1) for b in (-1, 1)], float)
    N /= np.linalg.norm(N, axis=1, keepdims=True)
    return V * r_in / (V @ N[0]).max(), N


def body_def(name):
    """-> hull vertices (m), mass (kg), com (m), inertia about com (kg m2), face normals, knob dirs, holes."""
    if name == "cube":
        h = 0.008
        V = np.array([(x, y, z) for x in (-h, h) for y in (-h, h) for z in (-h, h)])
        m = 0.004
        I = np.eye(3) * m * (2 * h) ** 2 / 6
        N = np.array([(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)], float)
        return V, m, np.zeros(3), I, N, V / np.linalg.norm(V, axis=1, keepdims=True), None
    if name == "d12":
        import trimesh
        V, N = regular_dodeca(0.025)
        m = 0.1
        hull = trimesh.convex.convex_hull(V)
        I = hull.moment_inertia / hull.volume * m
        return V, m, np.zeros(3), I, N, V / np.linalg.norm(V, axis=1, keepdims=True), None
    sys.path.insert(0, os.path.join(HERE, "..", "sim_mount"))
    from common import load_scan_mm
    g = json.load(open(os.path.join(HERE, "..", "sim_mount", "results", f"scan_geometry_{name}.json")))
    msh = load_scan_mm(name)
    c0 = np.array(g["centre"])
    assert msh.is_watertight
    rho = 8.7e-6  # kg/mm3, nominal leaded bronze (ASSUMED; does not affect which face lands up)
    m = msh.volume * rho
    com = (msh.center_mass - c0) / 1000.0
    I = msh.moment_inertia * rho * 1e-6  # trimesh: about the centre of mass, density 1
    hull = (msh.convex_hull.vertices - c0) / 1000.0
    N = np.array(g["normals"])
    K = np.array([k["dir"] for k in g["knobs"]])
    holes = {h["face"]: (h["ell_major"] + h["ell_minor"]) / 2 for h in g["holes"]}
    return hull, m, com, I, N, K, holes


def build(name, surf, dt):
    V, m, com, I, N, K, holes = body_def(name)
    fr, (tc, dr) = SURF[surf]
    w, Q = np.linalg.eigh(I)
    if np.linalg.det(Q) < 0:
        Q[:, 0] *= -1
    quat = np.zeros(4)
    mujoco.mju_mat2Quat(quat, Q.flatten())
    verts = " ".join(f"{x:.7f}" for x in V.flatten())
    xml = (f'<mujoco><option timestep="{dt}" gravity="0 0 -9.81"/><compiler inertiafromgeom="false"/>'
           f'<asset><mesh name="hull" vertex="{verts}"/></asset><worldbody>'
           f'<geom name="floor" type="plane" size="5 5 0.1" friction="{fr} 0.005 0.0001" solref="{tc} {dr}"/>'
           f'<body name="obj"><freejoint/>'
           f'<inertial pos="{com[0]:.7f} {com[1]:.7f} {com[2]:.7f}" quat="{quat[0]} {quat[1]} {quat[2]} {quat[3]}" '
           f'mass="{m:.6f}" diaginertia="{w[0]:.4e} {w[1]:.4e} {w[2]:.4e}"/>'
           f'<geom type="mesh" mesh="hull" friction="{fr} 0.005 0.0001" solref="{tc} {dr}"/></body>'
           f'</worldbody></mujoco>')
    return mujoco.MjModel.from_xml_string(xml), N, K, holes, V


_CACHE = {}


def throw(args):
    name, surf, proto, seed, dt = args
    key = (name, surf, dt)
    if key not in _CACHE:
        _CACHE[key] = build(name, surf, dt)
    model, N, K, holes, V = _CACHE[key]
    d = mujoco.MjData(model)
    rng = np.random.default_rng(seed)
    (h0, h1), (v0, v1), (w0, w1) = PROTO[proto]
    q = rng.normal(size=4)
    q /= np.linalg.norm(q)
    d.qpos[:3] = (0, 0, np.max(np.linalg.norm(V, axis=1)) + rng.uniform(h0, h1))
    d.qpos[3:7] = q
    a = rng.uniform(0, 2 * np.pi)
    sp = rng.uniform(v0, v1)
    d.qvel[:3] = (sp * np.cos(a), sp * np.sin(a), 0.0)
    wd = rng.normal(size=3)
    d.qvel[3:6] = wd / np.linalg.norm(wd) * rng.uniform(w0, w1)
    nk = len(K)
    in_contact = np.zeros(nk, bool)
    events = np.zeros(nk)
    impulse = np.zeros(nk)
    f6 = np.zeros(6)
    still = t = 0.0
    bounces = 0
    airborne = True
    while t < 8.0:
        mujoco.mj_step(model, d)
        t += dt
        now = np.zeros(nk, bool)
        R = d.xmat[1].reshape(3, 3)
        for i in range(d.ncon):
            c = d.contact[i]
            p = R.T @ (c.pos - d.xpos[1])
            k = int(np.argmax(K @ (p / np.linalg.norm(p))))
            mujoco.mj_contactForce(model, d, i, f6)
            now[k] = True
            impulse[k] += abs(f6[0]) * dt
        events += now & ~in_contact
        in_contact = now
        if d.ncon == 0:
            airborne = True
        elif airborne:
            bounces += 1
            airborne = False
        if np.linalg.norm(d.qvel[:3]) < 1e-2 and np.linalg.norm(d.qvel[3:]) < 0.2:
            still += dt
        else:
            still = 0.0
        if still > 0.3:
            break
    R = d.xmat[1].reshape(3, 3)
    up = (N @ R.T)[:, 2]
    top = int(np.argmax(up))
    tilt = float(np.degrees(np.arccos(np.clip(up[top], -1, 1))))
    return dict(top=top, tilt=tilt, nknob=int(in_contact.sum()), t=t, bounces=bounces,
                travel=float(np.hypot(*d.qpos[:2])), events=events.tolist(), impulse=impulse.tolist())


def drop_test():
    """Restitution each surface setting gives: a 30 mm sphere dropped from 0.2 m, first rebound."""
    for s, (fr, (tc, dr)) in SURF.items():
        xml = (f'<mujoco><option timestep="0.0002"/><worldbody><geom type="plane" size="1 1 .1" solref="{tc} {dr}"/>'
               f'<body><freejoint/><geom type="sphere" size="0.015" mass="0.1" solref="{tc} {dr}"/></body>'
               f'</worldbody></mujoco>')
        mo = mujoco.MjModel.from_xml_string(xml)
        d = mujoco.MjData(mo)
        d.qpos[2] = 0.215
        hit, peak = False, 0.0
        for _ in range(int(1.0 / 0.0002)):
            mujoco.mj_step(mo, d)
            if d.ncon:
                if hit and peak > 0:
                    break
                hit = True
            elif hit:
                peak = max(peak, d.qpos[2] - 0.015)
        print(f"{s}: friction {fr}, solref ({tc}, {dr}) -> rebound {peak*1000:.1f} mm of 200 mm, "
              f"e = {np.sqrt(max(peak, 0) / 0.2):.2f}")


if __name__ == "__main__":
    if sys.argv[1] == "drop":
        drop_test()
        sys.exit()
    name, surf, proto, n = sys.argv[2:6]
    dt = float(sys.argv[6]) if len(sys.argv) > 6 else 0.0005
    from multiprocessing import Pool
    t0 = time.time()
    with Pool(14) as pool:
        res = pool.map(throw, [(name, surf, proto, s, dt) for s in range(int(n))], chunksize=4)
    out = os.path.join(HERE, "results", f"{name}_{surf}_{proto}_{n}_{dt}.json")
    json.dump(res, open(out, "w"), separators=(",", ":"))
    print(f"{name} {surf} {proto} n={n} dt={dt}: {time.time()-t0:.0f}s -> {out}")
