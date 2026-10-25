# Review of the Continuum answer

**Bottom line:** once the comparison is made symmetric, the throughput-tier result is a tie or a loss, and the headline interactive lead (2.2–4.4× over Rubin) is not supported. The only gain that survives is a narrow, fragile one at ≥2,000 tok/s/user against Cerebras CS-4.

The supporting files the answer cites (`runs/refine_continuum/round2/model2.py`, `final.txt`, `sens3.py`) do not exist in this repository. So I checked its numbers by redoing the roofline arithmetic from its own stated inputs.

## What holds up

- **Continuum's internal arithmetic is consistent.** At ≥1,000 tok/s/user, 61 microbatches × 233 users × 1,071 tok/s × 0.85, divided by 0.47 MW, gives about 27M tok/s/MW, close to its 28.7M.
- **The component figures check out:**
  - W-Tier: 2.3 GB per tier and 256 TB/s at 307 W.
  - Bonds: about 4.7k per tile at 1.5 Gb/s.
  - SRAM cost: about $120/GB.
- **The ≥200 Rubin figure reproduces.** From the answer's inputs (12.4 GB of weights per GPU, about 380 users per GPU limited by KV capacity, η = 0.6, 8 µs × 61 layers) I get about 28.6M tok/s/MW. The answer reports 28.3M.
- **It is candid about its weaknesses:** the throughput-tier tie, the loss on peak single-stream speed, the τ and W-Tier kill criteria, and the 1.05 W/mm² thermal figure with no claimed advantage.

## What is unfair or unsupported

1. **Unequal τ in the ratio table.** Continuum is scored at 5 µs against Rubin at 8 µs. Both figures are unmeasured projections. With both at 8 µs, the answer's own ratios fall to 1.07×, 1.95× and 3.85× (≥200, ≥800, ≥1,000).

2. **Rubin's interactive numbers do not follow from the stated inputs.** I used the same semi-serial per-layer roofline for both designs, i.e. max(KV, attention compute) + max(weights, FFN compute) + τ. The inputs were the answer's own: 0.565 ms of weight reads per step, 16.2 µs of compute per user-step, 4.7 µs of KV reads, and τ = 8 µs. With these, Rubin is **compute-bound, not weight-bound**, up to about 1,300 tok/s/user.

   | Tier | Rubin, my recomputation | Rubin, as the answer reports |
   |---|---|---|
   | ≥800 | ~24M tok/s/MW | 13.8M |
   | ≥1,000 | ~22.5M tok/s/MW | 6.5M |

   Continuum at 8 µs scores 26.8M and 24.9M, so the ratio is about **1.1×**. If Continuum also gets the semi-serial treatment (attention, then FFN), its 1,000-tier stage grows from about 30 µs to about 40 µs, and it falls to roughly **0.85–1.0×**.

   The answer's energy note mentions "HBM weight re-reads" on the GPU side, which may explain the gap. That mechanism is never justified, and the code is not available to check it. Until it is reconciled, the 2–4× claim is unsupported.

3. **Tile-level expert imbalance is ignored.** Weights sit stationary under each tile, about 1.3 expert-thirds per tile. At the ≥200 tier that is about 22 tokens per tile on average, and the maximum across 288 tiles (Poisson) is about 1.7× the mean. This adds roughly 10 µs to a 52 µs stage, about 15% fewer tokens. GPUs schedule experts dynamically across SMs and only see inter-GPU imbalance, which the shared 0.85 derate already covers. Combined with Rubin-50, the throughput tier becomes **a loss of about 0.8–0.95×**. The interactive tiers stay weight-bound and are largely unaffected.

4. **Smaller points.**
   - Peak power (2.3 kW) exceeds TDP (2.1 kW), but Rubin is also provisioned below its 240 kW rack maximum, so the two roughly cancel.
   - Continuum's speed-floor win comes from using 184 packages per model replica, while GPUs are held to a 72-GPU NVLink domain. That limit is a real 2026 constraint, but it should be stated.

## What survives

At **≥2,000 tok/s/user** no GPU or TPU configuration is viable: weight reads plus 61 × τ exceed the 0.9 ms step budget. The best incumbent is CS-4, at about 1.5M tok/s/MW. I re-derived the Continuum figure at τ = 8 µs:

- each stage has about 6.5 µs left after τ;
- that allows about 34% of experts to be touched;
- which supports about 13 users per microbatch;
- giving **about 2.9M tok/s/MW, or 1.9× CS-4.**

This win is fragile:

| Change | Result vs CS-4 |
|---|---|
| W-Tier at 180 TB/s | 1.3× |
| τ = 10 µs | 1.25× |
| W-Tier at 128 TB/s | 0.87× (a loss) |
| CS-4 dense compute higher than the assumed 25 PF | Erodes the lead |

It also sits beyond Continuum's own throughput cliff. It is a modelled, conditional win in a niche tier, not evidence of being "best in the world."

| Tier | Answer's claim | After correction |
|---|---|---|
| ≥200 | 0.95–1.13× vs Rubin | ~0.8–1.07×, a tie or loss |
| ≥800 | 2.2× | ~0.85–1.1×, a tie |
| ≥1,000 | 4.4× | ~0.85–1.1×, a tie |
| ≥2,000 | 3.1× vs CS-4 | ~1.3–1.9× vs CS-4, conditional |

HONEST GAIN: ~1.9x higher output tok/s per provisioned MW than Cerebras CS-4 at ≥2,000 tok/s/user (modelled only; 1.3x at 180 TB/s W-Tier, gone at 128 TB/s); no supported gain over Rubin at ≤1,000 tok/s/user