# Review of "Continuum" (round 3)

## What checks out

The answer's internal arithmetic holds up when re-derived:

| Check | Answer | Recomputed | Verdict |
|---|---|---|---|
| W-Tier capacity | 2.3 GB per tier | 750 mm² × 24.7 Mb/mm² = 18.5 Gb ≈ 2.3 GB | ✓ |
| W-Tier bandwidth | 256 TB/s | 288 tiles × 4.7k bonds × 1.5 Gb/s ≈ 254 TB/s | ✓ |
| Bond area | ~0.4 mm² per tile | 4.7k × (9 µm)² ≈ 0.38 mm² | ✓ |
| Stage compute (≥200 tier) | ~51 µs | Linear 30.5 µs (FP4) + attention 20.8 µs (FP8) at η = 0.6 | ✓ |
| Throughput (≥200 tier) | 485 tok/s/user, 73.7k tok/s/pkg, 30.1M tok/s/MW | 3.66 ms per step × 1.8 accepted; 33.4k × 485 / 187 × 0.85 | ✓ |
| KV residency | ~115 GB per package | 33.4k users × 0.65 GB / 187 | ✓ |
| Rubin KV fit | 23,455 users | ~15 TB KV + 0.9 TB weights over ~85 GPUs ≈ 190 GB/GPU < 288 GB | ✓ |
| Die yield | ~47% raw | e^(−0.75) at 750 mm², D0 = 0.1/cm² | ✓ |
| HBM | 144 GB, ~10 TB/s | 4 × 36 GB 12-high stacks at ~2.5 TB/s each | ✓ |

The answer is also honest about the round-2 artifact (MTP-1 only), reports Rubin50 as an upper bound, and publishes kill criteria. The remaining problems are inputs that tilt toward Continuum. They are not arithmetic errors.

## Unfair or unsupported items in its own comparison

1. **Slot power overhead is asymmetric. This is the largest correction.**
   - Continuum is provisioned at 2.45 kW against a 2.1 kW TDP and ~2.3 kW peak. That leaves only 0.15–0.35 kW for hosts, the switched plane, power conversion and cooling.
   - Rubin's slot is 3.06 kW against a ~1.8–2.3 kW GPU, so its overhead is ~0.75–1.25 kW.
   - Some saving is real, because a point-to-point mesh needs fewer switches. But Continuum still needs:
     - host CPUs, since the answer relies on host-memory prefix caching;
     - front-end NICs;
     - the spare-remap switch plane;
     - ~6–8% power-conversion loss.
   - A defensible slot is about 2.7–2.8 kW. That multiplies Continuum's tok/MW by **~0.88–0.91**. The answer's own sensitivity row (3.0 kW gives 0.88–1.03 against Rubin35) points the same way.
   - The same asymmetry sits in the energy table: 450 W static for Continuum against 1 kW for Rubin.

2. **Spares are powered but not counted.** Throughput is computed per active package (187), but the pod provisions 192, i.e. 470 kW. Correction: **×0.974**.

3. **The intra-package NoC is unmodeled.** Each expert is sliced across all 288 tiles. The down-projection therefore needs either:
   - a cross-tile reduce-scatter of ~15 MB per tile per stage, which is ~4 GB of on-die traffic per ~51 µs, or
   - an equivalent all-gather of intermediates.

   That costs plausibly 100–350 W or a lower η, and none of it appears in the 2.3 kW budget. GPUs pay their equivalent inside measured kernel efficiency. Correction: **~×0.92–0.96**.

4. **The p = 0.6 wins assume chain-only drafting for the GPU.** The GPU baseline is restricted to geometric chains (k = 0–7). Tree drafting (EAGLE/DFlash-style) is standard practice and is exactly what a FLOP-rich, weight-bound GPU uses at low acceptance. So the 1.24–1.40× (128K) and 1.6–1.9× (1M) prose wins are upper bounds. The 4.8× cell at ≥1,500 tok/s/user is a ratio between two collapsing systems and is meaningless.

5. **Choice of baseline.** "Best current practice" is Rubin, somewhere between 35 PF dense and 50 PF effective. Against Rubin50 the answer already loses at most tiers. MI455X, TPU, LPX and CS-4 serving a 1.6T model are not the frontier for this workload, so the 1.3–18× ratios against them do not establish a lead over best practice.

6. **The cost comparison is apples to oranges.** It sets Continuum's full BOM against "Rubin's 8 HBM stacks alone". The answer still concludes cost is not decisive, so this does not change the result.

## Corrected primary metric (output tok/s per provisioned MW, against Rubin)

The combined correction is ≈ 0.90 × 0.974 × 0.94 ≈ **0.82** (range ~0.78–0.85).

| Regime | Answer (Rubin35 / Rubin50) | Corrected |
|---|---|---|
| 128K, p = 0.8, ≥200 | 1.07 / 0.90 | **0.88 / 0.74** (loses) |
| 128K, p = 0.8, ≥1,000 | 1.19 / 0.99 | **0.98 / 0.81** (tie to loses) |
| 128K, p = 0.6, ≥1,000 | 1.40 / 1.24 | 1.15 / 1.02 before tree drafts; ~tie after |
| 1M, p = 0.8, ≥1,000 | 1.26 / 1.20 | 1.03 / 0.98 (tie) |
| 1M, p = 0.6, ≥1,000 | 1.93 / 1.89 | ~1.5 before tree drafts; likely 1.2–1.4 after (niche) |
| 8K | 1.11 / 0.84 | 0.91 / 0.69 (loses) |
| Prefill | 1.14 / 0.90 | 0.93 / 0.74 (loses) |

The corrected values sit inside the answer's own kill zone: its §7 says any one assumption slipping makes it "just another inference chip".

## What survives

- **Tokens per HBM stack: ~1.35–1.8× Rubin (model output).** Power overhead does not affect this metric, and the spare correction only trims it slightly. It is a real resource advantage while HBM4 is supply-bound. The cost is moving the scarcity to SoIC hybrid-bond capacity, which TSMC does not publish. It is also a secondary metric.
- **A possible niche lead: 1M context, low draft acceptance, ≥1,000 tok/s/user.** This is perhaps 1.2–1.5× tok/MW, but it is unvalidated and vulnerable to tree speculation.

On the answer's primary metric, at its headline operating point (128K, interactive), there is no supported gain over a fairly provisioned Rubin. The design is a plausible, honestly documented research proposal, not a demonstrated improvement.

HONEST GAIN: none in output tok/s per provisioned MW vs Rubin at 128K (≈0.8–1.0x after correcting slot power, spares and NoC); only a modeled ~1.4–1.8x more output tokens per HBM stack