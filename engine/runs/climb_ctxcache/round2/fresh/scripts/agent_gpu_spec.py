# Own-stack GPU time for the 200 SWE-agent sessions (append-only, exact prefix caching), now also
# counting decode compute, with and without lossless prompt-lookup speculative decoding.
# tau = output tokens per verify pass, rho = proposed tokens per output token (from copyspec.py, K=8).
# Time per pass is the sum of its compute time and its memory time (conservative: no overlap).
import json, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import r1_traces as T
from agent_gpu import M, FL, BW, HBM_S, BATCH
TAU, RHO = float(sys.argv[3]), float(sys.argv[4])
tr = T.load(sys.argv[1]); ex = {json.loads(l)["id"]: json.loads(l)["exec_s"] for l in open(sys.argv[2])}
for name, (kvb, lin, att, wb) in M.items():
    res = {}
    for spec in (False, True):
        tot = kvread = 0.0
        for t in tr:
            ntok = [T.tok(x) for x in t["text"]]; A = T.requests(t); es = ex[t["id"]]; prev = None
            for j, a in enumerate(A):
                L = T.TOOLS + sum(ntok[:a]); c0 = T.TOOLS + sum(ntok[:prev]) if prev is not None else 0
                new = L - c0; o = ntok[a]; Lm = L + o / 2
                tot += new * lin / FL + new * (c0 + new / 2) * att / FL                    # prefill of new tokens
                passes = o / TAU if spec else o; work = o * (1 + RHO) if spec else o       # tokens run through the model
                tot += work * (lin + Lm * att) / FL                                        # decode compute
                kv = passes * Lm * kvb / BW; tot += kv + passes * wb / BATCH / BW; kvread += kv
                if j < len(es) and es[j]: tot += L * kvb * es[j] * HBM_S
                prev = a
        res[spec] = (tot, kvread)
    (b, bk), (s, sk) = res[False], res[True]
    print(f"{name:42s} GPU-h {b/3600:5.2f} -> {s/3600:5.2f} ({s/b-1:+.1%}); decode reads of cached KV {bk/b:.0%} of GPU time -> {sk/s:.0%}")
