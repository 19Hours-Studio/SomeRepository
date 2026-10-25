# Review of the Continuum-6 answer

**Files.** I tried to open the cited run files (`runs/refine_continuum/round6/`, `round5/`), but my shell commands returned no output, so I could not inspect or re-run the model. All checks below are by hand, using the answer's own stated numbers.

## What holds up

- **The hand arithmetic is internally consistent.** I re-derived every figure below and each matches:
  - **Continuum-6 compute time at ≥1,000 tok/s/user.** Positions per microbatch are 268 × 2 = 536. Per-position time is 6.83e-8 s. 536 × 6.83e-8 s ÷ 6 × 1.12 ÷ 0.6 = 11.4 µs.
  - **Speed.** 1.8 accepted tokens ÷ (62 × 22.8 µs) = 1,273 tok/s/user.
  - **Pod efficiency.** 33,232 users × 1,273 × 0.85 ÷ 910 kW = 39.5 tok/s/W.
  - **Rubin efficiency.** 0.85 × 6,630 × 1,045 ÷ 190 kW = 31.0 tok/s/W.
  - **Speculation waste.** At p = 0.8, k = 4 computes 5 positions for 3.36 accepted tokens, a waste of 1.49. k = 1 computes 2 for 1.8, a waste of 1.11.
  - **Capacity.** KV at 128K is roughly 0.6 GB per user. That fits both 33k users in the pod's 54 TB of HBM and 6.6k users in NVL72.
- **The mechanism is physically real.** Per layer, the two machines have about the same weight bandwidth: 1.58 PB/s for NVL72 against 1.54 PB/s for 6 Continuum packages. The difference is how that bandwidth is used:
  - Rubin has to spend the whole rack, about 190 kW, streaming one layer at a time.
  - Continuum keeps each layer resident in SRAM on about 15 kW of packages.
  - Pipelining Rubin across racks does not fix this. Per-layer latency is still set by how fast each GPU's HBM reads that layer.
  - So above about 1,000 tok/s/user, Rubin is forced into deeper speculation and wastes more compute. Below about 500, both machines are compute-bound and the result is a tie. This is the Groq/Cerebras insight applied to a model too large for SRAM-only systems, which is a sound argument.
- **The answer concedes honestly.** It admits a tie at moderate speeds, a likely loss to Rubin Ultra, a GPU model that is 3–11× above measured results, and that η is the decisive unknown.

## Corrections the answer did not fully make

1. **Process node is counted as architecture.** The answer gives Continuum 0.040 pJ/FLOP on N2 against 0.050 for Rubin on N3P.
   - That 20% comes from the newer process, not the design, and Nvidia's next chips will get it too.
   - The answer's own sensitivity table gives the equal-energy result: **1.27 → 1.13 at ≥1,000 tok/s/user**, and the ≤500 "tie" becomes about 0.93–0.96, a mild loss.
   - Scaling the higher tiers by the same 0.89 gives roughly 1.34 at ≥1,500 and 1.70 at ≥2,000.
2. **Zero-skip parity is unsupported.** Rubin's 50 PF is a shipping vendor feature. Continuum's 1.43× front end is not built.
   - If Continuum only gets weight-only zero-skip, the answer itself gives about 1.05 at ≥1,000.
   - Combined with correction 1, that is about 0.94, which is a loss.
3. **η = 0.6 on tiny slices is optimistic.** Each tile processes about 8–9 positions per expert across 32 columns. No evidence is offered for 60% efficiency on matrix multiplies that narrow.
   - At η = 0.5 with equal energy per FLOP, the answer's own figure is about 0.94.
4. **The calendar comparison is unfair.** Continuum ships in 2028 at the earliest, but the headline is against 2026 Rubin.
   - Its real rival is Rubin Ultra, also on N3P.
   - Using Nvidia's own 600 kW figure rather than the less authoritative 820 kW reports, Continuum loses at every 128K tier: 0.68–0.85×.
   - It wins only at 1M context and ≥1,500 tok/s/user: 1.04× and 1.40×.
5. **The HBM-per-stack advantage is not a net supply gain.** The 2.6–4.7× advantage moves the bottleneck to SoIC, which has about a tenth of CoWoS capacity. A single gigawatt would use 1.5–2.3 months of the world's SoIC output.
   - The design also uses more N2 and N4 silicon per token than Rubin.
   - This advantage only counts for a buyer whose specific constraint is HBM.
6. **No realisation evidence exists for Continuum.** The GPU model already overstates measured results by 3–11×. Every ratio assumes Continuum would realise the same fraction of its modelled ceiling, and nothing supports that. Every gain in the answer is therefore modelled, not demonstrated.

## Net result

- **Against shipping Rubin NVL72, after the node correction:** about 1.1× tokens per provisioned MW at ≥1,000 tok/s/user, and about 1.3–1.7× at ≥1,500–2,000.
  - At ≥1,000, the gain disappears under any one of the remaining open assumptions: narrow-tile efficiency, or zero-skip.
  - The ≥1,500–2,000 gains are more robust, because they come from Rubin running near its own speed ceiling. They cover a narrow speed tier.
- **Against Rubin Ultra, its real calendar rival:** a loss at 128K, and a small win only in the 1M-context, ≥1,500 tok/s/user corner.
- **Everything is model output with no realisation evidence.** "Best in the world" is not supported.

HONEST GAIN: ~1.1x tokens per provisioned MW vs Rubin NVL72 at ≥1,000 tok/s/user after equalising process energy (modelled only, within error; none vs Rubin Ultra)