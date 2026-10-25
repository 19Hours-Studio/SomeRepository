# Compare the round-1 replay's append-only bill with the dollars SWE-agent actually recorded
# (litellm cost from real usage incl. cache reads/writes), per trajectory. Sonnet 4: $3/M input.
import json, sys, os, statistics as st
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import r1_traces as T
tr = T.load(sys.argv[1]); stats = {json.loads(l)["id"]: json.loads(l) for l in open(sys.argv[2])}
raw = {json.loads(l)["id"]: json.loads(l) for l in open(sys.argv[1])}
rat = []; tot_rep = tot_real = 0; outs = 0
for t in tr:
    ntok = [T.tok(x) for x in t["text"]]
    A = T.requests(t)
    seq = [T.ctx(t, ntok, a, set()) for a in A]
    c, hit, tok = T.bill(seq, 1.25, 0.10)
    out = sum(ntok[a] for a in A)                          # assistant messages = model output
    rep = (c * 3 + out * 15) / 1e6
    real = stats[t["id"]]["stats"]["instance_cost"]
    rat.append(real / rep); tot_rep += rep; tot_real += real
    assert stats[t["id"]]["stats"]["api_calls"] >= len(A) - 1
rat.sort()
print(f"200 traces: recorded ${tot_real:.2f} vs replayed append-only ${tot_rep:.2f}  ratio {tot_real/tot_rep:.3f}")
print(f"per-trace ratio recorded/replayed: p10 {rat[20]:.2f} median {rat[100]:.2f} p90 {rat[180]:.2f}")
print("history processors:", {json.dumps(s['history_processors']) for s in stats.values()})
calls = sum(s["stats"]["api_calls"] for s in stats.values()); print("api calls", calls, "replayed requests", sum(len(T.requests(t)) for t in tr))
