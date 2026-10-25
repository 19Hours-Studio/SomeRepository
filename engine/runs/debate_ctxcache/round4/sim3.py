# Round-2 replay. Same session model as round1/replay2 with critic1's in-place bookkeeping fix, plus:
#   * work is fixed in TOOL CALLS (50); a request may carry b>1 independent calls (parallel tool use)
#   * idle gaps longer than the cache TTL, with client policies expire / keepalive-ping / ski-rental pings
#   * retention sweep for provider span ops vs the best client policy (errata)
#   * sub-agent delegation (live-context lever)
# API units = multiples of base input price.  Prices: w = write multiplier, r = read multiplier.
import random, statistics, math

PR = {"anth5m": dict(w=1.25, r=0.10, ttl=5), "openai56": dict(w=1.25, r=0.10, ttl=30),
      "openai_legacy": dict(w=1.00, r=0.10, ttl=5)}

def session(policy, seed=0, calls=50, sys_tok=10_000, tool=2_000, out=300, edit_every=5, diff=200,
            q2=0.0, q4=0.0, window=None, trigger=None, target=None, k=32, ph=20, price="anth5m",
            idle_p=0.0, idle_min=15, ttl_policy="expire"):
    """q2/q4: probability a request carries 2/4 independent calls (else 1). Returns dict of API costs."""
    p = PR[price]; rng = random.Random(seed); gaps = random.Random(seed + 10_000); nid = 0
    ctx = [[0, sys_tok, "sys"]]; prev_pos = {}
    api = reads = writes = pings = hit = resent = 0.0; done = 0; nreq = 0; pending_out = 0
    while done < calls:
        b = 1
        if q2 + q4 > 0: u = rng.random(); b = 4 if u < q4 else 2 if u < q4 + q2 else 1
        b = min(b, calls - done)
        # edits that fall due during this request's calls (one per edit_every calls)
        n_edit = sum(1 for c in range(done, done + b) if c and c % edit_every == 0)
        patched = []
        for _ in range(n_edit):
            tools = [i for i, s in enumerate(ctx) if s[2] == "tool"]
            if not tools: break
            i = rng.choice(tools); s = ctx[i]; nid += 1
            if policy == "inplace":   patched.append((nid, rng.randrange(0, s[1]))); ctx[i] = [nid, s[1], "tool"]
            elif policy == "append_full": s[2] = "stale"; ctx.append([nid, tool, "tool"])
            elif policy == "errata":  s[2] = "stale"; ctx.append([nid, diff, "erratum"])
            elif policy == "punch":   del ctx[i]; ctx.append([nid, tool, "tool"])
            elif policy == "patch":   patched.append(("patch", s[0]))
        L = sum(s[1] for s in ctx)
        if window and L > trigger:
            j = 1
            while L > target and j < len(ctx) - 1:
                s = ctx[j]
                if s[2] != "sys" and s[1] > ph:
                    if policy in ("punch", "patch"): del ctx[j]; L -= s[1]; continue
                    nid += 1; ctx[j] = [nid, ph, "cleared"]; L -= s[1] - ph
                j += 1
        L = sum(s[1] for s in ctx)
        cached = 0
        if policy in ("punch", "patch"):
            last = None; extra = 0
            for s in ctx:
                if s[0] in prev_pos:
                    if last is not None and prev_pos[s[0]] != last + 1: extra += min(k, s[1])
                    last = prev_pos[s[0]]; cached += s[1]
            extra += (k + diff) * len(patched); cached -= extra
        else:
            for n, s in enumerate(ctx):
                if prev_pos.get(s[0]) == n: cached += s[1]; continue
                for pid, cut in patched:
                    if s[0] == pid: cached += cut
                break
        old = sum(s[1] for s in ctx if s[0] in prev_pos)   # tokens sent before (re-sent)
        # idle gap before this request (not before the first)
        if nreq and gaps.random() < idle_p:
            G = idle_min; T = p["ttl"]; step = T - 0.5          # ping just before expiry
            need = max(0, math.ceil(G / step) - 1)              # pings to bridge the gap
            if ttl_policy == "keepalive": pings += need * p["r"] * Lprev
            elif ttl_policy == "ski":                            # online: ping up to n* then let it expire
                nstar = int((p["w"] - p["r"]) / p["r"])
                if need <= nstar: pings += need * p["r"] * Lprev
                else: pings += nstar * p["r"] * Lprev; cached = 0
            elif ttl_policy == "expire" and G > T: cached = 0
        api += p["r"] * cached + p["w"] * (L - cached)
        reads += p["r"] * cached; writes += p["w"] * (L - cached)
        hit += min(cached, old); resent += old
        prev_pos = {s[0]: n for n, s in enumerate(ctx)}; Lprev = L
        for j in range(b): nid += 1; ctx.append([nid, tool + (out * b if j == b - 1 else 0), "tool"])
        done += b; nreq += 1
    return dict(api=api + pings, reads=reads, writes=writes, pings=pings, nreq=nreq,
                hit_resent=hit / max(resent, 1))

