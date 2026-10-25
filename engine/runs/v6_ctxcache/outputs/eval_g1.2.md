=== GATE ===
IDEA 1: Probe-routed position-independent KV reuse
KILLER | m, the share of requests the probe sends to exact recompute (true multi-source share × recall + single-source share × false-positive rate) | required m ≤ 0.121 for a 1.5x whole bill (my rerun of the idea's own cost model reproduces its 1.52/1.43/1.35/1.22 exactly) | available m ≈ 0.25, range 0.15–0.34 (true multi-hop share is 23–34% in curated test sets QALD-9plus and LC-QuAD2.0, per arXiv 2607.14561; 42% of MultiHop-RAG queries need two pieces of evidence, arXiv 2401.15391; the only real-log proxy, multi-click queries, is 6.5–11.4% of web queries, Kravi et al.; my assumption of probe recall 0.9 and false-positive rate 0.05 turns a true share of 0.114 into m = 0.147; agent traffic that reasons across several tool outputs is probably higher still; no source measures the multi-hop share of production traffic) | MARGIN 0.48
CHAIN | exact prefix caching plus prefix-aware routing plus LMCache/HiCache offload, self-hosted, cost model 45% fixed + 55% prefill | now 1.00 of the whole bill | with idea 0.72 at m = 0.25 (0.66 at m = 0.10; ceiling 0.62 even at m = 0, because the 45% fixed share caps any prefill-only idea at 2.2x) | RATIO 1.39
VERDICT | WOUNDED | The cost model holds up, but 1.5x needs ≤12% of requests routed away, and realistic multi-source shares plus probe errors put m near 25%; probe recall is unmeasured (2606.17107 says deviation signals are unreliable) and needs a real-model run on 2WikiMQA, MuSiQue and agent replays.
NEW FACT | The share of multi-hop questions in curated question-answering test sets is 22.8% (QALD-9plus) and 34.0% (LC-QuAD2.0); 42% of MultiHop-RAG queries need two pieces of evidence | https://arxiv.org/pdf/2607.14561 ; https://arxiv.org/pdf/2401.15391
NEW FACT | Multi-click queries, a loose proxy for complex needs, are 6.5% of sessions and 11.4% of unique queries in a commercial web-search log | https://ekravi.cswp.cs.technion.ac.il/wp-content/uploads/sites/21/2017/02/p1423-kravi.pdf

IDEA 2: SLO-gated canonical chunk blending
KILLER | fallback share m once the idea's own "0.42 vs 0.83 compute" claim is turned into a whole bill (45% fixed + 55% prefill, plus the 1% shadow recompute) | required m ≤ 0.127 for 1.5x | available m = 0.30 by the idea's own stated scenario (and multi-hop shares of 23–34% in test sets, arXiv 2607.14561); canonical ordering alone gives only 15–50% exact reuse (FACT 5), so most traffic still rests on the blend path | MARGIN 0.42
CHAIN | exact prefix caching plus routing plus offload, self-hosted or provider-side (per-chunk KV needs server access, so this does not apply to a plain API user) | now 1.00 of the whole bill | with idea 0.73 at m = 0.30 (the claimed 0.42/0.83 = 1.98x applies to prefill only and becomes 1.36x over the whole bill) | RATIO 1.36
VERDICT | WOUNDED | It is the same economics as Idea 1 but routes by query and document class, not per request, so multi-hop requests inside a "passing" class still get blended; it misses 1.5x unless fallback stays ≤13%.

I checked the arithmetic against both ideas' own numbers and it matches. The script is `gate.py` in this run folder. No share of multi-hop requests in production traffic was found in any source.

Sources:
- [MARS, arXiv 2607.14561](https://arxiv.org/pdf/2607.14561)
- [MultiHop-RAG, arXiv 2401.15391](https://arxiv.org/pdf/2401.15391)
- [Kravi et al., One Query, Many Clicks](https://ekravi.cswp.cs.technion.ac.il/wp-content/uploads/sites/21/2017/02/p1423-kravi.pdf)