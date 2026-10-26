import sys, time
import numpy as np

N = int(sys.argv[1]) if len(sys.argv) > 1 else 127
BUDGET = float(sys.argv[2]) if len(sys.argv) > 2 else 54.0
t0 = time.time()
rng = np.random.default_rng()
conv = np.convolve
BITS = [1 << i for i in range(N)]


def energy(x):
    c = np.correlate(x, x, 'full')[N:]
    return int(c @ c)


def walk(x, max_steps, visited, best_e):
    """Self-avoiding walk: always take the best unvisited single-flip neighbour."""
    x = x.copy()
    h = 0
    for i in range(N):
        if x[i] > 0:
            h |= BITS[i]
    cs = np.correlate(x, x, 'full')
    cs[N - 1] = 0
    e = int(cs[N:] @ cs[N:])
    wb, wbx = e, x.copy()
    visited.add(h)
    base = 4 * (N - 2)
    since = 0
    for step in range(max_steps):
        g = conv(x, cs)[N - 1:2 * N - 1]
        t = conv(x, x)[0::2]
        cand = e + base + 4 * t - 4 * x * g
        order = np.argsort(cand, kind='stable')
        for i in order[:8]:
            i = int(i)
            nh = h ^ BITS[i]
            if nh not in visited:
                break
        else:
            for i in order[8:]:
                i = int(i)
                nh = h ^ BITS[i]
                if nh not in visited:
                    break
            else:
                break
        h = nh
        visited.add(h)
        x[i] = -x[i]
        cs = np.correlate(x, x, 'full')
        cs[N - 1] = 0
        e = int(cand[i])
        if e < wb:
            wb, wbx = e, x.copy()
            since = 0
        else:
            since += 1
    return wb, wbx


def main():
    best_e, best = None, None
    while time.time() - t0 < BUDGET:
        x = rng.choice(np.array([-1, 1]), N)
        visited = set()
        steps = 0
        e, y = walk(x, 4000, visited, best_e)
        if best_e is None or e < best_e:
            best_e, best = e, y
            print(best_e, N * N / (2 * best_e), round(time.time() - t0, 1), file=sys.stderr)
    print("".join("+" if v > 0 else "-" for v in best))


main()
