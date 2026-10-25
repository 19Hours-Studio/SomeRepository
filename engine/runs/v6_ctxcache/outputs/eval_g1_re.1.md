I've finished all six estimates and written them to `RESULT.md` in the run directory. One margin was computed inconsistently and is corrected below.

=== RECHECK ===
IDEA 1: input-cost cut needed for a 2.4x lower bill | required 2.84x input cut (output is 10% of the bill and untouchable: (1/2.4−0.1)/0.9; this needs 31–37% of turns to be 100k mid-edits; I re-derived the 6.11x and 1.022x multipliers) | available 1.08–1.11x input cut, which is 1.07–1.10x on the whole bill (keep-alive ceiling from the Mooncake FAST25 traces, FACT 20; no source gives the share of edited turns) | MARGIN 0.46

IDEA 2: document-token reuse per request for a 1.5x lower bill | required 0.507 (from 1.25−1.15u = 1/1.5, treating the whole prompt as documents; about 0.62 on the idea's own haircut curve) | available 0.629 at Zipf 1.2 (my simulation, `calc.py`, with an infinite cache and no TTL, so it is a ceiling; the idea's TTL- and breakpoint-limited figure is 0.546; the Zipf exponents are assumed, not measured, since LazyAttention assumes 1.1/1.5/2.1 and RAGPulse gives no fitted value) | MARGIN 1.24 (0.87 on the idea's own effective reuse; 0.94 at Zipf 1.05)

IDEA 3: share of requests the gate must accept as blended | required 0.97 at a canonical hit share of 0.325 (0.81 at 0.15; at 0.5 it is impossible, with a maximum of 1.35x; even 100% accepted gives only 1.53x) | available about 0.9, assuming 10% are gated out. That figure is assumed: I found no measured multi-source share for production traffic, and MultiHop-RAG (arXiv 2401.15391) is a synthetic benchmark. | MARGIN 0.93

IDEA 4: probability that a session idle for 5 minutes returns in the next window | required 0.08 (0.1/1.25; 0.087 on the strict break-even) | available 0.0018 for conversation and 0.0017 for tool agent, from a request-level replay of the Mooncake traces (`hazard2.py`). At block level, which includes partial-prefix reuse, it is 0.087–0.096, which is only at break-even, so the net gain is about zero. | MARGIN 0.02 (token level about 1.0–1.1 gross, no net gain)

IDEA 5: share m of requests routed to exact recompute | required m ≤ 0.046 for 1.5x (my whole-bill arithmetic: 45/55 split, blended path 0.242, exact path 0.83+0.031, 1% shadow check). The idea says 0.12; I get 1.456x at m = 0.1 and a ceiling of 1.54x at m = 0. | available about 0.1 at best. That is the idea's own assumption, and there is no measured multi-source share, probe recall or false-positive rate. | MARGIN 0.46 (0.23 at m = 0.2)

IDEA 6: fallback share m, as a whole bill | required m ≤ 0.049 for 1.5x. The idea's claim of 0.42 vs 0.83 compute (1.98x) becomes 1.31x on the whole bill at m = 0.3, with a ceiling of 1.54x at m = 0. | available m = 0.30, the idea's own unmeasured assumption | MARGIN 0.16

I made one wrong call in `RESULT.md`: it lists Idea 5's margin as 0.46 using m = 0.1, but I labeled it with the idea's own m rather than a measured one. The 0.46 stands only as an optimistic reading.

Files are in `/home/user/SomeRepository/engine/runs/v6_ctxcache/eval_g1_re/r1/`:
- `RESULT.md`
- `calc.py`
- `hazard.py`
- `hazard2.py`
- `data/`, which holds the downloaded traces