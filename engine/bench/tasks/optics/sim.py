"""2D ray tracer for a sunlight concentrator. Light enters through the aperture (the top of a box W = 1 wide and H = 1
high) at every position, with directions spread uniformly within +-3 degrees of straight down. Inside the box you place
perfect mirrors (polylines) and one flat receiver (a segment that absorbs on both sides). A ray is collected when it
hits the receiver; it is lost when it leaves the box or makes more than 200 reflections.

Score = collected fraction x (W / receiver width) / (1 / sin 3deg), i.e. the concentration as a fraction of the
etendue limit (1.0 is the physical maximum).

Usage: python3 sim.py design.json   design: {"receiver": [[x1, y1], [x2, y2]], "mirrors": [[[x, y], [x, y], ...], ...]}
       with every point inside the box: -0.5 <= x <= 0.5, 0 <= y <= 1; at most 4000 mirror segments.
"""
import json, math, sys
import numpy as np

W, H, THETA, MAXSEG, MAXB = 1.0, 1.0, math.radians(3.0), 4000, 200
NX, NA = 600, 61  # rays: 600 positions x 61 directions, stratified


def trace(rec, mirrors):
    segs = [(np.array(p[i], float), np.array(p[i + 1], float)) for p in mirrors for i in range(len(p) - 1)]
    A = np.array([s[0] for s in segs] + [rec[0]], float); Bp = np.array([s[1] for s in segs] + [rec[1]], float)
    E = Bp - A; nseg = len(A); is_rec = np.zeros(nseg, bool); is_rec[-1] = True
    xs = -W / 2 + (np.arange(NX) + 0.5) / NX * W; an = -THETA + (np.arange(NA) + 0.5) / NA * 2 * THETA
    X, G = np.meshgrid(xs, an); P = np.stack([X.ravel(), np.full(X.size, H - 1e-9)], 1); D = np.stack([np.sin(G.ravel()), -np.cos(G.ravel())], 1)
    alive = np.ones(len(P), bool); got = np.zeros(len(P), bool)
    for _ in range(MAXB):
        live = np.nonzero(alive)[0]
        if not len(live): break
        for c0 in range(0, len(live), max(1, 2_000_000 // nseg)):  # chunks keep the ray x segment arrays small
            step(live[c0:c0 + max(1, 2_000_000 // nseg)], P, D, A, E, is_rec, alive, got)
    return got.mean()


def step(idx, P, D, A, E, is_rec, alive, got):
        p, d = P[idx], D[idx]
        den = d[:, None, 0] * E[None, :, 1] - d[:, None, 1] * E[None, :, 0]  # cross(d, e)
        q = A[None, :, :] - p[:, None, :]
        with np.errstate(divide="ignore", invalid="ignore"):
            t = (q[..., 0] * E[None, :, 1] - q[..., 1] * E[None, :, 0]) / den
            u = (q[..., 0] * d[:, None, 1] - q[..., 1] * d[:, None, 0]) / den
        ok = (np.abs(den) > 1e-14) & (t > 1e-9) & (u >= 0) & (u <= 1)
        t = np.where(ok, t, np.inf); j = t.argmin(1); tm = t[np.arange(len(idx)), j]
        miss = ~np.isfinite(tm); alive[idx[miss]] = False
        hit = ~miss; r = is_rec[j] & hit; got[idx[r]] = True; alive[idx[r]] = False
        m = hit & ~is_rec[j]; ii, jj = idx[m], j[m]
        P[ii] = P[ii] + D[ii] * tm[m][:, None]
        e = E[jj]; nrm = np.stack([-e[:, 1], e[:, 0]], 1) / np.linalg.norm(e, axis=1)[:, None]
        D[ii] = D[ii] - 2 * (D[ii] * nrm).sum(1)[:, None] * nrm
        out = (P[ii, 0] < -W / 2 - 1e-9) | (P[ii, 0] > W / 2 + 1e-9) | (P[ii, 1] < -1e-9) | (P[ii, 1] > H + 1e-9)
        alive[ii[out]] = False


def check(d):
    rec, mirrors = np.array(d["receiver"], float), d.get("mirrors", [])
    pts = [rec[0], rec[1]] + [np.array(q, float) for p in mirrors for q in p]
    if any(not (-W / 2 - 1e-9 <= q[0] <= W / 2 + 1e-9 and -1e-9 <= q[1] <= H + 1e-9) for q in pts): raise ValueError("a point lies outside the box")
    if sum(len(p) - 1 for p in mirrors) > MAXSEG: raise ValueError(f"more than {MAXSEG} mirror segments")
    w = float(np.linalg.norm(rec[1] - rec[0]))
    if w < 1e-4: raise ValueError("receiver narrower than 1e-4")
    return rec, mirrors, w


if __name__ == "__main__":
    try: rec, mirrors, w = check(json.load(open(sys.argv[1])))
    except Exception as e: print(json.dumps({"ok": False, "error": str(e)})); sys.exit()
    eta = trace(rec, mirrors); c = eta * W / w
    print(json.dumps({"ok": True, "collected": round(eta, 4), "receiver_width": round(w, 5), "concentration": round(c, 3), "score": round(c * math.sin(THETA), 4)}))
