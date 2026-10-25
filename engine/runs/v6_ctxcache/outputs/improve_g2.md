I improved all three answers and ran a Python check for each. No idea reaches 3x or a hit rate near 100% for edited middles or rarely used documents. The best honest gains are about 1.2–1.8x (Idea 1), 1.1–1.25x on top of a strong baseline (Idea 2), and 1.0–1.5x on input cost depending on gap pattern (Idea 3). No answer-quality number was measured, because model weights can't be downloaded here.

=== IDEAS ===
IDEA 1
NAME: Popularity order with second-sighting cache writes
MECHANISM: Documents are still sent in order of descending global retrieval count from an online counter (ties broken by ID), with the system prompt first and the question last. Every hit is therefore an exact prefix match and the cached state is exact. Two changes fix the weak link.
(1) Second-sighting admission. The client keeps a list of document-prefix hashes it has seen recently, with no cached state behind them. A cache breakpoint is placed only at prefix depths already seen within the TTL window. Documents past that depth go after the last breakpoint and are billed at 1.0x instead of a 1.25x write. This is the CDN "cache on second hit" / TinyLFU admission idea applied to breakpoint placement.
(2) TTL by traffic regime. The 1-hour TTL (2x write cost) is used when the organisation sends fewer than about 1k requests per 5 minutes, and the 5-minute TTL otherwise.
Replay setup: 100k chunks, top-5, Zipf, 4 breakpoints at document depths 2–5, Anthropic multipliers, compared with sending documents uncached. Bill ratios across 10 to 1,000 requests per 5 minutes:
- Zipf 1.05: 1.06–1.24x
- Zipf 1.2: 1.19–1.44x
- Zipf 1.5: 1.46–1.83x
The old always-write rule gave 0.88–1.61x and lost money at low traffic. The method now never loses in any tested regime, and 1.5x holds at Zipf 1.5 from about 100 requests per 5 minutes (1.66x), where the old rule needed about 1k. It covers document reordering only. Quality effect: only the reordering itself. Test it by comparing F1/EM and the spread across permutations against relevance order on a real model.
VALUE: 1.06–1.83x cheaper per request than the best current API practice (documents uncached), with no approximated KV, and it runs client-side only. It no longer loses money at low traffic or flat popularity. Rarely retrieved documents still miss (23–60% of document tokens), so a hit rate near 100% is not reachable.

IDEA 2
NAME: Probe-gated blending, popularity-ordered exact fallback
MECHANISM: This runs on your own serving stack or provider-side only. The parts kept from before:
- position-independent chunk KV, stored before position rotation is applied;
- the EPIC fix (recompute each chunk's first tokens);
- CacheBlend's top-r recompute and the seam-window recompute;
- the layer-1 deviation probe that sends requests that look multi-source to the exact path.
The fix: flagged requests are no longer recomputed in relevance order, which reused only 17% (an 83% prefill). They are re-sent in Idea 1's popularity-first order, so the exact path reuses 0.40–0.77 of document tokens (prefill falls to 0.736, 0.630 and 0.450 of relevance order at Zipf 1.05, 1.2 and 1.5). At the realistic routed share m = 0.25, the bill against plain prefix caching is 1.46, 1.50 and 1.55x (was 1.39x). The largest m that still keeps 1.5x rises from 0.12 to 0.19, 0.24 and 0.46. The honest stronger baseline is prefix caching plus popularity order. Against it, blending adds only 1.25, 1.19 and 1.08x at m = 0.25, and less at steep popularity, because the exact path already captures most of the reuse. It covers reordering, moved or re-read tool outputs, and text after an insertion. Changed spans and multi-source requests get exact recompute. Memory and latency are unchanged (128 KiB per token at 8B; 4k tokens load in 10.7 ms over PCIe5).
VALUE: About 1.5x cheaper than plain prefix caching at m ≈ 0.25, but only 1.08–1.25x on top of popularity-ordered prefix caching. Two things still need a real-model run on 2WikiMQA, MuSiQue and agent replays: probe recall and quality on single-source requests. Blending is worth it only where popularity is flat.

IDEA 3
NAME: Per-session TTL switch from return hazard
MECHANISM: The client measures, per session, s (the share of turns that come back after a 5–60 minute gap) and n/P (tokens written per turn divided by the cached prefix). It uses the 1-hour TTL when s > s* = 0.75n/(1.15P). Otherwise it uses the 5-minute TTL with a 1-token keep-alive read sent only while the return probability exceeds 0.08 per window. Prior art is Claude Code's static `promptCacheTtl`/`subagentPromptCacheTtl` (5m or 1h per request type, about v2.1.243). What this adds is choosing the TTL per session from measured s and n/P.
Input-bill ratios:
- Long agent session (100k prefix, 2k tokens per turn, s* = 0.013): 1.15x at s = 0.02 and 1.71x at s = 0.10 against plain 5-minute TTL. It matches a blanket 1-hour TTL there.
- Short-prefix sessions with large writes (s* = 0.33): 1.40–1.52x cheaper than a blanket 1-hour TTL.
On the Mooncake traces the measured rewrite share is f = 0.09–0.11, so the ceiling there is only 1.07–1.10x. It covers no edit cases, only expiry. Output is byte-identical, so there is no quality risk. It runs client-only with zero added latency.
VALUE: 1.0–1.5x on input against the best static TTL choice. The gain is large only for sessions with real 5–60 minute pauses, and nothing on short-gap traffic. This is the smallest honest version: it cannot make edited or reordered context cheaper.

=== NOTES ===
- **Idea 1:** I added second-sighting breakpoint admission and per-regime TTL. New deciding number: the bill ratio is ≥1.0x in every regime, and 1.5x is now reached at Zipf 1.5 from about 100 requests per 5 minutes (was about 1k). Source: `i1_admission.py` / `.out` (my replay; same setup as `eval_g1/c1/pop_order_ttl.py`; Anthropic 1.25/2.0/0.1 multipliers).
- **Idea 2:** The fallback now uses popularity-first order. New deciding number: the largest routed share for 1.5x rises from 0.12 to 0.19, 0.24 and 0.46. Against the stronger popularity-order baseline the gain is only 1.08–1.25x. Source: `i2_fallback.py` / `.out`, with the cost model from `improve_g1/chains.py` and prefill ratios from `improve_g1/i2_order_sim.out`.
- **Idea 3:** Narrowed from "f must be about 0.8" to a per-session switch rule, s* = 0.75n/(1.15P). New deciding number: 1.40–1.52x against a blanket 1-hour TTL for short-prefix sessions, 1.71x against plain 5 minutes at s = 0.10, and a trace ceiling of 1.07–1.10x. Source: `i3_regime.py` / `.out` and `improve_g1/i3_ttl_replay.out`. The Claude Code TTL settings were confirmed by secondary sources only (version 2.1.243, not 2.1.242); I didn't find the official docs. All Idea 3 numbers are input bill only and leave out output tokens.

Everything is in `/home/user/SomeRepository/engine/runs/v6_ctxcache/improve_g2/`: `answers.md`, the three scripts and their `.out` files. Nothing was committed.

Sources:
- [Developers Digest: Claude Code prompt cache TTL controls](https://www.developersdigest.tech/blog/claude-code-prompt-cache-ttl-controls)
- [ProPakistani: Claude reportedly resets your cache](https://propakistani.pk/2026/10/16/claude-reportedly-resets-your-cache-to-charge-you-more/)
- [claudeissues 99808: no way to set prompt cache TTL for subagents](https://claudeissues.com/issue/99808-no-way-to-set-the-prompt-cache-ttl-for-built-in-or-workflow-subagents-subagents)