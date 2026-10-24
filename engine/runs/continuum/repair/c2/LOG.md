# LOG — repair c2 (scripts: idea1_prefill.py, idea1_round2.py, idea1_ttft.py, idea2_attnstack.py, idea2_cost.py)

| # | idea | change | decisive number | result |
|---|------|--------|-----------------|--------|
| 1 | I1 memory-light prefill | test kill claim: 1 die holds the whole model, EP | per-expert FLOP/B = 910 at 8K tok/pass (256 tok/expert); 1M tok/pass needed to pass a 30k ridge | kill confirmed for whole-model-per-die EP; plus EP all-to-all 0.65 TB/s/die → needs NVLink |
| 2 | I1 | layer-pipeline: 8 dies × 47 GB of the 376 GB FP4 weights, layer-major mega-batch | balance at 22k tok/pass (10 PF) / 45k (20 PF); inter-stage 15 GB/s; KV egress 2.4 GB/s/die; TTFT 0.69 s | works physically; no scale-up fabric |
| 3 | I1 | 10 PF die → 20 PF (power-density limit 1.48 W/mm², ~Rubin's); add facility $10/W | all-in $/Mtok prefill: 0.00077 vs Rubin 0.00098 (1.27×), CPX-HBM4 0.00092 (1.20×), B200 2.7× | modest cost win; main win 0 GB HBM, 0 CoWoS (Rubin 1.26 GB HBM per 1k tok/s) |
| 4 | I1 | 128K single prompt TTFT | 1.02 s (8 chunks) vs 0.37 s 8×Rubin CP | loses ~2.8× on single long-prompt latency |
| 5 | I1 | sensitivity LPDDR $21/GB; HBM4 $32/GB | 0.00082 vs Rubin 0.00119 → 1.45× | win holds; grows if HBM4 price rises |
| 6 | I2 in-HBM attention | recompute energy incl. GPU-side path (PHY+NoC 15 mm+L2/SMEM) | 5.34 → 3.58 pJ/b = 33% saving (kill test: 15%; claim: 2×) | the energy-based claim fails; at best ~1.5× |
| 7 | I2 | find the regime: detach stacks from GPU (JEDEC SPHBM4 organic mount, Jul 2026); base die = GQA attention engine + narrow link | link need 0.21 GB/s decode (KV/link = 8,000×) + ~2 GB/s KV ingress; RT latency 0.16 ms/step | the value is capacity/BW scaling off CoWoS, not energy |
| 8 | I2 | cost/Mtok Llama-70B-class 128K FP8 KV vs Rubin-only, Lamina(H200) | COGS 0.177 vs 0.304 (1.71×); price view 2.6×; FP4 KV 1.69×; 16K ctx 1.53× | WORKS in GQA long-context niche |
| 9 | I2 | base die power & thermal | 13–19 W (FP8, 2–2.5 TB/s); FP4 KV 23–34 W (too hot → FP8 math only, FP4 storage at reduced BW); 1-D stack ΔT 20–40 K | deciding unknown = stack thermal resistance; MLA (484 FLOP/B → 387 W) and DSA indexer (128 FLOP/B → 102 W) excluded |
| 10 | novelty | Duplex (arXiv 2409.01141) = GPU-attached base-die logic-PIM for GQA/MoE; Lamina = attention on cheap GPUs; CENT = CXL GDDR6-PIM | detached SPHBM4 attention-stack nodes: no prior found | anchor kept, version distinct |

## Consistency tables

### Idea 1 (Continuum-P, 8-stage, 20 PF FP4 dense/die, 64 GB LPDDR5X 1024-bit @10.7 Gb/s)
| limit | value used | window | ok? |
|---|---|---|---|
| LPDDR BW (1.37 TB/s peak, 80% sustained) | weights 47 GB/pass + act/KV ~4 GB at T=90k → ~0.55 of the time | ≤0.9 | ok |
| LPDDR capacity 64 GB | 47 weights + 0.4 KV stage + 2.6 act | ≤64 | ok (14 GB prefix cache) |
| on-die SRAM | expert tile 25 MB + 2.8k tok × 7 KB = 45 MB | ~128 MB | ok |
| inter-stage link | 15–45 GB/s | x8 112G SerDes ≈ 112 GB/s | ok |
| KV egress | 2.4–5 GB/s/die (MLA); 70B GQA 1 die 14 GB/s | 400G NIC 50 GB/s | ok |
| power density | 1.48 W/mm² | Rubin ≈1.4 W/mm² liquid | at limit |
| TTFT p50 8K | 0.69 s | ≤1 s | ok |
| TTFT 128K single | 1.02 s | ≤1 s | marginal / loses vs 8×Rubin 0.37 s |
| NVFP4 W4A4 accuracy | FACT 3: −0.04 pt MMLU-Pro (training, hybrid model) | ≤1% | unverified for prefill-KV quality |

### Idea 2 (Continuum-A stack: 16-high 48 GB HBM4 DRAM dies, N4 attention base die, 2.0–2.5 TB/s)
| limit | value used | window | ok? |
|---|---|---|---|
| base-die logic power | 13–19 W FP8 | StreamDQ-class "low-power IP" only; no published budget | UNKNOWN (decides) |
| DRAM temp | 1-D ΔT 20–40 K above lid with 17 W base | 85 °C (95 °C 2× refresh) | ok only if lid ≤ ~50 °C and k_int ≥ 3 W/mK |
| link decode | 0.2–0.4 GB/s/stack | x4 lane 14–25 GB/s | ok |
| KV ingress after prefill | ~1 GB/s/user (21.5 GB per 20 s session) → 2 GB/s/stack | 14–25 GB/s | ok |
| GPU NIC aggregate | 758 stacks × 0.21 = 160 GB/s | Rubin ~200 GB/s | 80%, tight → cap batch ~1,200 |
| per-layer RT latency | 80 × 2 µs = 0.16 ms | step 21–25 ms | ok (ping-pong) |
| tok/s/user | 49 (2.5 TB/s, 90% fill) | ≥40 | ok; Rubin-only gives 74 |
| model class | GQA group 8 → 16 FLOP/B | MLA 484, DSA 128 FLOP/B | niche-limited |

## Sources
- Duplex: https://arxiv.org/pdf/2409.01141 ; StreamDQ base-die thermal: https://arxiv.org/pdf/2607.08993
- JEDEC SPHBM4 (JESD330-4, Jul 2026): https://blocksandfiles.com/2025/12/17/jedec-sphbm4/ , https://www.01net.it/new-jedec-sphbm4-standard-enables-hbm4-class-bandwidth-on-organic-substrates/
- Lamina: https://arxiv.org/abs/2405.01814
- HBM prices: https://capitalandcompute.net/memory-prices/hbm/ , https://siliconanalysts.com/data/hbm-pricing , https://www.sammyfans.com/2026/10/02/samsung-seeks-more-than-3x-hbm3e-pricing-for-hbm4/
- Rubin CPX → 168 GB HBM4 (Kuo): https://technews.tw/2026/09/02/nvidia-rubin-cpx-reenters-roadmap-hbm4-ai-prefill/
- VR200 $7.8M rack / $55K GPU (MS via): https://wccftech.com/nvidia-vera-rubin-rack-hit-with-memory-price-surge-pushing-hbm4-lpddr5x-bill-to-2m-of-7-8m-total/amp/
- B200 COGS ~$6.4K, prices: https://intuitionlabs.ai/articles/nvidia-ai-gpu-pricing-guide
- Intel Crescent Island 160 GB LPDDR5X: https://newsroom.intel.com/artificial-intelligence/intel-to-expand-ai-accelerator-portfolio-with-new-gpu
- SOCAMM2 154 GB/s: https://community.cadence.com/cadence_blogs_8/b/ip/posts/socamm-modernizing-datacenter-memory-with-lpddr6-5x
- Ledger FACTs 1,3,5,6,7,13 (../../evidence.md)
- My estimates (flagged): GPU-side 80 fJ/b/mm × 15 mm, SRAM 0.15 pJ/b/pass, 0.4–0.6 pJ/FLOP FP8, N3 wafer $20K, D0 0.1, sys overhead 35%, facility $10/W, interface k 1.5–3 W/mK.
