# Critic-0 review of Continuum-7 (round 7)

Scripts: `scripts/audit1.py`–`audit4.py`. Outputs: `audit1.txt`–`audit4.txt`. Re-runs of the author's scripts: `rerun/`.
All ratios are C7 / best Rubin, output tok/s per provisioned W, V4-Pro, p = 0.8, tiers ≥200 / ≥500 / ≥1000 / ≥1500 / ≥2000 tok/s/user.

## 1. Reproduction
All seven round-7 scripts re-run byte-identical (`rerun/*.txt` vs `round7/*.txt`). These hand checks hold:
- §4.2: 12.5 µs, 1,157 tok/s/user, 52.4 tok/s/W.
- The 22.8 vs 18.6 PF/kW decomposition gives 1.17.
- Supply per GW: 1.57M vs 4.04M HBM stacks; 68k SoIC passes.
- 0.4 Tb/s of KV ingress per package; 0.652 GB of KV per user at 128K.
- 580 A and 0.42 W/mm².
- The claim that ≥1000 survives every adverse pair: the worst pair (η 0.5 + W-tier 0.30 pJ/bit) gives 1.11. A triple (same node + η 0.5 + leakage ×2) gives 1.03.

## 2. Corrections (the number each one moves)
| # | Issue | Moves | From → to |
|---|---|---|---|
| A | The pipeline model averages KV reads and attention/indexer FLOPs over all 62 layers. A pipeline runs at its slowest stage. CSA stages read 2.76 MB per user (indexer keys) against 0.66 MB for HCA, so a CSA stage takes 18.7 µs of KV time against the averaged 11.3 µs. Fixed by giving each layer type its own g (`audit3`). | 128K | 1.17/1.29/1.57/1.70/2.47 → **1.04/1.15/1.40/1.67/2.42** |
| | | 1M | 1.21/1.21/1.44/2.00/3.68 → **1.01/1.01/1.20/1.67/3.26** |
| B | The trim was asymmetric. C7T's host, NIC and switch power is 110 W per slot. Rubin's slot carries about 420 W of the same (3,056 W slot − 2.3 kW TGP − 14.6% conversion), covering half a Vera CPU, 1.6T CX-9 and NVSwitch. A decode build of Rubin with 150–250 W trimmed: | 128K | ≥200 1.17 → 1.07–1.00; ≥1000 1.57 → 1.43–1.34 |
| C | The four-way perfect overlap (SRAM, KV, compute and link) suits C7, whose operating point balances 8.6/11.3/12.5/10.8 µs, more than Rubin, which is compute-bound at bulk. A two-phase bracket applied to both (`audit2`): | 128K | → 0.94/1.03/1.25/1.68/2.21 (pessimistic bound) |
| D | The calibration is ~89% prefill. In calib7, 1.26e-4 s of prefill against 1.6e-5 s of decode per output token. So "GPUs realise 0.19" measures prefill realisation and says almost nothing about decode. It is also ambiguous by 9× (0.19 if total tokens, 1.70 if output-only; the glossary's "total token output rate" does not settle it). The §0.3 break-even percentages (85/64/40%) therefore have no decode anchor. | §0.3 | unsupported, not a number |
| E | Site-level dilution. "Sites are power-limited" justifies a site metric, but prefill power, which is the same for both, is excluded. The answer's own KV-ingress figure (0.65 GB per request, 29k req/s) implies ~64 fresh prompt tokens per output token. At that ratio the site gain is ≈1.00–1.03. At r = 1 / 4 fresh tokens per output token: 1.09/1.30/1.84 and 1.04/1.12/1.37 (≥200/≥1000/≥2000). | site | see `audit2` |
| F | Per HBM stack compares C7's 16-high stacks with Rubin's 12-high. Per GB of HBM: | ≥200/≥1000/≥2000 | 3.0/4.0/9.3× → **2.25/3.0/7.0×** |
| G | "Logic area 1.2× Rubin" counts only N2. The 8 N4 W-tiers (≈60 cm² per package) add ~24M cm² per GW, so total silicon is ~4× Rubin's per token. N4 is not scarce, but this belongs in the supply table. | supply | disclosure |
| H | The tokens-per-BOM-dollar range of 1.1–1.4× pairs like ends. Crossing the ranges gives 0.76–1.77×; centre to centre gives ~1.2×. | cost | wider |

## 3. Where it undersells itself
- The tile-imbalance penalty is 1.12 against the GPU's 1.07, yet at g = 6 the SRAM is 87% empty, so hot experts can be replicated. At parity (1.07): 1.22/1.35/1.64/1.78/2.57 (+4–5%).
- The "Ultra 600 kW + undervolt" loss (0.75–0.87) stacks the law on a point that already implies 47% better FLOP/W than same-node Rubin. At 0.55 V it gives 30 PF/kW, 2.3× Rubin's best on N3P. That is not physically credible, and the answer could reject this bound rather than headline it as a loss. There is also an unconfirmed report (igorsLAB) that the 4-die Ultra was cut.
- The bracketed design fix in §4 (HBM-less HCA packages plus imbalance parity) fully recovers correction A at 128K (51.9 tok/s/W against 52.4).

## 4. Central estimate after the check (`audit4`: per-layer stages, HBM-less HCA packages, imbalance 1.07, Rubin trimmed 150–250 W)
- **128K:** 0.99–1.06 / 1.10–1.17 / **1.33–1.42** / 1.56–1.67 / 2.25–2.40.
- **1M:** 0.95–1.01 / 0.95–1.01 / 1.13–1.21 / 1.61–1.70 / 3.06–3.27.
- **Against bottom-up Ultra, the calendar-fair comparator** (128K): 1.02/1.02/1.13/1.23/1.27. At 1M: 0.83 at bulk.
- **Status:** all of these are decode-pod figures, before realisation and before prefill dilution.

## 5. Larger honest gain
1. **Layer-type-heterogeneous packages.** HCA-layer packages without HBM keep their KV in the idle W-tier, worth +7% and 50% fewer stacks on those stages. CSA-layer packages get more HBM bandwidth, or have the indexer keys (2.1 MB per user per layer) moved into the W-tier, which is 87% idle. This is the main unused lever.
2. **Regime:** high-prefix-cache agentic decode with long outputs (r ≲ 1) at ≥1000 tok/s/user, and hard p ≈ 0.6 speculation. There, both the decode share and Rubin's speculation waste are large.
3. **Measurement:** a decode-only GPU calibration point (decode-pool tok/s/GPU at fixed interactivity) is what the claim needs, not 8K/1K total throughput.