def avg(policy, seeds=100, **kw):
    r = [session(policy, seed=s, **kw) for s in range(seeds)]
    return {key: statistics.mean(x[key] for x in r) for key in r[0]}

if __name__ == "__main__":
    print("== 0. sanity: matches round1 (anth5m, 50 calls, 1/request) ==")
    base = {pol: avg(pol) for pol in ("inplace", "append_full", "errata", "punch", "patch")}
    for pol, x in base.items():
        print(f"{pol:12s} API={x['api']:9,.0f} reads={x['reads']:9,.0f} writes={x['writes']:9,.0f}"
              f" hit_resent={x['hit_resent']:.4f} vs inplace {x['api']/base['inplace']['api']-1:+.1%}"
              f" vs append_full {x['api']/base['append_full']['api']-1:+.1%}")
    print("\n== 0b. prices: openai56 (w=1.25,r=0.1,30m TTL) equals anth5m without idle; legacy w=1.0 ==")
    for pr in ("openai56", "openai_legacy"):
        a = {pol: avg(pol, price=pr)["api"] for pol in ("inplace", "append_full", "errata")}
        print(f"{pr:14s} errata {a['errata']/a['inplace']-1:+.1%} vs inplace, {a['errata']/a['append_full']-1:+.1%} vs append_full")
    print("\n== 0c. read-price sensitivity (unverified 0.05x on newer Anthropic models) ==")
    PR["anth_r05"] = dict(w=1.25, r=0.05, ttl=5)
    a = {pol: avg(pol, price="anth_r05")["api"] for pol in ("inplace", "append_full", "errata")}
    print(f"r=0.05: errata {a['errata']/a['inplace']-1:+.1%} vs inplace, {a['errata']/a['append_full']-1:+.1%} vs append_full")

    print("\n== 1. fewer requests: share of calls issued in parallel groups (errata, same 50 calls) ==")
    e1 = base["errata"]["api"]; a1 = base["append_full"]["api"]
    for q2, q4 in ((0, 0), (0.3, 0), (0.5, 0), (1, 0), (0, 0.5), (0, 1)):
        x = avg("errata", q2=q2, q4=q4); y = avg("append_full", q2=q2, q4=q4)
        print(f"q2={q2:.1f} q4={q4:.1f}: requests={x['nreq']:5.1f} errata {x['api']:9,.0f} ({x['api']/e1-1:+.1%} vs errata seq,"
              f" {x['api']/a1-1:+.1%} vs append_full seq); append_full batched {y['api']/a1-1:+.1%}")
    print("   baseline already parallel at q2=0.3 -> errata with q2=1:")
    b0 = avg("append_full", q2=0.3)["api"]; b1 = avg("errata", q2=1)["api"]; b2 = avg("errata", q4=1)["api"]
    print(f"   {b1/b0-1:+.1%} (pairs), {b2/b0-1:+.1%} (quads) vs append_full at q2=0.3")

    print("\n== 2. idle gaps > TTL (errata, sequential): fraction of requests preceded by an idle gap ==")
    for pr in ("anth5m", "openai56"):
        for G in (15, 45, 120):
            for f in (0.05, 0.2):
                row = {tp: avg("errata", price=pr, idle_p=f, idle_min=G, ttl_policy=tp, seeds=40) for tp in ("expire", "keepalive", "ski")}
                ref = avg("errata", price=pr, seeds=40)["api"]
                print(f"{pr:8s} gap {G:3d} min f={f:.2f}: expire {row['expire']['api']/ref-1:+6.1%}"
                      f"  keepalive {row['keepalive']['api']/ref-1:+6.1%}  ski-rental {row['ski']['api']/ref-1:+6.1%}"
                      f"  (hit_resent expire {row['expire']['hit_resent']:.3f})")

    print("\n== 3. provider span ops vs errata by retention (200 calls, 200k window, trigger 195k) ==")
    for tgt in (15_000, 40_000, 100_000, 140_000, 170_000, 185_000):
        trig = 195_000 if tgt > 40_000 else 60_000
        R = {pol: avg(pol, seeds=20, calls=200, window=200_000, trigger=trig, target=tgt)["api"]
             for pol in ("append_full", "errata", "punch", "patch")}
        print(f"target {tgt//1000:3d}k (trig {trig//1000}k): errata {R['errata']:11,.0f}  punch {R['punch']/R['errata']-1:+.1%}"
              f"  patch {R['patch']/R['errata']-1:+.1%} vs errata;  errata {R['errata']/R['append_full']-1:+.1%} vs append_full")
    print("   combined with pairs (q2=1) at 170k:")
    R = {pol: avg(pol, seeds=20, calls=200, window=200_000, trigger=195_000, target=170_000, q2=qq)["api"]
         for pol, qq in (("append_full", 0), ("errata", 0), ("patch", 1), ("errata_b", 1)) if pol != "errata_b"}
    R["errata_b"] = avg("errata", seeds=20, calls=200, window=200_000, trigger=195_000, target=170_000, q2=1)["api"]
    print(f"   errata+pairs {R['errata_b']/R['append_full']-1:+.1%}, patch+pairs {R['patch']/R['append_full']-1:+.1%} vs append_full sequential")
