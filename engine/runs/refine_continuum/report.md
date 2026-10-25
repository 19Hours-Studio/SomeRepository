# refine_continuum: stepwise improvement of a plain answer, judged afterwards

| version | words | cost |
|---|---|---|
| v0 | 1308 | plain answer |
| v1 | 4011 | $2.61 |
| v2 | 4937 | $2.22 |
| v3 | 5104 | $1.61 |
| v4 | 5625 | $2.28 |

| comparison | newer version won (both orders) | margins | score (+ newer, - older) |
|---|---|---|---|
| v1 vs v0 | 2 of 2 | clearly, clearly | +4 |
| v2 vs v0 | 2 of 2 | clearly, clearly | +4 |
| v3 vs v0 | 2 of 2 | clearly, clearly | +4 |
| v4 vs v0 | 2 of 2 | clearly, clearly | +4 |
| v2 vs v1 | 2 of 2 | clearly, clearly | +4 |
| v3 vs v2 | 2 of 2 | clearly, clearly | +4 |
| v4 vs v3 | 2 of 2 | clearly, clearly | +4 |

## Why (the judge, newer vs older)
- v1 vs v0: newer wins, clearly. Both propose the same physically sensible design, SRAM-resident weights with HBM used only for KV, but B turns it into a fully specified design. Its blocks are derived from stated bases, and its roofline arithmetic is checkable and holds up. It compares against six current designs across speed tiers and context lengths, states its losses honestly, and gives a sensitivity table plus tests with conc
- v1 vs v0 (swapped): newer wins, clearly. A delivers a fully specified architecture with block-level numbers, roofline and energy checks, a six-way quantitative comparison that admits losses, sensitivity thresholds, supply and yield risks, a software story and kill-criteria tests. B shares the core idea (SRAM-stacked weights, HBM only for KV) but presents it as a loose idea list built on an older attention assumption. It also gives thin t
- v2 vs v0: newer wins, clearly. B covers every required dimension with derived, cross-checked numbers: blocks, roofline, power, packaging, numerics, cost and a multi-system tiered comparison. It is explicit about where it ties or loses, and it gives concrete kill criteria and a facts-vs-assumptions split. A has the right core idea and some honest trade-offs, but leaves packaging, power, numerics and the Ironwood comparison thin,
- v2 vs v0 (swapped): newer wins, clearly. A delivers one complete architecture with quantified blocks, roofline checks, comparisons across several tiers against GPU, TPU, LPX and CS-4, and a sensitivity analysis with kill criteria. It also states its losses openly. B has a similar core idea but is split into loose ideas, with thinner coverage of packaging, power, risks and the test plan, so it is less usable as an architecture proposal.
- v3 vs v0: newer wins, clearly. B gives a fully quantified architecture covering power, packaging, yield, cost and thermal limits, and it compares against more competitors under fair assumptions, including GPU speculative decoding. It honestly scales its claim down to a 10–90% lead in a narrow regime and states where it ties or loses. A covers the required elements more thinly and likely overstates its advantage because it leave
- v3 vs v0 (swapped): newer wins, clearly. A compares fairly, re-running every competitor at its own best speculation depth and equal latency, and openly cuts its own claimed lead from 4× to 10–90%. It also gives full ratio tables, sensitivity analysis and kill criteria. B omits speculative decoding and gives GPUs much worse per-layer latency than Continuum, so its "Rubin can't reach this speed" claim is likely an artifact of those assumpt
- v4 vs v0: newer wins, clearly. B covers every element the brief asks for: justified metrics, quantified blocks, roofline checks, comparisons against GPU, TPU and SRAM/wafer-scale designs with wins and losses, supply and yield limits, software, a kill-criteria test plan, and a separation of facts from assumptions. It calibrates its baseline model against measurement and shows how sensitive the result is to the decisive latency a
- v4 vs v0 (swapped): newer wins, clearly. A delivers a complete, internally consistent architecture with quantified blocks, roofline and energy checks, a calibrated comparison against six or more current systems, and explicit win, tie and loss regions. It also includes a sensitivity analysis on its decisive assumption, supply and yield limits, and a concrete falsification table. B covers similar themes only as loosely connected idea sketc
- v2 vs v1: newer wins, clearly. A's headline lead comes from giving Continuum a much lower per-layer latency than the GPUs, omitting MTP, and overstating Cerebras compute, and its claimed thermal advantage ignores the SRAM stack. B corrects all of these, redesigns the chip in response, and honestly reports ties or losses in the throughput tiers with a narrower, defensible win only at high interactivity. A reader acting on B gets
- v2 vs v1 (swapped): newer wins, clearly. A fixes B's main modelling biases: Continuum got 3 µs per layer against 15–40 µs for GPUs, MTP was missing, and CS-4 dense compute was inflated. With those fixed, A reports honestly that Continuum only ties at throughput tiers and wins at high interactivity. That gives a falsifiable, defensible claim instead of B's inflated "1.6× everywhere". A also corrects B's thermal-advantage claim and makes i
- v3 vs v2: newer wins, clearly. Both share the same plausible architecture and rigorous structure, but A's headline 2.2–4.4× interactive lead over Rubin comes from restricting GPUs to MTP-1 speculation and giving Continuum a lower τ. B corrects this with best-k speculation and equal τ for every system, and shows the real lead is about 1.1–1.4×. B also explains the physical reason for that bound and adds a kill test targeting it,
- v3 vs v2 (swapped): newer wins, clearly. Both share the same architecture and structure, but B's headline 4.4× interactive lead rests on limiting GPUs to one draft token and giving Continuum a lower per-layer latency than the GPUs. A removes both biases, quantifies the much smaller real lead (≈1.1–1.4×, a tie against Rubin50), explains the physics behind that bound, and adds the kill test that matters most. Someone acting on A gets an ho
- v4 vs v3: newer wins, clearly. Both share an identical, well-specified architecture. B grounds its decisive assumption, per-layer exposed latency, in measured data and shows a full sensitivity matrix that includes A's equal-τ case. It also fixes the GPU-model calibration that A leaves off by about 7×, quantifies the SoIC supply constraint, and adds a direct kill test on Rubin's latency. A's equal τ = 8 µs looks conservative but
- v4 vs v3 (swapped): newer wins, clearly. A grounds its decisive variable, per-layer exposed latency, in measured figures from Cerebras, LPX and GPUs, shows the full τ sensitivity matrix, and calibrates its GPU model to within ~2× of InferenceX. B leaves a 7× calibration gap unresolved and uses an idealized equal τ. Architecture, risk and software coverage are otherwise nearly identical, so A's better-grounded comparison and sharper kill 
