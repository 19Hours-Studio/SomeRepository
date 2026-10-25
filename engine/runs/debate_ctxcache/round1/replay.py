# Round-1 replay. Billing in units of base input price. Fixes vs baseline calc.py:
#  - tokens never sent before (new tool output, previous assistant reply, turn-0 system prompt) are WRITES
#  - in-place edit diverges at a uniform point inside the changed segment (fairer to the baseline)
#  - finite context window; compaction = clear oldest tool results (Anthropic clear_tool_uses style)
#  - baselines: in-place edit, and append-full re-read (what coding agents already do)
#  - provider-side "punch": deleted/superseded spans are dropped from the block table, rest billed as hits,
#    k boundary tokens after each contiguous hole recomputed (EPIC-style) and billed as writes
import random, statistics, sys

PR = {"anthropic5m": dict(w=1.25, r=0.10), "openai": dict(w=1.00, r=0.10)}

def run(policy, seed=0, turns=50, sys_tok=10_000, tool=2_000, out=300, edit_every=5, diff=200,
        window=None, trigger=None, target=None, k=32, price="anthropic5m", placeholder=20):
    p = PR[price]; rng = random.Random(seed); nid = [0]
    def seg(size, kind):
        nid[0] += 1; return dict(id=nid[0], size=size, kind=kind)
    ctx = [seg(sys_tok, "sys")]
    prev = []                         # previous request: list of (id, size)
    cost = hit = tot = new_tot = 0; comp = 0; maxL = 0
    for t in range(turns):
        div_inside = None             # in-place edit: (segment id, tokens kept)
        if t and t % edit_every == 0:
            tools = [i for i, s in enumerate(ctx) if s["kind"] == "tool"]
            if tools:
                i = rng.choice(tools); s = ctx[i]
                if policy == "inplace":
                    keep = rng.randrange(0, s["size"])
                    ns = seg(s["size"], "tool"); ns["prefix_of"] = (s["id"], keep); ctx[i] = ns
                elif policy == "append_full":
                    s["kind"] = "stale"; ctx.append(seg(tool, "tool"))
                elif policy == "errata":
                    s["kind"] = "stale_base"; ctx.append(seg(diff, "erratum"))
                elif policy == "punch":
                    del ctx[i]; ctx.append(seg(tool, "tool"))
        # compaction when over trigger: clear oldest tool/stale segments to a placeholder
        L = sum(s["size"] for s in ctx)
        if window and L > trigger:
            j = 1
            while L > target and j < len(ctx) - 1:
                s = ctx[j]
                if s["kind"] in ("tool", "stale", "stale_base", "erratum") and s["size"] > placeholder:
                    if policy == "punch":
                        del ctx[j]; L -= s["size"]; continue
                    ns = seg(placeholder, "cleared"); ctx[j] = ns; L -= s["size"] - placeholder
                j += 1
            comp += 1
        L = sum(s["size"] for s in ctx); maxL = max(maxL, L)
        if window: assert L <= window, (policy, t, L)
        # billing
        if policy == "punch":
            prev_ids = {i for i, _ in prev}
            cached = 0; boundary = 0; hole = False; pi = 0
            prev_order = [i for i, _ in prev]
            # a hole = some previously-present ids disappeared between two kept ones
            kept = [s for s in ctx if s["id"] in prev_ids]
            pos = {i: n for n, i in enumerate(prev_order)}
            last = -1
            for s in kept:
                if pos[s["id"]] != last + 1: boundary += min(k, s["size"]) if last >= 0 else 0
                last = pos[s["id"]]
                cached += s["size"]
            cached -= boundary
        else:
            cached = 0
            for n, s in enumerate(ctx):
                if n < len(prev) and prev[n][0] == s["id"]:
                    cached += s["size"]; continue
                if "prefix_of" in s and n < len(prev) and prev[n][0] == s["prefix_of"][0]:
                    cached += s["prefix_of"][1]
                break
        newtok = sum(s["size"] - (s["prefix_of"][1] if "prefix_of" in s else 0)
                     for s in ctx if s["id"] not in {i for i, _ in prev})
        cost += p["r"] * cached + p["w"] * (L - cached); hit += cached; tot += L; new_tot += newtok
        prev = [(s["id"], s["size"]) for s in ctx]
        ctx.append(seg(tool + out, "tool"))
    return dict(cost=cost, hit=hit / tot, hit_old=hit / max(1, tot - new_tot), maxL=maxL, comp=comp,
                floor=None)

def mean_cost(policy, seeds=200, **kw):
    r = [run(policy, seed=s, **kw) for s in range(seeds)]
    return (statistics.mean(x["cost"] for x in r), statistics.mean(x["hit"] for x in r),
            statistics.mean(x["hit_old"] for x in r), max(x["maxL"] for x in r),
            statistics.mean(x["comp"] for x in r), [x["cost"] for x in r])

if __name__ == "__main__":
    POL = ["inplace", "append_full", "errata", "punch"]
    print("== A. 50 turns, no window (seed 0, then 200-seed mean) ==")
    for price in PR:
        base = None
        for pol in POL:
            r0 = run(pol, price=price)
            m, h, ho, mx, _, cs = mean_cost(pol, price=price)
            base = base or m
            print(f"{price:11s} {pol:12s} seed0 cost={r0['cost']:9,.0f} hit={r0['hit']:.4f} | "
                  f"mean cost={m:9,.0f} ({m/base-1:+.1%} vs inplace) hit={h:.4f} hit_on_resent={ho:.4f} maxctx={mx:,}")
    print("\n== B. long sessions, 200k window, compaction; best trigger/target per policy ==")
    W = 200_000
    for turns in (100, 200, 500):
        rows = {}
        for pol in POL:
            best = None
            for trig in (150_000, 180_000, 195_000):
                for tgt in (40_000, 70_000, 100_000, 130_000, 160_000):
                    if tgt >= trig: continue
                    m, h, ho, mx, c, _ = mean_cost(pol, seeds=40, turns=turns, window=W, trigger=trig, target=tgt)
                    if best is None or m < best[0]: best = (m, h, ho, mx, c, trig, tgt)
            rows[pol] = best
        b = rows["inplace"][0]; a = rows["append_full"][0]
        for pol, (m, h, ho, mx, c, trig, tgt) in rows.items():
            print(f"turns={turns:3d} {pol:12s} cost={m:11,.0f} vs inplace {m/b-1:+.1%} vs append_full {m/a-1:+.1%} "
                  f"hit={h:.4f} hit_on_resent={ho:.4f} compactions={c:.1f} best trig/tgt={trig//1000}k/{tgt//1000}k")
    print("\n== C. punch sensitivity to boundary recompute k (200 turns) ==")
    for kk in (0, 32, 256, 2048):
        m = mean_cost("punch", seeds=40, turns=200, window=W, trigger=195_000, target=160_000, k=kk)[0]
        print(f"k={kk:5d} cost={m:,.0f}")
