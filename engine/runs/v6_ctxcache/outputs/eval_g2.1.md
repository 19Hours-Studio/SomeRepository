Three ideas are DEAD and one is WOUNDED. None of the four gets near a 100% hit rate.

**How I measured.** I replayed a RAG workload against Anthropic's cache pricing. Setup: 100k-chunk corpus, top-5 retrieval drawn from a Zipf distribution, random arrivals, 1.25x writes, 0.1x reads, and 2x for 1-hour writes. I first checked the replay on a case with a known answer: with no reuse it gives exactly 0.853 for always-write and 1.000 for second-sighting.

All ratios below are for the **whole request**, compared with ledger B's best practice (documents sent uncached, $0.0174 per request). The ideas quote input-only ratios, so their numbers look higher. The replay gives the ideas oracle popularity ranks, which is optimistic for them. Idea 2 is checked by arithmetic against the Mooncake replay facts (FACT 20/23). No real model could be run here, so quality is not measured.

=== GATE ===
IDEA 1: Reuse-gated single-breakpoint document ordering
KILLER | gate uses each document's own reuse probability, but a hit needs the whole prefix path (all earlier documents) to repeat | required per-request ratio 1.5 (its own claim at Zipf 1.2) | available 1.09–1.23 at Zipf 1.2, 1.05–1.12 at Zipf 1.05, 1.20–1.50 at Zipf 1.5 for 10–1,000 requests per 5 min; document-token hit 0.13–0.63 (gate_sim.py replay) | MARGIN 0.77
CHAIN | documents uncached after a cached system prompt (ledger B) | now $0.0174/request | with idea $0.0141–0.0160/request at Zipf 1.2 | RATIO 1.16
VERDICT | WOUNDED | It never loses money, but with only one breakpoint it misses shallower shared prefixes: at ≥100 requests per 5 min it does no better than (often worse than) a plain four-breakpoint always-write, and it falls short of its claimed 1.33/1.50/1.9x everywhere (by about 1.5x at its own claimed Zipf 1.2 point).
NEW FACT | Several third-party guides say Anthropic's cache has been isolated per workspace rather than per organization since 5 Feb 2026, so a cached prefix is shared only within one workspace (not confirmed in official docs) | [evomap.ai](https://evomap.ai/pt/blog/prompt-caching-is-not-agent-memory), [levanteapp.com](https://www.levanteapp.com/blog/prompt-caching-explicado), [agentmarketcap.ai](https://agentmarketcap.ai/blog/2026/04/06/prompt-caching-economics-2026-anthropic-google-agent-cost)

IDEA 2: Per-session TTL switch from return hazard
KILLER | share of input tokens that cache expiry forces you to rewrite (the most any TTL choice can recover) | required about 1.5x input gain over the best static TTL | available 8.0% (conversation) and 4.2% (tool agent) of input, which caps the gain at 1.08–1.11x over a plain 5-minute TTL and less over the best static choice (FACT 20/23, Mooncake FAST25 replay; the s* = 0.75n/(1.15P) arithmetic checks out) | MARGIN 0.07
CHAIN | static 1-hour TTL for agents and 5-minute TTL elsewhere, the settings Claude Code already ships | now 1.0 (input bill) | with idea about 0.95–1.0 on trace-like traffic; 1.40–1.52x only for short-prefix sessions, whose bills are small | RATIO 1.05
VERDICT | DEAD | The arithmetic is correct and the output is byte-identical, but the idea only covers expiry, and on real traces that recovers about 1.1x at most.

IDEA 3: Popularity order with second-sighting cache writes
KILLER | document-token hit rate against the near-100% target | required ≈0.95 | available 0.21–0.66 (0.35–0.45 at Zipf 1.2) across 10–1,000 requests per 5 min (gate_sim.py replay; matches FACT 5's 15–50% exact-prefix ceiling) | MARGIN 0.40
CHAIN | documents uncached after a cached system prompt (ledger B) | now $0.0174/request | with idea $0.0154 (Zipf 1.05, 10/5 min) to $0.0105 (Zipf 1.5, 1k/5 min); $0.0128–0.0140 at Zipf 1.2 | RATIO 1.36 (range 1.13–1.66)
VERDICT | WOUNDED | It is the best of the four: it never loses money, reaches 1.5x or more only at Zipf 1.5 and ≥100 requests per 5 min, beats always-write by 0.1–0.3x, and the 1-hour TTL at low traffic adds 0.07–0.17x; but most document tokens still miss and it covers reordering only.
NEW FACT | Replay with whole-request costs: always writing at 4 breakpoints gives 0.93–1.58x, so it loses money at 10 requests per 5 min with Zipf 1.05; second-sighting with the 5-minute TTL only gives 1.05–1.66x | gate_sim_out.txt (this directory)

IDEA 4: Shared-prefix hazard keep-alive
KILLER | cost of pings compared with the extra hits they buy | required savings ≥ ping spend | available: pinging every qualifying depth costs 379–1,257 units per request but saves only about 150–450 units per request (from +0.06 to +0.08 of document hit). Pinging leaves only, as the idea says, finds zero leaf paths with arrival rate ≥0.083 per window at 10–100 requests per 5 min below Zipf 1.5, and loses 0.03–0.09x where it does ping (gate_sim.py / gate_sim_leaf.py, oracle path rates) | MARGIN 0.4
CHAIN | popularity order with always-write, or idea 3 | now 0.93–1.58x (always-write) and 1.13–1.66x (idea 3) against uncached | with idea 0.92–1.36x (every depth) and 0.93–1.48x (leaves) | RATIO 0.90
VERDICT | DEAD | The rule P × 1.25 > 0.1 ignores that a ping is paid every window on the whole prefix, system prompt included, and that pings on the same branch overlap; at low traffic, where it is meant to help, almost no leaf path qualifies.
NEW FACT | In a low-traffic organisation, a 5-document leaf path essentially never reaches 0.08 hit probability per 5-minute window (at 10–100 requests per 5 min, Zipf ≤ 1.2, 100k chunks), so leaf keep-alive does nothing | gate_sim_leaf_out.txt (this directory)

Everything is in `/home/user/SomeRepository/engine/runs/v6_ctxcache/eval_g2/c1/`: the scripts are `gate_sim.py` and `gate_sim_leaf.py`, their outputs are `gate_sim_out.txt` and `gate_sim_leaf_out.txt`, and the summary is `gate_notes.md`. Nothing is committed.

Sources:
- [evomap.ai – Prompt Caching Is Not Agent Memory](https://evomap.ai/pt/blog/prompt-caching-is-not-agent-memory)
- [levanteapp.com – prompt caching explicado](https://www.levanteapp.com/blog/prompt-caching-explicado)
- [agentmarketcap.ai – Prompt Caching Economics 2026](https://agentmarketcap.ai/blog/2026/04/06/prompt-caching-economics-2026-anthropic-google-agent-cost)