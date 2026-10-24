=== GATE ===
IDEA 1: GDDR7 disaggregated attention rack
KILLER | Cost of delivered KV bandwidth, GDDR7 versus HBM3E. It counts the memory device, CoWoS share, and electricity over 4 years at 100% use, $0.13/kWh and PUE 1.3. The "halving" claim needs the HBM-to-GDDR7 cost ratio to be at least 2x. | required ≥2.0x cheaper per GB/s | available 1.36–1.61x at device level (HBM3E $0.67 vs GDDR7 $0.42–0.50 per GB/s, both all-in) and about 2.0–2.5x at card BOM level ($0.80 vs $0.32–0.41 per GB/s). Inputs: SK hynix 12-high HBM3E ≈ $350 per stack (Notebookcheck); GDDR7 ≈ $10–15/GB at card level (Implicator); RTX 5090 512-bit at 1.79 TB/s; ledger D gives CoWoS $1.1k and BOM $6.4k for 8 TB/s. GDDR7 at about 5.5 pJ/bit is my estimate. | MARGIN 0.75
CHAIN | GB200 NVL72 with disaggregated prefill/decode. Attention–FFN disaggregation is already in use (MegaScale-Infer / Step-3 style). | now 1.0 $/token at long-context decode | with idea about 0.75–0.80. This assumes KV is 60% of decode cost and becomes 1.5–2x cheaper, minus extra link and network cost. | RATIO 1.3
VERDICT | WOUNDED | The bandwidth cost gain is real but nearer 1.4–1.6x than 2x. Also, each chip has only about 2 TB/s of GDDR7 pins, so the design needs about 4 attention chips for each HBM GPU. The board, power and network for those chips use up part of the saving.
NEW FACT | An HBM4 stack for Nvidia costs around the mid-$500s in 2026. A 12-high HBM3E stack costs about $350 from SK hynix and about $100 less from Samsung. | https://www.notebookcheck.net/Nvidia-may-raise-prices-as-it-pays-Samsung-double-for-future-HBM4-AI-memory-modules-with-3-3-TB-s-bandwidth.1172580.0.html
NEW FACT | GDDR7 costs about $10–15/GB at card level (RTX 5090 32 GB vs RTX Pro 6000 96 GB). Prices are expected to rise another 5–20% by late 2026. | https://www.implicator.ai/ram-prices-ease-2028-high-vram-gpus-different-story/

IDEA 2: Fixed attention engine in DRAM
KILLER | Share of token energy actually removed. A base-die engine still pays for row activation, on-die data movement and TSVs. It saves only the PHY/interposer energy and the GPU-side NoC/L2 energy. "Halving" means removing 50% of token energy. | required 50% of token energy | available ≈10% (range 7–16%). This is HBM about 50% of token energy (ledger est.) × KV 70% of bytes at 32K and batch 32 (measured in my roofline) × removable 19–28% per bit. The per-bit split is I/O 0.25 of 3.44 pJ/bit (RPU model), with GPU-side cost of 0.5–1.0 pJ/bit as my estimate. FGDRAM finds on-die data movement is the largest HBM2 term and I/O is a small remainder. | MARGIN 0.2
CHAIN | HBM GPU running FlashDecoding with an FP8 KV cache | now 242 mJ/token at 16K (arXiv 2605.11999) | with idea about 215–225 mJ/token | RATIO 1.1
VERDICT | DEAD | The idea's own deciding condition does hold: KV share is 0.55–0.91 at 16K–128K with batch 32. But even removing 100% of KV movement energy only gives 1.54x, and a base die can only remove about a quarter of it.
NEW FACT | AttAcc (ASPLOS 2024) puts attention in bank-level HBM-PIM, not the base die. It reports up to 2.67x energy efficiency on a 175B model. Gains of this size need in-bank compute. | https://unpaywall.org/10.1145%2F3620665.3640422
NEW FACT | The FGDRAM model gives HBM2 ≈ 3.97 pJ/bit. On-die data movement from row buffer to I/O is the largest term, then activation, and I/O is a small remainder. | https://research.nvidia.com/publication/2017-10_fine-grained-dram-energy-efficient-dram-extreme-bandwidth-systems

