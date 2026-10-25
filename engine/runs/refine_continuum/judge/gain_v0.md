# Review of the "Continuum" answer

I tried to read the answer's working files (`runs/vs_continuum/baseline/DESIGN.md`, `roofline.py`, `results.txt`, `sensitivity.txt`). Every shell call came back empty, including `echo`, so I could not inspect or rerun its model. The checks below redo its arithmetic from the numbers printed in the answer. The models I couldn't reach may change some details.

## What holds up

- **Weight size.** 671B parameters × 4.5 bits = 377 GB. Correct.
- **MLA KV size.** (512 + 64) values × 61 layers × 4.5 bits = 19.8 KB per token, or 2.6 GB per user at 128K. Correct.
- **Attention cost.** About 17 MFLOP per context token, so about 860 FLOP/B. Correct. Attention energy is about 56 mJ (compute) plus 21 mJ (KV read) at 32K. Consistent with its stated pJ assumptions.
- **SRAM power.** 128 TB/s × 0.3 pJ/bit ≈ 310 W. Plausible.
- **HBM4 configuration.** 6 stacks, 15 TB/s, 216 GB. Plausible.
- **Self-assessment.** It already admits no lead in training, about 1.08× at 128K, and a ~2× loss per silicon area at ≤100 tok/s/user. These admissions are honest.

## What is wrong or unfair

**1. The two "different" efficiency metrics are the same unit.**
1 tok/J equals 1,000 tok/s per kW. The answer reports 7.75 tok/J but 6,200 tok/s/kW for Continuum, and 6.5 tok/J but 4,227 tok/s/kW for Rubin. One figure must be modeled energy and the other nameplate power. The "1.5× per kW" claim therefore comes from comparing a guessed Continuum package power (~2.25 kW) against an uncertain Rubin TDP (1.8–2.3 kW). The modeled-energy figure, about 1.2×, is the only one with a stated basis.

**2. The SRAM capacity is overstated by about 1.5×.**
Two base dies under each ~800 mm² compute die give about 1,600 mm² of SRAM die per package. At 0.021 µm² per bit:
- At 100% array efficiency that is about 9.5 GB.
- At a realistic 60–70% array efficiency it is about 6 GB.

So 64 packages hold about 380–420 GB. That does not fit 377 GB of weights plus activations, buffers and expert-imbalance headroom. About 96 packages are needed. Four HBM stacks per package would keep the 13.8 TB of KV capacity and 384 stacks. However, it means 192 N2 dies instead of 128, plus the extra static power and CoWoS area that come with them.

**3. SRAM-resident weights are not where the gain comes from. Per-layer latency is.**
At 200 tok/s/user, a Rubin NVL72 reads its weight shard in about 0.24 ms per step: 5.2 GB per GPU at 22 TB/s. That is out of a 5 ms step budget, so moving weights off HBM saves very little.

The real gap is the fixed latency the model charges per layer:

| | Per-layer latency | Total over 61 layers | Step budget left |
|---|---|---|---|
| Rubin (optimistic case) | 25 µs | 1.5 ms | 3.5 ms |
| Continuum | 6 µs | 0.37 ms | 4.63 ms |

That ratio, about 1.3×, is roughly the claimed advantage. These two latencies have different standing:
- **Continuum's 6 µs is a target.** It is better than the ~10 µs the answer itself infers for Cerebras's on-wafer fabric, yet it is to be achieved over a switched multi-package copper fabric.
- **The GPU's 100 µs is calibrated** to throughput-tuned InferenceMAX configurations and to inter-node DeepEP over InfiniBand, not to NVLink inside a rack.

**4. "Rubin with today's software cannot reach 200 tok/s/user" is contradicted by public results.**
Nvidia reported more than 250 tok/s/user on DeepSeek-R1 (671B) on a DGX B200 in 2025, using MTP/speculative decoding. Neither side's model includes speculative decoding. It helps the latency-bound chip most, because it amortizes the fixed per-layer cost over about 1.7–2 tokens. With it, Rubin's latency share shrinks and the step-budget advantage falls from about 1.3× to about 1.15×.

**5. The ≥1,000 tok/s/user comparison is made against the wrong baseline.**
- Groq is evaluated as an all-SRAM system of about 2,300 chips, with a per-chip power the answer itself calls a guess.
- Current best practice for that regime is reported to be Rubin plus Groq 3 LPX in a disaggregated setup: KV and attention on Rubin's HBM, expert weights on LPU SRAM. That is essentially Continuum's own idea, and the answer gives no number against it.
- The claimed 3–5× lead also depends on the unproven 6 µs fabric. At 12 µs the answer's own figure drops to 1,785 tok/s/kW. At 20 µs it cannot reach the target at all.
- No supported gain remains in this regime.

**6. The thermal and power-delivery risk is understated.**
Each N2 die draws about 1 kW, roughly 1,400 A at about 0.7 V, and that current must pass through hybrid-bonded SRAM base dies. The 9800X3D precedent is a roughly 120 W part. The answer lists IR drop as a risk, but nothing in its numbers accounts for it.

## Corrected gain

Take the answer's best case: modeled tok/J at ≥200 tok/s/user and 32K context, against an optimistic Rubin.

1. Start from the claimed 1.2×.
2. Speculative decoding on the GPU side narrows the latency advantage to about 1.1–1.15×.
3. About 1.5× more packages to actually hold the weights adds static power and cuts a few more percent.
4. The Rubin TDP range alone moves this result by about ±12%.

The result is about 1.1× in modeled tokens per joule. That is unverified and roughly within the model's own error. At 128K context the gain is about 1.0×. No supported gain remains at ≥1,000 tok/s/user, in training, or per silicon area. The HBM-stacks-per-token advantage could partly survive, because KV capacity can be re-provisioned. However, it too is mainly the latency assumption restated. The decisive test is still the one the answer names: measured fabric latency per layer.

HONEST GAIN: ~1.1x tokens per joule at ≥200 tok/s/user and 32K context (modeled only, within error; ≈1.0x at 128K)