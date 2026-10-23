"""Chain-level SSD admission (fixes prefix dependency found in sim_admit.py: a deep block is useless
without its ancestors). DRAM LRU tier (cap blocks) -> SSD (unbounded, write-limited).
At each request's end, policy decides whether to persist its full prefix chain to SSD
(bytes written = chain blocks not already on SSD).
  rand(p)   : persist chain with prob p                      (cheapest filter)
  hit2      : persist only chains of requests that themselves hit (k>0) (second-hit analogue)
  reuse(t)  : learned P(chain reused | bucket) >= t          (reuse-only, no FLOP term)
  anchor(t) : P(reused|bucket) * chain_FLOPs / chain_new_bytes >= t   (the idea's score)
bucket = (hit?, log2 chain length). Labels: a chain counts as reused if a later request's
matched prefix covers >= its last block. Learned online (Beta(0.5,1) prior).
Usage: python3 -I sim_chain.py TRACE CAP_BLOCKS MODEL
"""
import json, sys, math, random
from collections import OrderedDict, defaultdict
sys.path.insert(0, '.')
from sim_evict import MODELS, block_flops

def run(reqs, cap_d, m, pol, t=0.0):
    rng = random.Random(1)
    dram = OrderedDict(); ssd = set()
    pending = {}       # tail hash -> bucket (chain persisted or not; for learning)
    n_b = defaultdict(lambda: 1.0); r_b = defaultdict(lambda: 0.5)
    written = allw = 0; tot = saved = 0.0
    seen_tail = set()
    for r in reqs:
        hs = r["hash_ids"]; k = 0
        while k < len(hs) and (hs[k] in dram or hs[k] in ssd):
            k += 1
        cost = [block_flops(m, j) for j in range(len(hs))]
        tot += sum(cost); saved += sum(cost[:k])
        # label: any earlier tail that lies within the longest previously-seen prefix of this request
        for j, h in enumerate(hs):
            b = pending.pop(h, None)
            if b is not None:
                r_b[b] += 1
        for j, h in enumerate(hs):
            if h in dram: dram.move_to_end(h)
            else: dram[h] = j
        while len(dram) > cap_d: dram.popitem(last=False)
        new = [h for h in hs if h not in ssd]
        allw += len(new)
        b = (min(k, 2), int(math.log2(len(hs) + 1)))
        n_b[b] += 1; pending[hs[-2] if len(hs) > 1 else hs[-1]] = b  # last FULL block (tail block is partial)
        p = r_b[b] / n_b[b]
        if pol == "all": ok = True
        elif pol == "rand": ok = rng.random() < t
        elif pol == "hit2": ok = k >= 2   # block 0 is a shared system prompt in these traces
        elif pol == "reuse": ok = p >= t
        else:
            dens = sum(cost[j] for j, h in enumerate(hs) if h not in ssd) / max(len(new), 1) / block_flops(m, 0)
            ok = p * dens >= t
        if ok:
            ssd.update(new); written += len(new)
    return written / allw, saved / tot

if __name__ == "__main__":
    reqs = [json.loads(l) for l in open(sys.argv[1])]
    cap = int(sys.argv[2]); m = MODELS[sys.argv[3]]
    _, f0 = run(reqs, cap, m, "rand", 0.0); _, f1 = run(reqs, cap, m, "all")
    print(f"# {sys.argv[1].split('/')[-1]} model={sys.argv[3]} DRAM={cap*512/1e6:.2f}M tok | DRAM-only {f0:.3f}  write-all {f1:.3f}")
    rows = [("rand", p) for p in (0.1, 0.25, 0.5, 0.75)] + [("hit2", 0)] + \
           [("reuse", t) for t in (0.2, 0.3, 0.4, 0.5, 0.6)] + [("anchor", t) for t in (0.3, 0.5, 1, 2, 4, 8)]
    for pol, t in rows:
        w, f = run(reqs, cap, m, pol, t)
        print(f"{pol}{t:<5} writes={w:.3f} flops_saved={f:.3f} SSDvalue_kept={(f-f0)/(f1-f0):.2f} value_per_write={(f-f0)/(f1-f0)/max(w,1e-9):.2f}")