IDEA 3: Stacked-SRAM weights, HBM KV
KILLER | Weight share of HBM bytes per decode step at deployed batch, for 671B FP4 DeepSeek-class MLA on GB200-class parts (5 PF FP8 dense, 8 TB/s, 4.66 GB of weights per GPU) | required ≈50% (the idea's own condition for 2x) | available 12% at 32K and batch 32 per GPU. It is 53% only at batch 4 per GPU, and 36% at 8K and batch 32. Absorbed MLA attention runs at 484 FLOP/B against a ridge of 625, so the step is nearly compute-bound (roofline in gate_calc.py; MLA dimensions checked against the published ~70 KB/token). | MARGIN 0.24
CHAIN | GB200 NVL72 serving DeepSeek-class MoE with EP/DP attention | now step time 5.3 ms at 32K and batch 32 per GPU | with idea 4.6 ms, so 1.14x speed. That is offset by about $650 or more of SRAM plus bonding on each of 96 packages instead of 72 GPUs. | RATIO 1.08 (up to about 1.3 at 8K context)
VERDICT | DEAD | Capacity (3.93 of 4 GB) and SRAM cost (about $530 on N7) both check out. But at throughput batch sizes the KV cache dominates the bytes, and the MLA step is nearly compute-bound, so the 2x shrinks to about 1.1x at 32K.
NEW FACT | RTX 5090: 512-bit GDDR7, about 1,792 GB/s, 575 W TGP. This sets the practical per-chip limit on GDDR7 bandwidth. | https://digitalproduction.com/2025/01/07/nvidias-rtx-5090-overkill-or-exactly-what-your-render-farm-needs/

IDEA 4: Attention-only near-memory KV engine
KILLER | DRAM-core share of access energy. The idea assumes it is ≤40%, i.e. at least 60% of per-bit energy can be removed. | required removable ≥60% per bit (to halve token energy, ≥50% of token energy) | available 7% per bit inside HBM (I/O 0.25 of 3.44 pJ/bit, RPU model), or about 28% if GPU-side NoC/L2 at 1 pJ/bit counts (my estimate). That works out to about 10% of token energy. FGDRAM also says core data movement and activation dominate. | MARGIN 0.2
CHAIN | HBM GPU running FlashDecoding with an FP8 KV cache, GQA model | now 242 mJ/token at 16K (arXiv 2605.11999) | with idea about 215–225 mJ/token | RATIO 1.1
VERDICT | DEAD | The core-share assumption is backwards: the DRAM core is roughly 70–93% of access energy, not ≤40%. So a base-die engine cuts token energy by about 10%, not 50%. Like Idea 2, it gives nothing on MLA.
NEW FACT | TokenStack (arXiv, May 2026), a heterogeneous HBM-PIM design, reports 30–47% lower energy per token than AttAcc. Bank-level PIM is the competitor this idea has to beat. | https://arxiv.org/pdf/2605.05639

Notes:
- **Files:** The calculations are in `gate_calc.py` and `gate_calc_output.txt` in the c1 directory. They include known-answer checks for KV per token: Llama-70B 320 KiB and DeepSeek-V3 MLA about 69 KiB. Nothing was committed.
- **Estimates:** The 50% HBM share of token energy and the GDDR7 pJ/bit figure are estimates, not measurements.
- **What would settle it:** A real split of HBM3E/HBM4 per-bit energy into core and I/O needs a vendor or ISSCC source; the PDFs could not be downloaded here. Real deployed batch sizes need traces.

Sources:
- [Notebookcheck HBM pricing](https://www.notebookcheck.net/Nvidia-may-raise-prices-as-it-pays-Samsung-double-for-future-HBM4-AI-memory-modules-with-3-3-TB-s-bandwidth.1172580.0.html)
- [Implicator GDDR7 pricing](https://www.implicator.ai/ram-prices-ease-2028-high-vram-gpus-different-story/)
- [Fine-Grained DRAM (NVIDIA)](https://research.nvidia.com/publication/2017-10_fine-grained-dram-energy-efficient-dram-extreme-bandwidth-systems)
- [Chatterjee HPCA 2017](https://research.nvidia.com/sites/default/files/pubs/2017-02_Architecting-an-Energy-Efficient/chatterjee.hpca2017.pdf)
- [RPU paper (HBM3E 3.44 pJ/bit model)](https://arxiv.org/pdf/2602.18568)
- [AttAcc](https://unpaywall.org/10.1145%2F3620665.3640422)
- [TokenStack](https://arxiv.org/pdf/2605.05639)
- [RTX 5090 specs](https://digitalproduction.com/2025/01/07/nvidias-rtx-5090-overkill-or-exactly-what-your-render-farm-needs/)
- [Rubin CPX rumor](https://www.ithome.com/0/883/345.htm)