# Continuum: three candidate architectures

**Target and metric.** The target is data-center decode of 0.5–1T-parameter MoE models at 32K+ context. "Best" means the lowest joules and dollars per token at ≥100 tok/s per user. HBM streaming is about 50% of decode energy (est.), so that is the term attacked. The ceiling is about 3x if the vendor margin (28%) and fees (5%) stay; training gains are capped near 1.5x by staff cost.

**Fact vs. estimate.**
- *Vendor or sourced figures:* Rubin about 288 GB HBM4 at about 22 TB/s. Ironwood 192 GB at 7.4 TB/s. WSE-3 44 GB SRAM. Groq about 230 MB per chip. HBM3E about 3.5–4 pJ/bit.
- *My assumptions:* hybrid-bonded DRAM at about 0.5 pJ/bit, about 0.3 Gb/mm² per layer, and 40 TB/s.

**Roofline check (A1).** 800 mm² × 4 layers × 0.3 Gb/mm² gives about 120 GB. Moving 40 TB/s at 0.5 pJ/bit costs about 160 W. Rubin-class HBM at 22 TB/s × 3.5 pJ/bit costs about 620 W.
- 37B active parameters at FP4 is about 18.5 GB per step.
- At 40 TB/s that is a floor of about 0.46 ms per step.
- At batch 64, compute needs only about 5 PF.

**Versus incumbents (est.).**

| Rival | Continuum wins | Continuum loses |
|---|---|---|
| Rubin | About 1.6–1.9x tokens/J on decode | 2.4x less capacity per chip; training |
| Groq | About 500x capacity per chip | — |
| WSE-3 | About 2.7x capacity per die | About 25x bandwidth per wafer |
| Ironwood | — | Training, and Google's optical circuit switching |

**Risks.**
- DRAM retention above about 85 °C when stacked over hot logic.
- Hybrid-bond yield.
- SoIC capacity, which is also scarce.
- FP4 training beyond 12B is unproven.

**Software.** A PyTorch/torch.compile backend plus vLLM/SGLang plugins. Existing models run unchanged at FP8; FP4 needs a short quantization-aware fine-tune.

**Falsification.** Build a 2-high test vehicle and measure pJ/bit and refresh overhead at 95 °C. Then replay a DeepSeek-V3 decode trace in a cycle model, calibrated first against a measured H100 run (27% bandwidth utilization). The design is dead if it gains less than 1.4x tokens/J.

=== IDEAS ===
IDEA 1
NAME: Continuum stacked-DRAM decode die
MECHANISM: Four DRAM layers are hybrid-bonded directly onto an 800 mm² logic die, holding about 120 GB of expert weights and KV at about 40 TB/s and about 0.5 pJ/bit (assumed), with no HBM or CoWoS interposer. Logic sits next to the cold plate, and refresh rate tracks measured die temperature. The closest earlier attempt, HBM-PIM, stalled on programmability; here the logic is an ordinary compiler target and the DRAM is plain memory. Deciding quantity: delivered pJ/bit including refresh at 95 °C.
VALUE: About 1.6–1.9x tokens per joule on MoE decode versus Rubin-class HBM, without consuming HBM supply.

IDEA 2
NAME: Continuum split attention-expert fabric
MECHANISM: Attention dies keep each request's KV in near-stacked DRAM. Separate expert dies hold FFN weights in cheap LPDDR and gather tokens from about 2,000 concurrent requests, so each expert becomes compute-bound. Routing runs over an optical scale-up fabric. The closest earlier attempt, attention-FFN disaggregation such as MegaScale-Infer, still used HBM on both sides. Deciding quantity: tokens batched per expert per step versus the fabric round-trip latency within a 10 ms token budget.
VALUE: Moves weight capacity onto commodity DRAM, cutting accelerator BOM by roughly 30–40%.

IDEA 3
NAME: Continuum air-cooled FP4 trainer
MECHANISM: Digital FP4 matrix units with per-16-element scales and FP8 fallback for sensitive layers run in 40 kW air-coolable racks on organic-substrate packaging, avoiding CoWoS. The closest earlier attempt, NVFP4 training, stayed within 1–1.5% of FP8 only up to 12B parameters. Deciding quantity: the FP4/FP8 loss gap at 70B or more over 10T tokens.
VALUE: About 1.3–1.5x cheaper pretraining in existing data halls, a gain capped by staff cost.