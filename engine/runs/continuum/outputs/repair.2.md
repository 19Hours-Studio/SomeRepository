=== IDEAS ===
IDEA 1
NAME: Layer-pipelined LPDDR prefill dies
MECHANISM: The anchor is kept: a dense FP4/FP8 compute die with no HBM runs the compute-bound prefill phase, sends the KV to the decode tier over a plain NIC, and uses the same ISA and compiler as that tier. The kill test was right that one die holding a whole MoE model is memory-bound: on DeepSeek-V3 at 8K tokens per pass, each expert sees only 256 tokens, which gives 910 FLOP/B. The repair splits the model's layers across 8 dies. Each die (20 PF dense FP4, 800 mm², ~1.18 kW) keeps 47 GB of the 376 GB of NVFP4 weights in 64 GB of 1024-bit LPDDR5X (1.37 TB/s) and pushes a large batch of tokens through one layer before moving to the next (layer-major mega-batch). That makes a die compute-bound from about 45K tokens per pass. Only activations cross between dies (15–45 GB/s, against the 0.65 TB/s per die that expert-parallel all-to-all would need), so no NVLink-class scale-up fabric is required. KV egress is 2.4–5 GB/s per die, TTFT is 0.69 s at 8K prompts, and the design uses 0 GB of HBM and no CoWoS.
VALUE: All-in cost per prefill token comes out 1.27× cheaper than Rubin, 1.20× cheaper than the revived HBM4 Rubin CPX and 2.7× cheaper than B200, rising to about 1.45× vs Rubin if HBM4 reaches $32/GB. It also removes the ~1.26 GB of HBM Rubin needs per 1K prefill tok/s.

IDEA 2
NAME: Detached attention-stack memory nodes
MECHANISM: The anchor is kept: the custom HBM4 logic base die runs GQA decode attention (QKᵀ, softmax, AV at FP8) on KV read through the TSVs, and only partial outputs leave the stack. The repair takes the stack off the GPU interposer. It uses a JEDEC SPHBM4-style organic-substrate mount (standard published July 2026), with a narrow link in place of the 2048-bit host bus. Each 48 GB, 2.5 TB/s stack becomes a separate KV node with a 13–19 W attention base die. It serves 2 users at 128K context (FP8 KV) at 49 tok/s each and needs only 0.2 GB/s of decode link, because KV bytes read outnumber link bytes about 8,000 to 1 (plus ~2 GB/s to load KV after prefill). The claimed 2× energy saving does not hold: counting the GPU-side NoC, L2 and shared-memory path, it is 33% (5.34 → 3.58 pJ/bit). The real gain is that KV capacity and bandwidth grow without CoWoS or GPU silicon: one Rubin handles weights and FFN for about 1,200–1,500 users while 400–760 stacks hold their KV.
VALUE: Long-context (128K) GQA decode costs about 1.7× less per million tokens than the best baseline (Rubin-only: $0.177 vs $0.304 at cost of goods; 2.6× at market prices), and 1.5× less at 16K context.

=== NOTES ===

**Idea 1: Layer-pipelined LPDDR prefill dies**
- **Anchor kept?** Yes. It is still an HBM-free prefill die that shares its ISA with the decode tier. What changed is how the model is split across dies (by layer, not by expert) and how tokens are scheduled (layer-major mega-batches).
- **Decisive numbers:**
  - DeepSeek-V3 public config: 669B parameters, 35.6B active per token, 92 GFLOP per token at 8K context.
  - NVFP4 at 4.5 bits per value (user note, FACT 3).
  - LPDDR5X at 9.6–10.7 Gb/s; a SOCAMM2 module gives 154 GB/s (Cadence). Vera reaches 1.2 TB/s on LPDDR, so the bandwidth is reachable (FACT 5).
  - Rubin CPX has reportedly been redesigned around 168 GB of HBM4 (Kuo, via TechNews, Sept 2026). The GDDR7 CPX that the kill test called prior art is no longer the shipping plan.
  - Rubin is about $55K per GPU, and the VR200 rack about $7.8M (Morgan Stanley via Wccftech).
  - HBM4 is $10–16/GB, with Samsung asking ~$32/GB; LPDDR is $7.8–21/GB (FACT 1).
