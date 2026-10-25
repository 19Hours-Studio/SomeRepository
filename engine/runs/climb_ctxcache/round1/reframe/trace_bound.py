# Replay Mooncake FAST'25 public traces (512-token blocks, chained hash_ids) with an INFINITE exact prefix cache.
# Question: how much of the billed input is (a) misses vs (b) re-reads of cached prefix?  => upper bound on any
# "raise hit rate" scheme (even a perfect 100%-hit, zero-quality-loss one).
import json, sys
W, R, O = 1.25, 0.10, 5.0   # Anthropic-style multipliers: cache write, cache read, output (Sonnet: $15 out / $3 in)
B = 512
def run(path):
    seen=set(); hit=miss=0; out=0; n=0
    for line in open(path):
        r=json.loads(line); h=r["hash_ids"]; L=r["input_length"]; n+=1
        k=0
        while k<len(h) and h[k] in seen: k+=1
        c=min(k*B, L); hit+=c; miss+=L-c; out+=r["output_length"]
        seen.update(h)
    tot=hit+miss
    cur = R*hit + W*miss                 # exact prefix caching, input bill
    perfect = R*tot                      # every token a hit (impossible upper bound for hit-rate work)
    print(f"{path.split('/')[-1]:26} req={n:6} tok_hit={hit/tot:.3f}  input_bill={cur/1e6:9.1f}M  "
          f"reads={R*hit/cur:.0%} writes={W*miss/cur:.0%} | 100%-hit bound: -{1-perfect/cur:.0%} input"
          f" | output share of (input+output) bill={O*out/(cur+O*out):.0%}")
for p in sys.argv[1:]: run(p)
