"""Two-tier exact prefix cache replay on Mooncake traces: DRAM (LRU, cap C_d blocks) -> SSD
(unbounded capacity, but writes cost endurance). On DRAM eviction a block is written to SSD only if
the admission policy accepts it. Output: (SSD bytes written / write-all bytes, FLOPs saved fraction).
Policies:
  all      : write every evicted block (what LMCache/Mooncake-style spill does by default)
  rand(p)  : write with prob p (cheapest budget-meeting filter)
  hit2     : write only if block was re-hit while in DRAM (classic second-hit flash admission)
  reuse(t) : write if learned P(reuse|bucket) >= t                     (anchor without FLOP term)
  anchor(t): write if learned P(reuse|bucket) * recompute_FLOPs/bytes >= t (expected reuse x FLOPs / byte)
Buckets: (min(hits,2), log2 depth). P(reuse) learned online from previously evicted blocks.
Usage: python3 -I sim_admit.py TRACE.jsonl CAP_DRAM_BLOCKS MODEL
"""
import json, sys, math, random
from collections import OrderedDict, defaultdict
from sim_evict import MODELS, block_flops

def run(reqs, cap_d, m, pol, t=0.0):
    rng = random.Random(1)
    dram = OrderedDict()          # h -> (depth, hits)
    ssd = set()
    evicted_bucket = {}           # h -> bucket at last DRAM eviction (for learning)
    n_b = defaultdict(lambda: 1.0); r_b = defaultdict(lambda: 0.5)  # Beta prior
    written = cand = 0
    tot = saved = 0.0
    c0 = block_flops(m, 0)
    for r in reqs:
        hs = r["hash_ids"]
        k = 0
        while k < len(hs) and (hs[k] in dram or hs[k] in ssd):
            k += 1
        for j, h in enumerate(hs):
            c = block_flops(m, j); tot += c
            if j < k: saved += c
            b = evicted_bucket.pop(h, None)
            if b is not None:     # block re-requested after DRAM eviction: label for learning
                r_b[b] += 1
        for j, h in enumerate(hs):
            if h in dram:
                d, hits = dram.pop(h); dram[h] = (d, hits + (j < k))
            else:
                dram[h] = (j, 0)
        while len(dram) > cap_d:
            h, (d, hits) = dram.popitem(last=False)
            if h in ssd:
                continue
            cand += 1
            b = (min(hits, 2), int(math.log2(d + 1)))
            n_b[b] += 1; evicted_bucket[h] = b
            p = r_b[b] / n_b[b]
            if pol == "all": ok = True
            elif pol == "rand": ok = rng.random() < t
            elif pol == "hit2": ok = hits >= 1
            elif pol == "reuse": ok = p >= t
            else: ok = p * block_flops(m, d) / c0 >= t   # bytes/block constant -> FLOPs/byte ~ FLOPs
            if ok:
                ssd.add(h); written += 1
    return written / max(cand, 1), saved / tot

if __name__ == "__main__":
    reqs = [json.loads(l) for l in open(sys.argv[1])]
    cap = int(sys.argv[2]); m = MODELS[sys.argv[3]]
    w0, f_dram = run(reqs, cap, m, "rand", 0.0)
    w1, f_all = run(reqs, cap, m, "all")
    print(f"# {sys.argv[1].split('/')[-1]} model={sys.argv[3]} DRAM={cap*512/1e6:.2f}M tok")
    print(f"DRAM only: flops_saved={f_dram:.3f} ; write-all: writes=1.000 flops_saved={f_all:.3f}")
    print("policy      writes  flops_saved  share_of_SSD_value_kept")
    def row(name, w, f): print(f"{name:11s} {w:6.3f}  {f:.3f}  {(f-f_dram)/(f_all-f_dram):.2f}")
    for p in [0.1, 0.25, 0.5]: row(f"rand{p}", *run(reqs, cap, m, "rand", p))
    row("hit2", *run(reqs, cap, m, "hit2"))
    for t in [0.05, 0.1, 0.2, 0.3, 0.5]: row(f"reuse{t}", *run(reqs, cap, m, "reuse", t))
    for t in [0.1, 0.2, 0.5, 1.0, 2.0, 4.0]: row(f"anchor{t}", *run(reqs, cap, m, "anchor", t))
