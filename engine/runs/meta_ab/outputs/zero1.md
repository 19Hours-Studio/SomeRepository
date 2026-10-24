# Continuum: a decode-first inference architecture

*No CONTEXT block came through with your message, so the figures below are approximate public numbers from my own knowledge.*

**Target and metric.** Continuum targets data-center inference for frontier LLMs: MoE models, 128K–10M-token contexts, and agentic decode. It is judged on one metric, **joules per output token at a fixed latency SLO (≥200 tok/s/user)**, with $/token as the tiebreaker. Training is out of scope. The training market keeps rewarding GPUs, while the much larger inference market is bottlenecked by memory traffic, not FLOPs.

**Why the incumbents lose on this metric**
- **Rubin-class GPUs (~288 GB HBM4, ~20 TB/s) and Ironwood (192 GB HBM3E, ~7.4 TB/s).** Decode streams every active weight and KV byte across the HBM PHY for very little arithmetic. HBM access costs about 3–5 pJ/bit, versus about 0.1 pJ/bit for on-die SRAM.
- **WSE-3 (44 GB SRAM) and Groq LPU (~230 MB/chip).** They avoid the HBM cost, but SRAM density is stuck near 0.02 µm²/bit at N3. Holding trillion-parameter models plus KV cache takes thousands of chips or wafers, so capital cost explodes.

**Architecture**
- **Compute:** 3D-stacked logic-on-DRAM with hybrid bonding at about 1 µm pitch. Arithmetic sits next to where bytes live.
- **Memory:** On-package DRAM stacks, about 512 GB per package. Bandwidth is taken vertically through 10⁶+ bond pads, not through the HBM shoreline.
- **Interconnect:** Co-packaged optics, a flat 4,096-package domain, and expert-parallel routing in hardware.
- **Numerics:** Native codebook arithmetic, described below.
- **Programming model:** A graph compiler that places experts and KV shards spatially. The user writes ordinary PyTorch.
- **Packaging and power:** About 1.2 kW per package with liquid cooling.

**What must be true**
1. Hybrid-bonded DRAM-on-logic must yield at least about 85%. The thermal coupling between hot logic and DRAM refresh is the real risk.
2. Frontier models must tolerate quantization to 2–3 effective bits/weight with under 0.5% quality loss.
3. Labs must co-design models with the hardware, as they now do for TPUs.

If all three hold, the estimate is about 10× joules/token versus Rubin on long-context decode. If the first fails, Continuum collapses into an expensive HBM chip.

=== IDEAS ===
IDEA 1
NAME: Codebook-Native Lookup Compute
MECHANISM: Weights are stored only as 2–4-bit indices into small learned codebooks, one per 256-weight block. The datapath never decompresses them: each activation is multiplied once against the 16 codebook entries, and indices then select and accumulate those precomputed products. Codebooks are refit per layer after deployment, using calibration traffic, without changing the indices.
VALUE: It cuts weight-movement energy and bandwidth 4–8× versus FP8 while replacing multipliers with adders and table reads.

IDEA 2
NAME: Attention-In-DRAM KV Stacks
MECHANISM: The KV cache lives in DRAM dies whose bonded logic layer computes QKᵀ, an online softmax, and the V-weighted sum locally per bank. Only the query vector enters each stack and only a partial output plus a normalizer leaves. Each bank tracks which tokens draw little attention and demotes them to lower precision or evicts them, so capacity adapts to each conversation.
VALUE: Million-token-context decode costs roughly the same per token as short-context decode, because KV bytes never cross a chip boundary.

IDEA 3
NAME: Checksum-Guarded Near-Threshold Compute
MECHANISM: Matrix engines run at about 0.45 V, below safe timing margins, and accept occasional bit errors. Algorithm-based fault-tolerance checksums on every tile product detect corrupted results, and only the affected tiles are recomputed. A controller tracks the error rate per voltage island and lowers each island's voltage until recompute overhead equals the energy saved.
VALUE: It delivers about 2–3× better compute energy efficiency on the same process node without sacrificing output correctness.