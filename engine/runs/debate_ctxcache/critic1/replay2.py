# Round-1 replay v2 (supersedes replay.py; same model, faster, adds "patch" and own-stack $ costing).
# Units: API bill in multiples of base input price; own-stack bill in $ on H100 (assumptions below).
# Session: system prompt, then each turn appends tool output + previous assistant reply (never sent before =
# cache WRITE). Every `edit_every` turns an earlier tool output changes (file re-read / state update).
# Policies for that change:
#   inplace     edit segment in place; prefix cache diverges at a uniform point inside it   (exact, baseline)
#   append_full append the new full version, keep stale copy (what coding agents already do) (exact for that prompt)
#   errata      append a `diff`-token erratum, keep stale base                             (exact for that prompt)
#   punch       provider op: drop stale span's KV blocks, append new full version; k boundary tokens recomputed
#   patch       provider op: replace span in place; only the `diff` new tokens + k boundary tokens computed,
#               later KV reused unchanged (approximate, CacheBlend/EPIC-like)
# Compaction (window): clear oldest tool results to a 20-token placeholder; client policies rewrite the suffix
# from the first cleared point, punch/patch drop blocks (k boundary recompute per hole).
import random, statistics

PR = {"anthropic5m": dict(w=1.25, r=0.10), "openai": dict(w=1.00, r=0.10)}
# own stack: Llama-3-70B-class, BF16 KV, H100 $2/h, 45% MFU, 3.35 TB/s
LIN, ATT, KVB, GPU_S, FLOPS, HBM = 2 * 70e9, 4 * 80 * 8192, 2 * 80 * 8 * 128 * 2, 2.0 / 3600, 0.45 * 989e12, 3.35e12
DRAM_GBS = 4 / (3 * 8760 * 3600)          # DRAM capex $4/GB over 3 years, per GB-second

def own_cost(L, cached, extra_recompute, out, gap_s):
    m = L - cached                           # tokens computed (positions cached..L)
    fl = LIN * (m + extra_recompute) + ATT * (m * (cached + L) / 2 + extra_recompute * L / 2)
    pre = fl / FLOPS * GPU_S
    dec = out * L * KVB / HBM * GPU_S        # KV reads during decode (weights shared by batch, KV not)
    hold = L * KVB / 1e9 * DRAM_GBS * gap_s  # park KV in DRAM between turns
    return pre, dec, hold

def run(policy, seed=0, turns=50, sys_tok=10_000, tool=2_000, out=300, edit_every=5, diff=200,
        window=None, trigger=None, target=None, k=32, price="anthropic5m", ph=20, gap_s=30):
    p = PR[price]; rng = random.Random(seed); nid = 0
    ctx = [[0, sys_tok, "sys"]]                 # [id, size, kind]
    prev_pos = {}                               # id -> index in previous request
    api = hit = tot = newt = 0.0; own = [0.0, 0.0, 0.0]; comp = 0; maxL = 0
    for t in range(turns):
        patched = None
        if t and t % edit_every == 0:
            tools = [i for i, s in enumerate(ctx) if s[2] == "tool"]
            i = rng.choice(tools); s = ctx[i]; nid += 1
            if policy == "inplace":
                patched = (nid, rng.randrange(0, s[1])); ctx[i] = [nid, s[1], "tool"]
            elif policy == "append_full":
                s[2] = "stale"; ctx.append([nid, tool, "tool"])
            elif policy == "errata":
                s[2] = "stale"; ctx.append([nid, diff, "erratum"])
            elif policy == "punch":
                del ctx[i]; ctx.append([nid, tool, "tool"])
            elif policy == "patch":            # span keeps its id (KV reused) except `diff` new tokens
                patched = ("patch", s[0])
        L = sum(s[1] for s in ctx)
        if window and L > trigger:
            j = 1
            while L > target and j < len(ctx) - 1:
                s = ctx[j]
                if s[2] != "sys" and s[1] > ph:
                    if policy in ("punch", "patch"):
                        del ctx[j]; L -= s[1]; continue
                    nid += 1; ctx[j] = [nid, ph, "cleared"]; L -= s[1] - ph
                j += 1
            comp += 1
        L = sum(s[1] for s in ctx); maxL = max(maxL, L)
        if window: assert L <= window
        new = sum(s[1] for s in ctx if s[0] not in prev_pos)
        extra = 0
        if policy in ("punch", "patch"):
            cached = 0; last = None
            for s in ctx:
                if s[0] in prev_pos:
                    if last is not None and prev_pos[s[0]] != last + 1: extra += min(k, s[1])
                    last = prev_pos[s[0]]; cached += s[1]
            if patched: extra += k; cached -= diff; new += diff
            cached -= extra
            # in patch/punch the boundary tokens are recomputed (billed as writes, costed as extra compute)
            fl_pre = (LIN * (new) + ATT * new * L) + (LIN * extra + ATT * extra * L / 2)
            pre = fl_pre / FLOPS * GPU_S
            dec = out * L * KVB / HBM * GPU_S; hold = L * KVB / 1e9 * DRAM_GBS * gap_s
        else:
            cached = 0
            for n, s in enumerate(ctx):
                if prev_pos.get(s[0]) == n: cached += s[1]; continue
                if patched and s[0] == patched[0]: cached += patched[1]; new += s[1] - patched[1]
                break
            pre, dec, hold = own_cost(L, cached, 0, out, gap_s)
        api += p["r"] * cached + p["w"] * (L - cached); hit += cached; tot += L; newt += new
        own[0] += pre; own[1] += dec; own[2] += hold
        prev_pos = {s[0]: n for n, s in enumerate(ctx)}
        nid += 1; ctx.append([nid, tool + out, "tool"])
    return dict(api=api, hit=hit / tot, hit_old=hit / (tot - newt), maxL=maxL, comp=comp, own=own,
                floor_api=p["r"] * (tot - newt) + p["w"] * newt)

