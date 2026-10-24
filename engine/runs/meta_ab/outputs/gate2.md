=== GATE ===
IDEA 1: Attention Inside HBM Base-Die
KILLER | Attention energy gain from doing top-k plus flash-decode in the base die, compared with running the same top-k sparse attention on the GPU. Keeping data on the stack saves only the off-stack I/O energy; the DRAM array, row activation and TSV energy are still spent | required 10x (the "order of magnitude" claim) | available 1.08x (I/O is 0.25 of 3.44 pJ/bit for HBM3e, arXiv 2602.18568). KAIST measured 1.10x energy efficiency for PIM-HBM against GPU-HBM | MARGIN 0.11
CHAIN | GPU decode with top-k sparse attention computed on the compute die (DeepSeek-V3.2 DSA picks the top 2048 tokens with an FP8 lightning indexer) | now 1.00 (relative energy/token, archetype C, HBM share 50%) | with idea about 0.96 | RATIO 1.04
VERDICT | DEAD | The order-of-magnitude saving comes from the top-k sparsity, which GPUs already run in production (DSA). Moving it into the base die saves only the 7–10% of HBM energy spent on off-stack I/O.
NEW FACT | DeepSeek-V3.2 already ships top-k sparse attention (k=2048, a separate indexer K cache served in vLLM), so "retrieve-then-attend" is current best practice and not new | https://arxiv.org/pdf/2512.02556 ; https://vllm.ai/blog/2025-09-29-deepseek-v3-2
NEW FACT | A KAIST PIM-HBM study (SPICE-modelled interposer and TSV) gets only a 10.4% average energy-efficiency gain over GPU-HBM | https://koasas.kaist.ac.kr/handle/10203/290541

IDEA 2: Attention Inside the Memory Stack
KILLER | Data-movement energy cut from scoring keys with LSH in the base die, against the same LSH or top-k selection done on the GPU. Only the off-stack PHY hop is removed | required more than 10x | available 1.08x (0.25/3.44 pJ/bit, arXiv 2602.18568; KAIST measured 1.10x) | MARGIN 0.11
CHAIN | GPU sparse attention with an on-die indexer (DSA, Quest-class) | now 1.00 relative decode energy/token | with idea about 0.96 | RATIO 1.04
VERDICT | DEAD | The base die reads its data through the same TSVs, at about the same bandwidth as the external interface, so it removes neither the bandwidth bottleneck nor most of the energy. The >10x figure is the sparsity gain, and GPUs already get that.
NEW FACT | In HBM3e, TSV traversal costs 0.148 pJ/bit per layer and row activation 0.18 pJ/bit, and both stay in place under base-die compute | https://arxiv.org/pdf/2602.18568

IDEA 3: Retrieval-native HBM base die
KILLER | Energy and cost cut per long-context token, beyond what a GPU gets by reading the same 1–2-bit key sketches and then the selected K/V rows. Only the sketch's off-stack crossing is saved. It is true that traffic crossing to the compute die falls 10–50x, but the energy behind it does not | required 10x (the "million-token costs what short costs" claim) | available 1.08x (I/O share 7.3% of HBM3e energy, arXiv 2602.18568) | MARGIN 0.11
CHAIN | GPU-side sketch or indexer top-k (DSA FP8 indexer; HashAttention/Quest-class) plus a sparse attention kernel | now 1.00 | with idea about 0.96 | RATIO 1.04
VERDICT | DEAD | The claimed traffic cut counts interface bits and ignores array and TSV energy. Once on-GPU sparse attention is the baseline, about 1.04x is left for the system.
NEW FACT | The HBM3e figure of 3.44 pJ/bit matches a component model whose I/O term is only 0.25 pJ/bit | https://arxiv.org/pdf/2602.18568

IDEA 4: Optical weight broadcast fabric
KILLER | Optical ingress bandwidth each package needs to receive 15/16 of all expert weights every decode step. At serving batch sizes almost every expert is touched each step. Figures: 671 GB FP8 DeepSeek-class model, 50–85 tok/s/user | required 31–54 TB/s per package | available about 1.8 TB/s per direction (NVLink 6 at 3.6 TB/s bidirectional per Rubin GPU; this is more than Rubin's own 22 TB/s HBM). The 1:16 split adds at least 12 dB of loss, so laser power must rise about 16x or more | MARGIN 0.034–0.057
CHAIN | Wide expert parallelism with disaggregated decode on NVL72. Each GPU already reads only its own 1/N of the experts once per step, and only small token activations go all-to-all | now 1.00 (group HBM weight reads = W per step) | with idea, still W of HBM reads per step plus W×16 optical deliveries | RATIO ≤1.0 (about 0.9 est.)
VERDICT | DEAD | Expert parallelism already reads each weight once per step across the group by moving activations, which are KB per token. Moving weights instead, which are hundreds of GB per step, fails by about 20–30x on bandwidth and saves no HBM reads.
NEW FACT | Rubin: 22 TB/s HBM4 (8×36 GB stacks) and 3.6 TB/s NVLink 6 per GPU | https://blog.barrack.ai/nvidia-rubin-specs-architecture-2026/ ; https://www.guru3d.com/story/nvidia-details-rubin-gpu-architecture-with-hbm4-nvlink-6-and-336-billion-transistors/

How I got the numbers: all margins and ratios are plain arithmetic from the sourced inputs, so nothing was measured by running a benchmark. The 3.44 pJ/bit HBM3e figure is an analytical model from a 2026 paper that says it matches reported HBM3e numbers. Its component terms do not add up to the total, and I found no vendor or JEDEC breakdown, so the I/O share is the least certain input. The "about 0.9" ratio for Idea 4 is my estimate. The calculation script is `/home/user/SomeRepository/engine/runs/meta_ab/gate/c2/gate_calc.py`.

Sources:
- [RPU – A Reasoning Processing Unit (arXiv 2602.18568)](https://arxiv.org/pdf/2602.18568)
- [KAIST PIM-HBM study](https://koasas.kaist.ac.kr/handle/10203/290541)
- [DeepSeek-V3.2 paper](https://arxiv.org/pdf/2512.02556)
- [vLLM DeepSeek-V3.2 blog](https://vllm.ai/blog/2025-09-29-deepseek-v3-2)
- [Barrack.ai Rubin breakdown](https://blog.barrack.ai/nvidia-rubin-specs-architecture-2026/)
- [Guru3D Rubin architecture](https://www.guru3d.com/story/nvidia-details-rubin-gpu-architecture-with-hbm4-nvlink-6-and-336-billion-transistors/)