- **Best-baseline comparison** (per million prefill tokens delivered, all-in: cost of goods + 35% system + power + $10/W facility):

  | Design | $/M prefill tokens |
  |---|---|
  | Continuum-P | 0.00077 |
  | Rubin | 0.00098 |
  | CPX-HBM4 | 0.00092 |
  | B200 | 0.0021 |
  | H100 (cheapest, cost of goods) | 0.0042 |
  | B200 rented at $4.5/h | 0.021 |

  At cost of goods the win is modest. HBM and CoWoS independence is the main value.
- **Consistency table** (in LOG.md): all checks pass.
  - LPDDR bandwidth ≤0.9 used.
  - Capacity: 50 of 64 GB used.
  - Links: 45 of 112 GB/s used.
  - TTFT at 8K: 0.69 s.
  - Power density sits at the limit (1.48 W/mm², about the same as Rubin), so liquid cooling is required.
  - It loses on single long-prompt latency: 1.02 s vs 0.37 s for 8 Rubins at 128K.
- **Hazards:**
  - The prefill benefit depends on NVFP4 weights × activations being accurate enough. The NVFP4 evidence is from training, not from KV quality.
  - Hot experts cause imbalance across pipeline stages.
  - LPDDR prices are rising (FACT 10).
  - The die is 30% smaller than Rubin, and there is little room left to cool it harder.
- **Deciding unknown:** sustained FP4 utilization of layer-major MoE prefill when weights stream from LPDDR (I assumed 0.6).
- **Cheapest experiment:** on a GB200 node, keep weights in Grace LPDDR and stream them over NVLink-C2C. This emulates the memory-light die. Sweep tokens per pass from 4K to 128K (8 points × 3 prompt lengths × 5 runs = 120 runs). Measure the knee and FLOP utilization. The design fails if the knee sits above ~150K tokens or utilization is below 0.4.
- **Closest work:** Rubin CPX (now HBM4), Intel Crescent Island (160 GB LPDDR5X, general inference), Qualcomm AI200 (not verified in my searches). None of them pairs a pipelined, prefill-only design with LPDDR-resident layer slices.
- **Verdict:** WORKS. The cost win is modest (1.2–1.45×); the supply win (no HBM, no CoWoS) is large.

**Idea 2: Detached attention-stack memory nodes**
- **Anchor kept?** Yes: attention runs in the HBM4 base die on KV read through the TSVs, and only partial outputs leave. What changed is that the stack is detached on organic substrate and its value is cost, not energy.
- **Decisive numbers:**
  - HBM energy is 3.44 pJ/bit, of which 0.25 is I/O (FACT 6/7).
  - The GPU-side path is my own estimate: ~80 fJ/bit/mm over 15 mm, plus three SRAM passes at 0.15 pJ/bit each.
  - GQA with groups of 8 at FP8 needs 16 FLOP/B. That works out to 32–40 TFLOPS and 13–19 W per stack.
  - MLA needs 484 FLOP/B (≈387 W) and the DSA indexer 128 FLOP/B (≈102 W), so both are excluded.
  - SPHBM4 (512 data pins with 4:1 serialization, on organic substrate) is the enabler.
- **Best-baseline comparison** (Llama-70B-class model, 128K context, $/M decode tokens at cost of goods):

  | Option | $/M decode tokens | Ratio |
  |---|---|---|
  | Attention stacks | 0.177 | — |
  | Rubin-only | 0.304 | 1.71× |
  | Lamina-style attention on H200s | 0.466 | 2.6× |
  | Stacks, FP4 KV | 0.101 | — |
  | Rubin-only, FP4 KV | 0.171 | 1.69× |

  Duplex (GPU-attached) only gets the ~33% energy saving on the KV share. Rubin-only also gives faster service per user (74 vs 49 tok/s), so the ratio compares slightly different service levels.
