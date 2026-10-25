I'd pick **B**, and by a clear margin. B is a revised version of A: it keeps A's four ideas, fixes their numbers, and tests the main claim on real agent sessions. A's numbers come from a made-up session simulation.

**What I checked**

- **A's script (`calc.py`).** I ran it and it reproduces A's figures. But its headline "−40% billed input, hit rate 92.9% → 99.75%" has three problems:
  - The baseline is a strawman: it rewrites an earlier tool output in place every 5 turns.
  - The "ski-rental compaction" rule, A's contribution on top of append-only, never fires. `erratum` and `erratum+ski` give the same result, 364,600 units.
  - The rewrite cost is charged at 1.25×. The extra cost of a rewrite is really (1.25 − 0.1)× = 1.15×, because those tokens would have been read at 0.1× anyway. B makes this correction, and the break-even turn counts drop slightly.
- **A's document ordering.** A suggests sorting documents by content hash so reordering becomes an exact prefix match. B points out the flaw: adding one document then breaks the cache for about half of the document tokens on average. Ordering by first appearance avoids that.
- **A's "hole-punch deletes."** A presents this as new. It is published prior art: Leyline (arXiv 2606.01065) does span splicing and reports +11.2 points of hit rate. B cites it and narrows its claim to "billing a deletion as a hit."
- **B's replay.** I re-ran `replay.py` on the 63 real SWE-agent trajectories (2,068 API calls). The output is byte-for-byte identical to `replay.out`. `superset.py` also reproduces: at all 4,136 checks, the batch mask hid nothing that SWE-agent's own masking showed.
- **B's token calibration.** B says that with no masking the recorded token counts would need about 4.9 characters per token, with a wide spread. That is why B concludes the recorded traces used SWE-agent's last-5 masking. I checked it independently and got a median of 4.86 (quartiles 3.88 to 6.6), so the claim holds.

**What B finds on real traces**

- SWE-agent's shipped "last-5 observations" masking costs **+58%** compared with plain append-only, because it breaks the cache on every call.
- Delta views plus price-triggered batch masking cost **−30.4%** against append-only. The 95% confidence interval is −26% to −34%, and it is cheaper on all 63 traces.
- The price-based trigger is only 1–4% better than the best fixed threshold chosen in hindsight. B says this itself.
- B explains why a hit rate near 100% doesn't make things much cheaper. Even with every reused token hit, re-reading old tokens is about 64% of the append-only bill (46% of it the growing history). First writes of new content are 41% of the best bill, and caching cannot remove those.

**Limits of both answers**

- Neither answer ran a real model, so every quality claim is untested. B's delta views in particular need an A/B test on SWE-bench, because the model has to follow back-references.
- Both rely on CacheBlend/EPIC (published methods that reuse cached document KV out of order and recompute a fraction of tokens) for reordering and middle insertions of documents that don't repeat. Neither adds anything beyond those papers there.
- B's evidence covers one kind of workload: coding-agent sessions.

WINNER: B
MARGIN: clearly
WHY: I re-ran both answers' code. A's −40% comes from a made-up simulation with a strawman baseline, a rewrite charged at 1.25× instead of 1.15×, and a compaction rule that never fires. Its "new" span-delete idea is already published (Leyline). B's replay of 63 real SWE-agent traces reproduces exactly and its token calibration checks out. It shows −30% for a client-only method that never reuses KV out of its context, finds that the shipped masking costs +58%, and is honest that a hit rate near 100% is not what lowers cost.
REAL GAIN A: none measured. Append-only errata are already known practice (Manus), its ski-rental rule never triggered, and the −40% is against a strawman. Its other ideas are prior art (CacheBlend, EPIC, Leyline, tiered caches).
REAL GAIN B: about −30% (CI −26% to −34%) billed input against append-only prefix caching on real SWE-agent traces, from a client-only method. Most of it comes from delta re-views, about −19%. Its effect on task quality has not been measured.

Sources:
- [Leyline: KV Cache Directives for Agentic Inference (arXiv 2606.01065)](https://arxiv.org/pdf/2606.01065)
- [papers.cool – 2606.01065](https://papers.cool/arxiv/2606.01065)
- [Emergent Mind – 2606.01065](https://www.emergentmind.com/papers/2606.01065)