def avg(policy, seeds=100, **kw):
    r = [run(policy, seed=s, **kw) for s in range(seeds)]
    f = lambda key: statistics.mean(x[key] for x in r)
    own = [statistics.mean(x["own"][i] for x in r) for i in range(3)]
    return dict(api=f("api"), hit=f("hit"), hit_old=f("hit_old"), maxL=max(x["maxL"] for x in r),
                comp=f("comp"), own=own, floor=f("floor_api"),
                api_min=min(x["api"] for x in r), api_max=max(x["api"] for x in r))

POL = ["inplace", "append_full", "errata", "punch", "patch"]
if __name__ == "__main__":
    print("== A. 50 turns, no window, 100 seeds ==")
    for price in PR:
        R = {pol: avg(pol, price=price) for pol in POL}
        b, a = R["inplace"]["api"], R["append_full"]["api"]
        for pol, x in R.items():
            o = sum(x["own"])
            print(f"{price:11s} {pol:12s} API={x['api']:9,.0f} ({x['api']/b-1:+.1%} vs inplace, {x['api']/a-1:+.1%} vs append_full)"
                  f" hit={x['hit']:.4f} hit_resent={x['hit_old']:.4f} maxctx={x['maxL']:,}"
                  + (f" | own ${o:.3f} (prefill {x['own'][0]:.3f} decode {x['own'][1]:.3f} hold {x['own'][2]:.4f})"
                     f" {o/sum(R['inplace']['own'])-1:+.1%} vs inplace, {o/sum(R['append_full']['own'])-1:+.1%} vs append_full"
                     if price == "anthropic5m" else ""))
    for pol in POL: print(f"{pol:12s} no-miss floor for its own prompt = {R[pol]['floor']:,.0f}")
    print("\n== B. 200k window; per policy best (trigger,target); 30 seeds ==")
    W = 200_000
    for turns in (100, 200, 400):
        R = {}
        for pol in POL:
            best = None
            for trig in (150_000, 195_000):
                for tgt in (40_000, 100_000, 140_000):
                    x = avg(pol, seeds=30, turns=turns, window=W, trigger=trig, target=tgt); x["tt"] = (trig, tgt)
                    if best is None or x["api"] < best["api"]: best = x
            R[pol] = best
        b, a = R["inplace"]["api"], R["append_full"]["api"]
        for pol, x in R.items():
            print(f"turns={turns:3d} {pol:12s} API={x['api']:11,.0f} ({x['api']/b-1:+.1%} vs inplace, {x['api']/a-1:+.1%} vs append_full)"
                  f" hit_resent={x['hit_old']:.4f} compactions={x['comp']:.1f} trig/tgt={x['tt'][0]//1000}k/{x['tt'][1]//1000}k"
                  f" own ${sum(x['own']):.2f}")
    print("\n== C. same target for all (quality-matched context budget 195k->140k), 200 turns ==")
    R = {pol: avg(pol, seeds=30, turns=200, window=W, trigger=195_000, target=140_000) for pol in POL}
    for pol, x in R.items():
        print(f"{pol:12s} API={x['api']:11,.0f} ({x['api']/R['inplace']['api']-1:+.1%} vs inplace, "
              f"{x['api']/R['append_full']['api']-1:+.1%} vs append_full) compactions={x['comp']:.1f}")
    print("\n== D. sensitivity: patch/punch boundary k; diff size; edit frequency (50 turns, Anthropic) ==")
    for kk in (0, 32, 256, 2000):
        print(f"k={kk:4d} patch {avg('patch', k=kk)['api']:,.0f}  punch {avg('punch', k=kk)['api']:,.0f}")
    for d in (50, 200, 1000, 2000):
        print(f"diff={d:4d} errata {avg('errata', diff=d)['api']:,.0f} patch {avg('patch', diff=d)['api']:,.0f}")
    for ee in (2, 5, 10, 25):
        R = {pol: avg(pol, edit_every=ee)["api"] for pol in POL}
        print(f"edit_every={ee:2d} " + " ".join(f"{pol}={v/R['inplace']-1:+.1%}" for pol, v in R.items()))
