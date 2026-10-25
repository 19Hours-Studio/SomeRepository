**B is clearly better.** It is the same work as A, corrected. The corrections change what the asker should actually do.

**What I checked**
- I re-ran B's billing replay (`billing2.py`, 200 real SWE-agent traces, about 3.5 minutes). The output was byte-identical to `billing2.out`.
- I read B's splice-quality code (`smol.py`, `spliceq.py`). It is a sound test: the spliced KV cache is scored against a full recompute of the same cleared prompt, on the agent's real next message. It also includes a no-shift control, a numerical-noise floor, and a check that removing and re-inserting the same tokens restores the cache to about 1e-5.
- A web search to confirm SWE-agent's `polling` option found nothing. That point rests on B's own simulation and the docs it cites.

**Where A goes wrong**
- **Strawman baseline.** A's headline, a 45–47% saving, is measured against sliding-window clearing. That policy costs 39.7% more than the append-only prompt the agent actually ran.
- **No real gain over existing practice.** Against append-only, A's "new" horizon rule saves 23.7%. SWE-agent's existing `polling=10` setting already saves 23.2%.
- **Its main tip can backfire.** Anthropic only looks back 20 blocks from a cache breakpoint. With the usual single breakpoint at the end of the prompt, A's horizon rule costs **19% more than append-only** in the re-run figures. A does not mention this.
- **No quality evidence.** A's server-side splice is priced at API rates nobody sells, and its quality is never measured.

**What B gets right**
- **Honest client-side numbers.** B concedes that the client-side gain is mostly prior art: the best batch rule is only about 3.6% cheaper than `polling=10` (0.740 vs 0.768 of append-only cost).
- **The fix that makes clearing pay.** B quantifies the breakpoint problem and gives the fix: four breakpoints (the API maximum), including one after the last placeholder and one at the first edited position. With that, every policy bills within 0.6–1.6% of the ideal.
- **Fair own-stack costing.** The splice is costed in GPU-hours, with the key re-rotation counted. It saves 33–42% against append-only, versus 23–28% for exact clearing.
- **Measured splice quality.** On a real model:
  - KL divergence is 0.006–0.013 nats per token.
  - Top-1 agreement is about 98%.
  - There is no harm to the likelihood of the real next message.
  - The error is about the size of showing one more old output (KL 0.011).
- **The limit, stated.** The test model is tiny: 135M parameters, with contexts of about 1.5k tokens. B says so.

**Weaknesses both share**
- Ideas 3–5 are the same in both, and neither runs a live frontier-model test of task success.
- Under the stated constraints, neither gets near 100% hit rate for reordered documents or changed outputs except through inexact KV reuse.
- B's own-stack figures come from a model, not a measured deployment.

WINNER: B
MARGIN: clearly
WHY: I re-ran B's billing replay and got byte-identical results, and I read its splice-quality harness, which is sound. A's headline saving is measured against a strawman (sliding window, +39.7% over append-only). Its horizon rule only matches SWE-agent's existing `polling=10` (−23.7% vs −23.2%). Under Anthropic's 20-block lookback with one end breakpoint, A's rule costs 19% more than append-only, which A never mentions. B fixes the baseline, supplies the breakpoint placement that makes clearing pay, and adds a real (if small-model) quality measurement of the splice.
REAL GAIN A: none. At best about 3% relative over SWE-agent `polling`, and only with breakpoint placement A doesn't describe; without it, a loss.
REAL GAIN B: Client side, about 3.6% relative over `polling=10` (−26.0% vs −23.2% against append-only), conditional on the four-breakpoint placement. On your own serving stack, the splice adds about 11–14 points (−33% to −42% GPU-hours against append-only), but this is modelled, and its quality is checked only on a 135M model.