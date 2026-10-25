"""Load imbalance (max unit load / mean) for MoE routing at the modelled operating points.
GPU: EP over 72 GPUs (5.33 experts/GPU), optionally 32 redundant replicas of the hottest experts (EPLB-style).
Continuum: weight-stationary tiles; each expert's per-package slice spread over r tiles; 288 tiles/package;
hot experts can be replicated into the 47% free SRAM. Routing: top-6 of 384, expert popularity lognormal(sigma),
sigma=0 is uniform. Usage: python3 imbal5.py > imbal5.txt"""
import numpy as np
rng = np.random.default_rng(0)
E, K = 384, 6

def route(npos, sigma):
    w = rng.lognormal(0, sigma, E) if sigma else np.ones(E)
    w /= w.sum()
    # top-6 without replacement approximated by multinomial on popularity (counts per expert)
    return rng.multinomial(npos * K, w), w

def gpu_imb(npos, sigma, n=72, red=0, trials=40):
    out = []
    for _ in range(trials):
        cnt, w = route(npos, sigma)
        units = [[] for _ in range(n)]
        # greedy placement by expected popularity, replicas split load of hottest experts
        order = np.argsort(-w)
        rep = {e: 2 for e in order[:red]}
        loads_exp = np.zeros(n)
        items = []
        for e in range(E):
            r = rep.get(e, 1)
            items += [(w[e] / r, e, r)] * r
        items.sort(reverse=True)
        load = np.zeros(n); assign = [[] for _ in range(n)]
        for wt, e, r in items:
            u = int(np.argmin(load)); load[u] += wt; assign[u].append((e, r))
        real = np.array([sum(cnt[e] / r for e, r in a) for a in assign])
        out.append(real.max() / real.mean())
    return np.mean(out)

def tile_imb(npos, sigma, r=16, tiles=288, rep_frac=0.0, trials=40):
    out = []
    for _ in range(trials):
        cnt, w = route(npos, sigma)
        nrep = int(rep_frac * E)
        order = np.argsort(-w)
        reps = np.ones(E, int); reps[order[:nrep]] = 2
        items = []
        for e in range(E):
            for _ in range(r * reps[e]):
                items.append((w[e] / (r * reps[e]), e, r * reps[e]))
        items.sort(reverse=True)
        load = np.zeros(tiles); real = np.zeros(tiles)
        for wt, e, rr in items:
            u = int(np.argmin(load)); load[u] += wt; real[u] += cnt[e] / rr
        out.append(real.max() / real.mean())
    return np.mean(out)

print("GPU operating points: >=200 B=23.5k*2 pos; >=1000 B=4.4k*5 pos (round-4 op points)")
for sigma in (0.0, 0.5, 1.0):
    for npos, lab in ((47000, ">=200"), (22000, ">=1000")):
        print(f"GPU EP72 sigma={sigma} {lab}: no-redundancy {gpu_imb(npos, sigma):.3f}  32 redundant {gpu_imb(npos, sigma, red=32):.3f}")
print("\nContinuum per-package tiles (b*pos positions per microbatch)")
for sigma in (0.0, 0.5, 1.0):
    for npos, lab in ((1078, ">=200 (539x2)"), (609, ">=1000 (203x3)")):
        cells = [f"r={r}: {tile_imb(npos, sigma, r=r):.2f}" for r in (4, 16, 64)]
        cells.append(f"r=16 +25% replicas: {tile_imb(npos, sigma, r=16, rep_frac=0.25):.2f}")
        print(f"sigma={sigma} {lab}: " + "  ".join(cells))
