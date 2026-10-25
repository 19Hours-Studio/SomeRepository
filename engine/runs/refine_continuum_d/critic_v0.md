The answer's arithmetic is right: all seven round-7 scripts re-run byte-identical. But the 1.17× bulk-tier headline doesn't survive two corrections, and the ≥1,000 tok/s/user gain shrinks from 1.57× to about 1.3–1.4×. Below, "ratio" means Continuum-7's output tok/s per provisioned W divided by Rubin's best at the same per-user speed floor (128K context, p = 0.8, unless stated). The full write-up is in `critique.md` in the critic0 folder; my scripts are in `scripts/`, with outputs in `audit1–4.txt` and `rerun/`.

## 1. Numbers that hold
- **Section 4.2 hand check:** 12.5 µs per microbatch, 1,157 tok/s/user, 52.4 tok/s/W, and the 22.8 vs 18.6 PF/kW split giving 1.17×.
- **Supply and physical numbers:** 1.57M vs 4.04M HBM stacks per GW; 68k SoIC passes per GW; 0.652 GB of KV per user at 128K; 0.4 Tb/s of KV ingress per package; ~580 A and 0.42 W/mm² per C-die; ~47% raw yield on a 750 mm² die.
- **"≥1,000 survives pairs of adverse assumptions" holds.** The worst pair (η 0.5 with W-Tier at 0.30 pJ/bit) gives 1.11. Three at once (same node, η 0.5, double leakage) gives 1.03.

## 2. Unfair or unsupported points

**A. The pipeline model averages every layer, but a pipeline runs at its slowest stage.** This is the biggest correction. The model spreads KV reads and attention/indexer work evenly over all 62 layers. In V4, the 30 CSA layers read 2.76 MB of KV per user against 0.66 MB for the HCA layers. A CSA stage therefore needs 18.7 µs of KV time, not the averaged 11.3 µs. Giving each layer type its own package count:

| Context | Answer | Corrected |
|---|---|---|
| 128K | 1.17 / 1.29 / 1.57 / 1.70 / 2.47 | **1.04 / 1.15 / 1.40 / 1.67 / 2.42** |
| 1M | 1.21 / 1.21 / 1.44 / 2.00 / 3.68 | **1.01 / 1.01 / 1.20 / 1.67 / 3.26** |

Rubin is unaffected, because a GPU runs all layers in sequence.

**B. Only Continuum got trimmed.** Continuum-7 carries 110 W per slot for host, NIC and switch. By my estimate Rubin's slot carries about 420 W of the same, derived as 3,056 W − 2.3 kW chip − conversion. I found no published Vera CPU or ConnectX-9 power figures, so this is an estimate. If a decode-only Rubin build also trimmed 150–250 W:
- ≥200: 1.17 → 1.07–1.00
- ≥1,000: 1.57 → 1.43–1.34

**C. Perfect overlap helps Continuum more than Rubin.** Continuum's operating point balances four resources at once: SRAM 8.6, KV 11.3, compute 12.5 and links 10.8 µs per microbatch. Rubin at bulk is simply compute-bound. If weight work and attention work run in sequence within a microbatch, applied to both systems, the ratios are 0.94 / 1.03 / 1.25 / 1.68 / 2.21. This is a pessimistic bound, and the answer has no sensitivity row for it.

**D. The calibration does not measure decode.** About 89% of the GPU time in `calib7` is prefill (1.26e-4 s of prefill against 1.6e-5 s of decode per output token). So "GPUs realise 0.19 of the model" is mostly a prefill figure. It is also ambiguous by 9×: 0.19 if InferenceX counts input plus output tokens, 1.70 if output only. The glossary calls throughput the "total token output rate", which doesn't settle it. The break-even thresholds in §0.3 (85% / 64% / 40%) therefore have no decode anchor.

**E. Leaving prefill out conflicts with "sites are power-limited".** The answer's own KV-ingress figures (0.65 GB per request, 29k requests/s) imply about 64 fresh prompt tokens per output token. At that ratio the gain across a whole site is about 1.00–1.03. With r fresh prompt tokens per output token:

| r | ≥200 | ≥1,000 | ≥2,000 |
|---|---|---|---|
| 1 | 1.09 | 1.30 | 1.84 |
| 4 | 1.04 | 1.12 | 1.37 |

