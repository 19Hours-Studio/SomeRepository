# improve_g1 — improved answers (scripts and outputs in this directory)

Files: chains.py / chains.out (Ideas 1 and 2 cost chains), i2_order_sim.py / .out (RAG ordering replay),
i3_ttl_replay.py / .out (TTL replay on Mooncake FAST25 conversation and toolagent traces, in traces/).

IDEA 1 — Probe-routed position-independent KV reuse
- Change: the 1% traffic-level shadow gate is replaced by a per-request route. The layer-1 deviation pass that CacheBlend already runs decides, per request, whether to blend or to take the exact prefix-cache path. Multi-source requests are recomputed exactly instead of being repaired at about 0.53 gap recovery. The claim to help API users is dropped.
- Bill ratio vs prefix caching (Archetype C chain): m=0.1 gives 1.52x, m=0.2 gives 1.43x, m=0.3 gives 1.35x, m=0.5 gives 1.22x. Reaching 1.5x needs m <= 0.12. The old all-blended claim was 1.64x.
- Unverified: the probe's recall on 2WikiMQA/MuSiQue (needs a real model). FACT 18 warns that deviation-style signals can be unreliable.

IDEA 2 — Popularity-first exact-prefix document ordering
- Change: blending is dropped. Documents are sorted by an online retrieval-frequency counter, so every hit is an exact prefix.
- Exact document-token reuse at Zipf 1.05/1.2/1.5: popularity order 0.400/0.546/0.768, hash order 0.152/0.229/0.503, relevance order 0.166/0.249/0.425. A CacheWeaver-like greedy trie gives 0.403/0.548/0.769, the same as the counter.
- API bill (Archetype B): 1.17/1.35/1.78x. Self-hosted (Archetype C): 1.17/1.26/1.43x. Caching documents only pays above u = 0.217.

IDEA 3 — Hazard-gated keep-alive as a TTL guard
- Measured f = 0.114 (conversation trace) and 0.089 (tool-agent trace). The ceiling if every rewrite became a free read is 1.096x and 1.069x.
- The leaf-session return hazard is about 0.002 per 5-minute window, against a break-even of 0.08. So the rule sends no pings and costs 1.00x.
- Fixed keep-alive costs 0.93–0.97x (1 ping) and 0.75–0.83x (3 pings). A blanket 1-hour TTL costs 0.73x, which means the rule is 1.36–1.37x cheaper than it.
