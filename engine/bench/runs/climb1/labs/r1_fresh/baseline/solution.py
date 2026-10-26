import sys, time
import numpy as np

N, BUDGET = (int(sys.argv[1]) if len(sys.argv) > 1 else 127), 55.0
rng = np.random.default_rng()
t0 = time.time()


def corr(x):
    return np.array([x[:N - k] @ x[k:] for k in range(1, N)])


best, best_e = None, None
while time.time() - t0 < BUDGET:
    x = rng.choice([-1, 1], N)
    c = corr(x); e = int(c @ c)
    while True:  # steepest descent over single flips
        ks = np.arange(1, N)
        # change of C_k when x_i flips: -2 x_i (x_{i+k} + x_{i-k}), with out-of-range terms 0
        pad = np.concatenate([np.zeros(N, int), x, np.zeros(N, int)])
        idx = np.arange(N)[:, None]
        delta = -2 * x[:, None] * (pad[N + idx + ks] + pad[N + idx - ks])
        cand = ((c[None, :] + delta) ** 2).sum(1)
        i = int(cand.argmin())
        if cand[i] >= e:
            break
        x[i] = -x[i]; c = c + delta[i]; e = int(cand[i])
    if best_e is None or e < best_e:
        best, best_e = x.copy(), e
print("".join("+" if v > 0 else "-" for v in best))
