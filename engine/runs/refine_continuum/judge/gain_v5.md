## Review of the Continuum-5 answer

### What I could and couldn't verify

- **The cited model files don't exist.** `run5.txt`, `model5.py`, `imbal5.txt`, `energy5.txt`, `zeros5.txt` and `calib5.txt` are not in `/home/user/SomeRepository/engine`. There is no `runs/` directory at all. So the waterfall, the τ matrix, the imbalance Monte Carlo and the zero-code fractions are unverifiable claims, not reproducible results. I checked only what can be recomputed from numbers stated in the text.
- **The arithmetic that can be checked holds up:**
  - Expert size: 3 × 7168 × 3072 × 4.5 bits = 37.2 MB. ✓
  - Experts touched: 459 positions over 384 experts with top-6 routing gives 383.7. ✓
  - W-Tier time: 14.7 GB ÷ 768 TB/s = 19.1 µs. ✓
  - Compute stage: 17.9 µs. ✓
  - Effective compute per kW: 17.4 vs 16.5 PF/kW. ✓
  - Users × tok/s/user: consistent with the reported per-chip throughputs after an unstated ~0.87 derate. The derate is near-symmetric: Rubin is reduced 1.17×, Continuum 1.15×. That is a ~2% residual tilt toward Continuum, which is minor.
- **The answer is commendably self-correcting.** Its own re-accounting already turns the old 1.3–1.6× lead into a tie (0.94–1.03×) on its primary metric, tokens per provisioned MW.

### Remaining unfairness in the comparison

1. **Node and calendar credit.** Continuum is given 0.040 pJ/FLOP (N2) against Rubin's 0.050 (N3P). The answer itself says Continuum cannot ship before ~2028, when its rival is Rubin Ultra or Feynman on an equal or newer node. A node advantage against a chip from an earlier calendar year is not an architectural gain. The answer's own sensitivity table puts this at ×0.88. Applied, the home workload moves from **0.94–1.03× to ≈0.83–0.91×**, which is a loss.
2. **Zero-skip parity is assumed, and the answer's own data cuts against it.** Its synthetic weights support only ≤1.07–1.15× from weight zeros. Granting Continuum Rubin's full 1.43× (dense 35 PF → 50 PF) requires activation-zero skipping that nobody has measured on Continuum. With skipping on neither design, the result is 0.89–1.08×. With weight-only skip for Continuum, the answer gives 0.8–0.85×.
3. **Realised fraction of the roofline is assumed equal.** Measured Rubin achieves only 1/3–1/11 of what the model predicts. Continuum is assumed to lose the same fraction, with no evidence either way. The same applies to tile efficiency η = 0.6 on 64-column slices; η = 0.45 means a ~25% loss. Every ratio rests on these assumptions.
4. **The niche wins are small or fragile.**
   - The 1M-context result is 1.12× at ≥1,000 tok/s/user, which is inside the model's error.
   - The 1.41×/2.29× results apply only at ≥1,500/2,000 tok/s/user. They depend on Continuum's own unproven τ ≈ 10 µs.
   - The p = 0.6 gains of 1.20–1.34× shrink to ~1.05–1.18× once the node credit is removed.
5. **The non-Nvidia wins of 1.6–19× are not gains over best practice.**
   - Rubin is the best current practice, and Continuum ties it.
   - The LPX and CS-4 comparisons put SRAM-only parts on a 1.6T-parameter, 128K-context workload the answer itself places outside their domain.
   - "Rubin+LPX" scores below Rubin alone in the model. That is not how Nvidia deploys LPX; it adds LPX to Rubin for latency tiers rather than replacing it.

### What survives

The one gain that follows from the architecture rather than from tuned parameters is the **~2.9× more tokens per HBM stack** (≈2.2× per DRAM GB with 16-high stacks). It comes from weights sitting in SRAM, so HBM holds only KV.

- **It survives the 12-high fallback.** Same stacks as Rubin, still 2.9×.
- **It is unaffected by the node correction**, because it is a per-stack measure, not a per-watt one.
- **It scales down with the η and realised-fraction unknowns:** ~2.2× at η = 0.45.
- **It is a resource swap, not an efficiency gain.** Each package uses ~4,500 mm² of N2+N4 silicon. A 1 GW site needs ~1.4–2.1 months of TSMC's entire SoIC capacity. It pays off only for a buyer for whom HBM is scarcer than SoIC and leading-edge wafers.
- **It comes at tokens per MW of ≈0.85–1.0× Rubin after correction**, so it is a Pareto point, not a "best" chip.
- **It is all model output.** No silicon exists, and the simulation files are not present.

HONEST GAIN: none in tokens per provisioned MW (≈0.85–1.0× Rubin after removing the N2 node credit); only a modelled ~2.9× more tokens per HBM stack (~2.2× per DRAM GB) at 128K and ≥1,000 tok/s/user, traded for SoIC capacity and unverified