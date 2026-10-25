"""Exact-arithmetic cost models for the ideas. Units: base input-token price = 1.
Anthropic multipliers (platform.claude.com docs): write 5m 1.25, write 1h 2.0, read 0.1
(0.05 on Opus/Sonnet 5.5, 0.025 on Fable 5.1). Output price assumed 5x input."""
from fractions import Fraction as F

W5, W1H, R, OUT = F(5, 4), F(2), F(1, 10), F(5)

print("== 1. Agent bill composition at a 100% achievable hit rate (append-only)")
S, a, T, o = 20000, 2000, 50, 300  # base ctx, tokens appended per turn, turns, output/turn
reads = sum(R * (S + a * t) for t in range(T))
writes = W5 * (S + a * T)
outs = OUT * o * T
tot = reads + writes + outs
print(f"  cached reads {float(reads):.0f} ({float(reads/tot):.1%}), writes {float(writes):.0f} "
      f"({float(writes/tot):.1%}), output {float(outs):.0f} ({float(outs/tot):.1%})")
nocache = sum(S + a * t for t in range(T)) + outs
print(f"  vs no caching {float(nocache):.0f}: {float(nocache/tot):.2f}x cheaper")
for hr in (F(9, 10), F(95, 100)):
    # a fraction (1-hr) of each turn's *previously cached* context is rewritten
    extra = sum((1 - hr) * (S + a * t) * (W5 - R) for t in range(1, T))
    print(f"  if only {float(hr):.0%} of the old context hits each turn: +{float(extra/tot):.1%} bill")

print("== 2. Middle edit: rewrite in place vs append a correction (journal)")
N, p, j = 100000, 30000, 400  # context, edit position, correction size
inplace = R * p + W5 * (N - p)
journal = R * N + W5 * j
print(f"  this turn: in-place {float(inplace):.0f} vs journal {float(journal):.0f} "
      f"-> {float(inplace/journal):.1f}x")
# Each later turn pays R*j extra for the journal entry; break-even number of turns:
be = (inplace - journal) / (R * j)
print(f"  journal stays cheaper for {float(be):.0f} later turns (each re-reads j at 0.1x)")
# Ski rental: compact (rewrite from earliest edit p_min) once accumulated journal re-read
# spend reaches the compaction cost C = (W5-R)*(N-p_min); total <= 2x optimal offline.
C = (W5 - R) * (N - p)
print(f"  ski-rental rule: compact when sum of 0.1*journal tokens re-read >= {float(C):.0f} "
      f"(= {float(C/R):.0f} journal-token-turns)")

print("== 3. Idle gap longer than the 5-min TTL: keep-alive vs rewrite vs 1h write")
for N in (20000, 100000):
    ping = R * N  # 1-token-output request every <5 min refreshes TTL (output cost negligible)
    rewrite = W5 * N
    print(f"  N={N}: one ping {float(ping):.0f}; a miss rewrite {float(rewrite):.0f}; "
          f"pings worth it up to {float(rewrite/ping):.1f} pings (~{float(rewrite/ping)*5:.0f} min) "
          f"if return certain; 1h write premium over 5m {float((W1H-W5)*N):.0f} = "
          f"{float((W1H-W5)/R):.1f} pings")
    for q in (F(1, 2), F(4, 5)):
        print(f"    P(return)={float(q):.0%}: ping while q*(1.25-0.1)N > 0.1N per ping -> "
              f"break-even pings {float(q*(W5-R)/R):.1f}")

print("== 4. Own stack: RAG/agent request with k reused chunks in a new order / new position")
L, d_model, layers, params = 32, 4096, 32, 8e9  # Llama-3-8B-like
kv_bytes = 2 * layers * 8 * 128 * 2  # K+V, 8 KV heads, head dim 128, BF16
print(f"  KV bytes/token (8B GQA BF16) = {kv_bytes} = {kv_bytes/1024:.0f} KiB")
def prefill_flops(n_new, ctx_before):
    lin = 2 * params * n_new
    attn = 4 * layers * d_model * sum(ctx_before + i for i in range(0, n_new, 64)) * 64
    return lin + attn
k, c, q, sysp = 8, 512, 150, 1000
n = sysp + k * c + q
full = prefill_flops(n, 0)
prefix = prefill_flops(k * c + q, sysp)  # only system prompt hits when order/set changes
for name, frac in (("EPIC 32 sink tok/chunk", 32 / c), ("CacheBlend r=15%", 0.15),
                   ("sink+15%+boundary 16", 32 / c + 0.15 + 16 / c), ("r=30% (multi-hop)", 0.30)):
    rec = int(frac * k * c)
    pic = prefill_flops(q + rec, sysp + k * c - rec)
    print(f"  {name:24s}: compute {pic/full:.3f} of full, {pic/prefix:.3f} of prefix-cache; "
          f"token hit {(sysp + k*c - rec)/n:.3f} vs prefix {sysp/n:.3f}")
gb = k * c * kv_bytes / 1e9
print(f"  KV to load for {k*c} reused tokens: {gb:.3f} GB -> {gb/50*1e3:.1f} ms @PCIe5 50GB/s, "
      f"{gb/7*1e3:.0f} ms @NVMe 7GB/s; full prefill ~{full/6e14*1e3:.0f} ms @600 TFLOP/s eff.")
for model, kvb in (("70B (80L, GQA8)", 2 * 80 * 8 * 128 * 2),):
    print(f"  {model}: {kvb/1024:.0f} KiB/token; 1M cached tokens = {kvb*1e6/1e9:.0f} GB")

print("== 5. Sparse read of cached context (Quest-style top-K pages), decode/new-token attention")
for ctx in (32000, 128000):
    for budget in (2048, 4096):
        print(f"  ctx {ctx}, budget {budget}: KV bytes read per step {budget/ctx:.3f} of dense "
              f"(+ page metadata 2/16 of keys = {2/16/2:.3f} of KV)")
