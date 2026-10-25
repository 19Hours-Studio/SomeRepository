=== GATE ===
IDEA 1: SRAM-resident MoE expert farm
KILLER | SRAM left for KV cache after the weights, measured as concurrent users at 500 tok/s on 8k-in/1k-out traffic (~9k-token context; MiniMax-M2 has 62 layers × 8 KV heads × head dim 128, so KV is 127 KB/token at FP8 and 71 KB at NVFP4). To get near GB300's $/Mtok, a 3-wafer system at ~$571/hr TCO (3 × ~$3M CS-3-class wafers over 4 years, with the package taken as 45% of TCO) has to sell ~2.64M tok/s | required ~5,300 users | available 61 users (FP8 weights and KV, 70 GB free) to 265 users (FP4 weights and NVFP4 KV, 171 GB free) out of 300 GB SRAM (config: HF MiniMax-M2/M2.5 config.json; price: Next Platform/AIM CS-3 $2–4M; arithmetic in gate_calc.py, with the KV formula checked against Llama-3-70B's known 320 KiB/token) | MARGIN 0.05 (0.012 at FP8)
CHAIN | GB300 NVL72 disaggregated serving of MiniMax M2.5/M2.7 | now $0.06 /Mtok | with idea ~$1.2–5.2 /Mtok | RATIO 0.012–0.05
VERDICT | DEAD | Keeping all 230B parameters in SRAM leaves almost no room for KV cache, so the batch is roughly 20–90× too small to amortise wafer-class silicon; also, 300 GB in "2.5–3 wafers" needs ~100–120 GB per wafer, against WSE-3's 44 GB (≈6.8 wafers at WSE-3 density).
NEW FACT | MiniMax-M2: 62 layers, 8 KV heads, head_dim 128, 256 experts with top-8 routing | https://huggingface.co/MiniMaxAI/MiniMax-M2/blob/refs%2Fpr%2F57/config.json
NEW FACT | Cerebras CS-3 price is unpublished; estimates are ~$2.5M per node, ~$3.2M per system, and ~$4M with MemoryX/SwarmX | https://www.nextplatform.com/2024/03/14/cerebras-goes-hyperscale-with-third-gen-waferscale-supercomputers/

IDEA 2: Decode-only part, disaggregated prefill/training
KILLER | Decode power per package at Rubin-class 22 TB/s. "2× tokens per kW" needs ≤ half of Rubin's decode draw (taken as 0.8 × ~2.3 kW TDP, an analyst estimate). The floor is HBM read at 3.44–5.74 pJ/bit, plus 3.6 TB/s scale-up SerDes at ~5 pJ/bit, plus on-die movement at ~1 pJ/bit, plus ~100 W for compute and leakage | required ≤920 W | available floor 1,025–1,430 W (HBM pJ/bit: arXiv 2602.18568 and 2607.26491; Rubin 22 TB/s and ~2.3 kW: spheron/introl secondary sources) | MARGIN 0.64–0.9
CHAIN | Rubin NVL72 + CPX disaggregated serving, $/Mtok on owner TCO | now 1.0 (normalised) | with idea 0.76–0.89 (2× tok/kW halves energy at 9% and power-provisioned facility at 12%; the upper end also assumes a generous 30% cut in package cost from dropping training FLOPs, but HBM dominates the BOM) | RATIO 1.12–1.32
VERDICT | WOUNDED | The trade-offs are stated honestly and the design is physically plausible, but HBM access energy alone takes most of the claimed 2× power budget, and energy is only ~9% of TCO, so even a full 2× tok/kW cuts cost per token by about 1.1–1.3×, short of 1.5×.
NEW FACT | Rubin GPU HBM4 is reported at up to 22 TB/s per GPU, with a ~2,300 W TDP from analyst estimates that Nvidia has not confirmed; one source warns that initial bandwidth may fall below 22 TB/s | https://www.spheron.network/blog/nvidia-vera-rubin-nvl72-guide/ ; https://introl.com/blog/nvidia-vera-rubin-platform-8-exaflops-infrastructure
NEW FACT | HBM3E access energy is ~3.44 pJ/bit in one model and ~5.74 pJ/bit including I/O in another; HBM4 has no primary pJ/bit figure | https://arxiv.org/pdf/2602.18568 ; https://arxiv.org/pdf/2607.26491

The script is `/home/user/SomeRepository/engine/runs/v6_continuum/eval_g0/c3/gate_calc.py`, not committed. Several decisive inputs are my own assumptions, not sourced: TCO/hr from the 45% package share, Rubin drawing 80% of TDP during decode, ~5 pJ/bit SerDes and ~1 pJ/bit on-die movement, and the 30% package-cost cut.

Sources:
- [MiniMax-M2 config](https://huggingface.co/MiniMaxAI/MiniMax-M2/blob/refs%2Fpr%2F57/config.json)
- [MiniMax-M2.5 config](https://huggingface.co/MiniMaxAI/MiniMax-M2.5/blob/refs%2Fpr%2F40/config.json)
- [Next Platform CS-3](https://www.nextplatform.com/2024/03/14/cerebras-goes-hyperscale-with-third-gen-waferscale-supercomputers/)
- [AIM Research CS-3](https://aimresearch.co/?p=12750)
- [Spheron Vera Rubin guide](https://www.spheron.network/blog/nvidia-vera-rubin-nvl72-guide/)
- [Introl Vera Rubin](https://introl.com/blog/nvidia-vera-rubin-platform-8-exaflops-infrastructure)
- [arXiv 2602.18568](https://arxiv.org/pdf/2602.18568)
- [arXiv 2607.26491](https://arxiv.org/pdf/2607.26491)