**F. "Per HBM stack" compares 16-high stacks with 12-high.** Measured per GB of HBM, 3.0 / 4.0 / 9.3× becomes **2.25 / 3.0 / 7.0×**.

**G. Silicon area is understated.** The "1.2× Rubin's logic area" figure leaves out the eight N4 SRAM tiers per package, about 60 cm² each package. Counting them, Continuum uses roughly 4× Rubin's silicon per token.

**H. The cost range pairs like ends.** Crossing the BOM ranges gives 0.76–1.77×; centre to centre is about 1.2×, not 1.1–1.4×.

**Where the answer undersells itself:**
- **Tile imbalance.** It charges Continuum 1.12 against the GPU's 1.07, yet SRAM is 87% empty at g = 6, so hot experts can be replicated. At parity the ratios rise 4–5%, to 1.22 / 1.35 / 1.64 / 1.78 / 2.57.
- **The worst Rubin Ultra case.** The "Ultra at 600 kW plus undervolt" bound (0.75–0.87×) implies 30 PF/kW, 2.3× same-node Rubin's best. That is not physically credible, and the answer could reject it instead of headlining it as a loss. A German report (igorsLAB) that the 4-die Ultra was dropped is unconfirmed.

## 3. Where a larger honest gain is
1. **Packages built per layer type: the main unused lever.** Fix A can be undone by design:
   - HCA-layer packages ship without HBM and keep their KV in the idle SRAM tiers.
   - CSA-layer packages get more HBM bandwidth, or move indexer keys into SRAM.
   - Hot experts are replicated to bring imbalance to parity.

   Combined, this brings Continuum back to 51.9 tok/s/W at 128K (52.4 before) and halves HBM stacks on the HCA stages. Against a trimmed Rubin it gives:
   - 128K: about 1.0–1.06 at ≥200, **1.33–1.42 at ≥1,000** and 2.25–2.40 at ≥2,000;
   - against Rubin Ultra built bottom-up, the fairer comparison by date: 1.02 / 1.13 / 1.27 at ≥200 / ≥1,000 / ≥2,000;
   - 1M context: 0.83 against Ultra at bulk.
2. **Regime.** The gain is largest for agentic decode with high prefix-cache reuse and long outputs (about one fresh prompt token or fewer per output token), at ≥1,000 tok/s/user, and for prose (p ≈ 0.6). There, decode dominates site power and Rubin wastes the most on deep speculation.
3. **Measurement.** The claim needs a decode-only GPU calibration point (decode-pool tok/s per GPU at fixed interactivity), not total 8K/1K throughput.

Bulk speeds are a tie. Every figure is model output with no silicon, and holds only at the decode-pod level; the gain shrinks toward 1 at the site level.

Sources:
- [Tom's Hardware: Vera Rubin NVL72 superlab](https://www.tomshardware.com/tech-industry/artificial-intelligence/behind-the-scenes-at-nvidias-engineering-superlab-vera-rubin-nvl72-running-openai-workloads-800vdc-demonstrated-and-more)
- [HashrateIndex: Vera Rubin NVL72 specs](https://hashrateindex.com/blog/nvidia-vera-rubin-nvl72-specs-breakdown/)
- [CUDO: Vera Rubin](https://www.cudocompute.com/products/nvidia-vera-rubin)
- [Introl: Vera Rubin 600 kW racks](https://introl.com/blog/nvidia-vera-rubin-gpu-600kw-racks-2027)
- [DCD: GTC rack density](https://www.datacenterdynamics.com/en/analysis/nvidia-gtc-jensen-huang-data-center-rack-density/)
- [igorsLAB: four-die Rubin Ultra report](https://www.igorslab.de/nvidia-soll-vier-die-version-von-rubin-ultra-gestrichen-haben-der-angeblich-neue-rueckzieher-ist-allerdings-nicht-ganz-neu/)
- [InferenceX throughput glossary](https://inferencex.semianalysis.com/glossary/throughput)
- [InferenceX about](https://inferencex.semianalysis.com/about)
- [arXiv 2506.05508: disaggregation metrics](https://arxiv.org/pdf/2506.05508)

HONEST GAIN: ~1.3–1.4× Rubin in output tok/s per provisioned W at ≥1,000 tok/s/user (128K, decode pod only, modelled; needs layer-type-specific packages; bulk tier ≈1.0, i.e. a tie; ≈1.1× against bottom-up Rubin Ultra)