# TTL policies for the errata session (anth5m reference without idle gaps = 479,425).
import sim3 as S
S.PR["anth1h"] = dict(w=2.0, r=0.10, ttl=60)
ref = S.avg("errata", seeds=40)["api"]
print(f"reference (no idle) {ref:,.0f}; 1h-TTL writes with no idle {S.avg('errata', price='anth1h', seeds=40)['api']/ref-1:+.1%}")
for G in (15, 45, 120):
    for f in (0.05, 0.2):
        r = {}
        for tp in ("expire", "keepalive", "ski"): r[tp] = S.avg("errata", idle_p=f, idle_min=G, ttl_policy=tp, seeds=40)["api"]
        r["1h"] = S.avg("errata", price="anth1h", idle_p=f, idle_min=G, ttl_policy="expire", seeds=40)["api"]
        best = min(r, key=r.get)
        print(f"gap {G:3d} min f={f:.2f}: " + "  ".join(f"{k} {v/ref-1:+6.1%}" for k, v in r.items()) + f"  -> best {best}"
              f" ({r[best]/r['expire']-1:+.0%} vs expire)")