- **Consistency table** (in LOG.md):
  - Link, KV ingress and per-layer latency are fine.
  - GPU NIC aggregate is tight at 80%, so batch should be capped at about 1,200 users.
  - The base-die thermal budget is UNKNOWN. A 1-D estimate gives a 20–40 K rise above the lid; this is acceptable only if bond-layer k is at least 3 W/mK and the lid stays at or below ~50 °C.
  - FP4 KV at full bandwidth needs 23–34 W, which is too hot. Store KV in FP4 but run the stack at reduced bandwidth.
- **Hazards:**
  - DRAM retention failures if the base die heats the stack.
  - The niche is shrinking as models move to MLA, DSA sparse attention, and linear-attention hybrids.
  - HBM4 price could reach $32/GB. The win still holds there: 0.26 vs 0.37.
  - It depends on vendors supplying custom SPHBM4 base dies.
- **Deciding unknown:** junction-to-lid thermal resistance of a 16-high stack with 15–20 W in the base die.
- **Cheapest experiment:** a thermal test vehicle. Take an HBM4/SPHBM4 daisy-chain stack, or a 16-die dummy stack with the same bond layers, put a heater in the base die, and sweep 0–25 W with the DRAM layers at 51 W. Use n ≥ 5 stacks × 2 bond types, then run a retention-at-temperature test at 85/95 °C. The design fails if a 16 W base die pushes DRAM above 85 °C with a 45 °C lid.
- **Closest work:** Duplex (base-die Logic-PIM attached to the GPU), NOVA (2026), StreamDQ (dequantization in a custom HBM base die), Lamina (attention on cheap GPUs), CENT (CXL GDDR6-PIM). I found no detached, organic-mounted HBM4 attention-stack node.
- **Verdict:** NICHE. It works for GQA long-context decode (≥16K). It fails for MLA and DSA models, and it depends on a thermal result.

Scripts and the full log are in `/home/user/SomeRepository/engine/runs/continuum/repair/c2/` (`LOG.md` plus 5 Python files).

Sources:
- [Duplex (arXiv 2409.01141)](https://arxiv.org/pdf/2409.01141)
- [NOVA (arXiv 2608.22613)](https://arxiv.org/pdf/2608.22613)
- [StreamDQ (arXiv 2607.08993)](https://arxiv.org/pdf/2607.08993)
- [Lamina (arXiv 2405.01814)](https://arxiv.org/abs/2405.01814)
- [JEDEC SPHBM4 (Blocks & Files)](https://blocksandfiles.com/2025/12/17/jedec-sphbm4/)
- [SPHBM4 on organic substrates (01net)](https://www.01net.it/new-jedec-sphbm4-standard-enables-hbm4-class-bandwidth-on-organic-substrates/)
- [HBM prices (Capital & Compute)](https://capitalandcompute.net/memory-prices/hbm/)
- [HBM pricing (Silicon Analysts)](https://siliconanalysts.com/data/hbm-pricing)
- [Samsung HBM4 pricing ask (Sammyfans)](https://www.sammyfans.com/2026/10/02/samsung-seeks-more-than-3x-hbm3e-pricing-for-hbm4/)
- [Rubin CPX moves to HBM4 (TechNews)](https://technews.tw/2026/09/02/nvidia-rubin-cpx-reenters-roadmap-hbm4-ai-prefill/)
- [VR200 rack cost (Wccftech)](https://wccftech.com/nvidia-vera-rubin-rack-hit-with-memory-price-surge-pushing-hbm4-lpddr5x-bill-to-2m-of-7-8m-total/amp/)
- [GPU pricing guide (IntuitionLabs)](https://intuitionlabs.ai/articles/nvidia-ai-gpu-pricing-guide)
- [Intel Crescent Island](https://newsroom.intel.com/artificial-intelligence/intel-to-expand-ai-accelerator-portfolio-with-new-gpu)
- [SOCAMM2 bandwidth (Cadence)](https://community.cadence.com/cadence_blogs_8/b/ip/posts/socamm-modernizing-datacenter-memory-with-lpddr6-5x)
- [Samsung HBM base die at Hot Chips 2026 (ServeTheHome)](https://www.servethehome.com/samsung-evolving-hbm-base-die-at-hot-chips-2026/)