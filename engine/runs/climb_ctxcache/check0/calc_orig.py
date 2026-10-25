# Exact arithmetic for the context-caching ideas. Prices as multiples of base input price.
import random
P = {"anthropic_5m": dict(w=1.25, r=0.10, miss=1.0), "openai_auto": dict(w=1.0, r=0.10, miss=1.0)}

print("== 1. erratum vs in-place rewrite: break-even turns ==")
for name, p in P.items():
    for N, pos, e in [(100_000, 50_000, 500), (100_000, 90_000, 2_000), (30_000, 5_000, 200)]:
        rewrite = p["w"] * (N - pos)           # suffix re-write once
        per_turn = p["r"] * e                   # erratum tokens re-read every later turn
        once = p["w"] * e
        print(f"{name:13s} N={N} edit@{pos} e={e}: rewrite={rewrite:.0f}  erratum once={once:.0f} +{per_turn:.0f}/turn  break-even turns={(rewrite-once)/per_turn:.0f}")

print("\n== 1b. synthetic agent session replay (50 turns) ==")
def session(policy, seed=0, turns=50, sys_tok=10_000, tool=2_000, out=300, edit_every=5, edit_tok=1_000, p=P["anthropic_5m"]):
    rng = random.Random(seed); ctx = [sys_tok]; cost = 0; hit = 0; tot = 0; debt = 0.0
    for t in range(turns):
        div = sum(ctx)  # index of first divergent token vs previous request (default: everything cached)
        if t and t % edit_every == 0:   # a tool output earlier in context changes (file re-read, state update)
            k = rng.randrange(1, len(ctx))
            if policy == "inplace":
                div = sum(ctx[:k]); ctx[k] = ctx[k]   # same size, different content
            else:  # erratum appended; ski-rental compaction
                ctx.append(edit_tok); debt += p["r"] * edit_tok
                rewrite_cost = p["w"] * (sum(ctx) - sum(ctx[:k]))
                if policy == "erratum+ski" and debt >= rewrite_cost:
                    div = sum(ctx[:k]); debt = 0
        L = sum(ctx); cached = min(div, L)
        cost += p["r"] * cached + p["w"] * (L - cached); hit += cached; tot += L
        ctx.append(tool + out)
    return hit / tot, cost
base_full = None
for pol in ["inplace", "erratum", "erratum+ski"]:
    hr, c = session(pol)
    print(f"{pol:12s} token hit rate={hr:.4f} billed input units={c:,.0f}")
nocache = sum(10_000 + 2_300 * t for t in range(50))
print(f"no-cache reference ~{nocache:,} units (in-place ctx size)")

print("\n== 2. KV bytes/token and marginal cost of a cached token (own stack) ==")
models = {"Llama-3-70B BF16 (80L,8kv,128d)": 2*80*8*128*2, "Llama-3-70B FP8": 2*80*8*128*1,
          "DeepSeek-V3 MLA BF16 (61L,576)": 61*576*2}
gpu_hr, hbm_bw, flops_eff = 2.0, 3.35e12, 0.45*989e12   # H100 $2/h, 45% MFU dense BF16
for m, b in models.items():
    print(f"{m:34s} {b/1024:.0f} KB/token; 100k ctx = {b*1e5/1e9:.1f} GB")
b = models["Llama-3-70B BF16 (80L,8kv,128d)"]
prefill = 2*70e9/flops_eff*gpu_hr/3600*1e6
read_per_out = b/hbm_bw*gpu_hr/3600*1e6   # $ per M cached tokens per output token (KV read at decode)
print(f"prefill recompute: ${prefill:.3f}/M tok ; decode KV-read: ${read_per_out*1000:.3f}/M cached tok per 1000 output tokens")
for tier, usd_gb_h in [("HBM (H100 $2/h /80GB)", 2/80), ("DRAM ~$0.005/GB-h", 0.005), ("NVMe ~$0.0002/GB-h", 0.0002)]:
    print(f"store 1M tok 1h in {tier:22s}: ${usd_gb_h*b*1e6/1e9:.2f}")
print("transfer 1M tok over PCIe5 ~50GB/s:", f"{b*1e6/50e9:.1f} s")

print("\n== 3. blended (CacheBlend/EPIC) effective hit on non-prefix tokens ==")
for chunk in [256, 512, 1024]:
    for r_or_k in [("CacheBlend r=15%", 0.15), ("EPIC k=32 tok/chunk", 32/chunk)]:
        print(f"chunk={chunk:5d} {r_or_k[0]:20s} recompute frac={r_or_k[1]:.3f} -> eff hit={1-r_or_k[1]:.3f}")
