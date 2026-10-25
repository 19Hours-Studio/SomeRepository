# Gain check for answer.md (round2)

Reproduced: `round2/sim3.py` matches `sim3.out` exactly (sanity block). Extra runs: scratch script chk.py.

| Claim | Against the best current practice | Verdict |
|---|---|---|
| ~100% hit rate on re-sent tokens | append_full (append-only, the current practice) already scores 1.0000 in the answer's own sim | no gain |
| Errata −35.8% | measured against in-place editing, which is not best practice | baseline is a strawman |
| Errata −11% vs append_full | all from diff size: 2,000-token diff → +0.0%; against a 300/500-token snippet baseline → −0.7% / −2.0% | 0 to −11%, typically a few % |
| Batching −31.7% to −57.9% | parallel tool use is a default provider feature; W&D already measured −35.9%; the gain depends on an extra batching share nobody measured; with the baseline at 50% / 70% pairs, all-pairs gives −26% / −20% | prior art; size unknown |
| TTL policy −16% to −54% | measured against "let it expire"; picking 1h TTL is the obvious practice; keep-alive beats always-1h only at 15 min / 5% idle (+11.1% vs +19.5%, ≈ −7%) | small |
| Span ops −17% to −55% | only at shallow compaction; against deep clearing (cheapest) +4.6% / −1.0%; approximate KV, quality untested; provider-only | ≈0 at cost-optimal retention |
| Segment cache | CacheBlend/EPIC etc., numbers from papers | prior art |

No output-quality number was measured for any idea.
