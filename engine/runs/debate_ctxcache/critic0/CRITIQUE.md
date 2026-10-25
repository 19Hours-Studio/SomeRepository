# Critique of baseline answer (ctxcache)
Scripts: recheck.py (replay fixed), recheck_storage.py (Idea 4). Author's calc.py reproduces exactly.

## Numbers that hold
- Break-even turns 1238 / 50 / 1550 (Anthropic), 990 / 40 / 1240 (OpenAI). Using buy=(1.25-0.1)(N-p): 1137 / 45. Conclusion unchanged.
- KV sizes 320 KB/tok (L3-70B BF16), 69 KB/tok (DSV3 MLA), ratio 4.66x; PCIe 6.6 s per 1M tok at 50 GB/s.
- Storage $8.19 / $1.64 / $0.066 per M-tok-h at the stated $/GB-h; recompute $0.175/M (linear FLOPs only).
- EPIC 32/512 = 6.25% recompute; CacheBlend ~15%; EPIC "up to 8x TTFT, negligible loss" (paper abstract).
- GPT-5 cached input $0.125 vs $1.25 = 0.1x (OpenAI GPT-5 Chat model page + trackers).

## Numbers that do not hold
1. Replay bug: each turn's new tool output + previous assistant output (2,300 tok) and the turn-0 system prompt
   are counted as cache READS (div = sum(ctx) taken after the append). Fixed:
   hit 92.9% -> 89.8% (in-place), 99.75% -> 96.3% (erratum); cost 604k->721k, 365k->506k;
   saving -40% -> -30% (seed 0). With a full 2k erratum (restating the changed tool output): -25%.
   Over 200 seeds: mean -33% (1k erratum) / -29% (2k), range -10%..-46%.
2. Ski-rental never fires in the replay (erratum == erratum+ski); debt accrued once per edit, not per turn.
   The 2x-competitive claim contributes 0 to the measured gain. With per-turn rent it fires 1x in 200 turns
   and was slightly worse (6.34M vs 6.18M); the binding constraint is the context window (ctx 141k @50 turns).
3. Baseline is partly a strawman: agents (Claude Code etc.) already append re-reads rather than edit in place;
   vs that practice Idea 1 gains ~0. Gain is real only vs in-place state (memory blocks, todo lists in sys prompt).
4. "Exact KV == full recomputation": exact for a *different* prompt (stale + correction), not the edited prompt.
5. Hash-sorting documents: a new doc lands at a random rank -> on average ~half the doc block is rewritten.
   First-seen (arrival) order is append-only and strictly better for evolving sets; sort also discards rank order.
6. Idea 3 hit rate for agent memory: AgentKVShift reports CacheBlend-style methods need 45-55% refresh there,
   so "85-94% hit" is RAG-only; agent memory ~45-55% (CacheBlend) or 70-90% (AgentKVShift, F1 0.284 vs 0.296).
7. Idea 4: recompute at 100k ctx is $0.338/M (attention +94%), not $0.175. DRAM priced at cloud rental
   ($0.005/GB-h) but compared with NVMe at block-storage price; on capex DRAM is $0.05/M-tok-h,
   break-even reuse interval 3.5-6.8 h, not 6 min. Ordering NVMe<DRAM<HBM stands, "20x" is basis-dependent.
8. Prior art missed: llama.cpp `--cache-reuse` (KV-shift chunk reuse after mid-prompt changes) ~ Idea 2;
   Gemini explicit context caching bills storage per token-hour ($4.50/M-h 2.5 Pro, $1/M-h Flash) ~ Idea 4.

## Undersold
- On previously-sent tokens Idea 1 hits ~100%; the remaining 3.7% miss is irreducible new content.
- Longer sessions: -37% at 200 turns, -43% at 500 (if window allowed).
- AgentKVShift is a better Idea-3 engine for agents than CacheBlend (10-30% refresh), not only a caveat.
