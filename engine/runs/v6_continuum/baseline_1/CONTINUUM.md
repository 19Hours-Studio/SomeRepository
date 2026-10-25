# Continuum — design note (baseline_1)

Scripts: `roofline.py` (constants, MoE/KV model), `variants.py` (memory-mix sensitivity, `variants_out.txt`),
`final.py` (5-chip × 3 attention types × 2 contexts × 3 SLOs, `final_out.txt`).

## Target and metrics
- Workload: data-center **decode** of frontier sparse-MoE LLMs (1T total / 32B active, Kimi-K2/DeepSeek-class),
  8K–128K context, GQA, MLA and DSA (sparse) attention. Prefill and training are secondary (see Idea 3).
- Metrics: (1) tokens/s per kW of TDP **at a per-user SLO** (100 / 400 / 1000 tok/s/user), which stands in for cost per token,
  since power and capex scale together; (2) tokens per joule (energy model); (3) maximum tok/s/user.
  Peak FLOPS is not a metric. Serving revenue is set by throughput at an interactivity SLO, and opex by joules.

## Package (all EST unless marked FACT)
| block | spec |
|---|---|
| Compute | 4 × ~400 mm² logic chiplets, N2-class (N3P fallback). Dense FP4 40 PF, FP8 20 PF, BF16 10 PF per package |
| Tier-0 SRAM | ~0.25 GB distributed (tiles, KV block buffers, expert staging) |
| Tier-1 stacked DRAM | 4-high custom DRAM per chiplet, die-to-wafer hybrid bonded (SoIC-class, ≤9 µm pitch), logic on top. 10 GB/layer → 160 GB per package, 16 TB/s per chiplet → 64 TB/s per package, ~0.8 pJ/bit (arXiv 2604.08044 gives 0.66–0.88) |
| HBM | none in the decode SKU (variant sweep: HBM tier lowers tok/s/kW, because its 10 TB/s sets the per-step sweep time) |
| Scale-up | 3.6 TB/s per package (NVLink-6-class), copper 72-package rack; target all-to-all ≤3 µs (1.5 µs stretch) |
| Power | ~2.0 kW TDP; ~1.25 W/mm² of logic; liquid cooled |
| Interposer | ~3 reticles of CoWoS-L (no HBM sites) |

Sanity checks: stacked-DRAM power is 64 TB/s × 8 × 0.8 pJ = 410 W. FP8 at peak is 20 PF × 0.08 pJ = 1.6 kW, so the package
cannot run the memory and FP8 at full rate together. Decode is memory-limited, prefill is compute-limited, and DVFS
shares the 2 kW between them. Ridge = 20 PF / 64 TB/s = 312 FLOP/B. MLA absorbed decode needs ~430 FLOP/B
(compute-bound here), and GQA needs ~28 FLOP/B (memory-bound everywhere).
Bond count: 64 TB/s at 2 Gb/s per bond = 256k signal bonds, ~21 mm² at 9 µm pitch, so bonding does not limit bandwidth.
DRAM bank parallelism does (~10× HBM's banks per Gb).

## Results (final_out.txt; Continuum ÷ Rubin, tok/s per kW-TDP at SLO 100/400/1000)
- GQA 8K: 2.2 / 2.6 / 2.6×. GQA 128K: 2.2 / 2.6 / 2.7×. tok/J 2.3–2.5×.
- MLA dense 8K: 1.08 / 1.15 / 1.14×. 128K: 1.25 / 1.29 / 1.13×. tok/J 1.3–1.4×.
- DSA 128K: 1.8 / 1.9 / 2.7×. tok/J 1.8×.
- vs Ironwood: 2.8–3.8× (GQA 128K). vs WSE-3: 13–18×. vs Groq LP30: 4–6× (LP30 bandwidth and power are EST).
- Loses on: max tok/s/user. Continuum ≈ Rubin ≈ 2.8k, set by 120 all-to-alls × 3 µs. The SRAM/LPU model reaches ~8k,
  and measured Cerebras reaches 2.2k on gpt-oss-120B. It also loses on capacity per package (160 vs 288 GB), which means more
  packages for huge-KV pools. It does not win on training.

## Risks / limits
1. Delivering ~2,700 A at 0.75 V up through a 4-high DRAM stack (power-TSV area), plus DRAM held at ≥85–95 °C under 1.25 W/mm² logic
   (refresh doubles). This is the #1 kill risk.
2. A custom DRAM die with ~10× the bank parallelism of HBM: no vendor product exists. It needs an SK hynix / Samsung / Micron custom-DRAM program.
3. Yield: KGD die-to-wafer bonding is required (wafer-on-wafer compounds ~0.67 logic yield). Stack-bond yield ≥99% per layer is assumed.
4. Supply: no HBM, but competes for SoIC/hybrid-bond capacity, which is smaller than CoWoS (~95–130k wpm end-2026).
5. Model fragility: the edge over Rubin shrinks to ~1.1× for dense-MLA models. Rubin's 1.8 kW and FP8 figures are estimates.

## Falsification plan
- Calibrate `final.py` against measured B200/GB200 MLPerf-Inference and Artificial Analysis data (±30%). If, after calibration,
  the Continuum / Rubin tok/s/kW on GQA-128K is <1.5×, drop the design.
- 3D thermal + power-integrity simulation (3D-ICE/HotSpot + Voltspot-class): kill if DRAM Tj >95 °C or IR drop >5% at 2 kW.
- CACTI-3DD/Accelergy DRAM model: kill if stacked energy >1.5 pJ/bit or <40 TB/s per package at 160 GB.
- LLMCompass or a cycle-level simulator with real expert-routing traces and paged-KV gathers. DSA gathers are random ~324 B rows.
- Accuracy: NVFP4 KV/weights vs BF16 on RULER/LongBench at 128K. Kill the numerics plan if the drop is >1 point.
