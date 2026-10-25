# Lever the answer does not price: cache-aware observation masking on the real traces. Every K requests, observations
# older than the last M turns are replaced by a ~10-token placeholder; between those points the context is append-only,
# so the cache breaks only once per K requests (at the first newly masked observation). Prior art on quality:
# Lindenbauer et al. 2025 (JetBrains), "The Complexity Trap" - observation masking matched LLM summarization on SWE-bench Verified.
# Usage: python3 -I mask_check.py <trajs_dir> <round3_code_dir>
import sys, glob
sys.path.insert(0, sys.argv[2]); import trace4 as T
R, W, O = T.R, T.W, T.O
F = sorted(glob.glob(sys.argv[1] + "/*.json")); TR = [T.load(f)[0] for f in F]
def run(t, K, M, ph=10):
    # segment list: (step, tokens, is_obs); prompt j = first prompt + for i<j: out_i(completion-ish) + obs_i
    n = len(t); obs = [min(len(s["obs"]) / 3.6 + 0.5, max(t[i + 1]["L"] - s["L"], 0)) if i + 1 < n else 0 for i, s in enumerate(t)]
    other = [max(t[i + 1]["L"] - s["L"], 0) - obs[i] if i + 1 < n else 0 for i, s in enumerate(t)]
    masked_upto = 0; prev = None; c = 0.0
    for j, s in enumerate(t):
        if K and j and j % K == 0: masked_upto = max(masked_upto, j - M)
        segs = [("p", t[0]["L"])]
        for i in range(j):
            segs.append((("a", i), other[i])); segs.append((("o", i, i < masked_upto), ph if i < masked_upto else obs[i]))
        L = sum(x for _, x in segs); hit = 0
        if prev:
            for a, b in zip(segs, prev):
                if a != b: break
                hit += a[1]
        c += R * hit + W * (L - hit) + O * s["out"]; prev = segs
    return c, L
base = sum(run(t, 0, 0)[0] for t in TR)
print(f"append-only base (obs approximated) {base:,.0f} units (trace4 reports 95,205,486)")
for K, M in ((10, 10), (10, 5), (20, 10), (5, 10)):
    c = sum(run(t, K, M)[0] for t in TR); print(f"mask every {K} requests, keep last {M} obs: {c/base-1:+.1%}")
