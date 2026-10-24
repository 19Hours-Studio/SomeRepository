All four ideas come out DEAD. Idea 3 was measured in code, and the bound was checked against known answers first: the rounding-error variance came out at 0.999 of the exact h²/12, and the bound was confirmed valid on every sample. The other three are exact arithmetic from sourced inputs. The scripts are `idea3_escalation.py` and `gate_calcs.py` in the working directory, and nothing was committed.

=== GATE ===
IDEA 1: In-Memory Attention Key Search
KILLER | Capacity of the ferroelectric CAM needed to hold 4-bit keys for 1M-token decode at a batch of 32 (Llama-70B-class GQA: 80 layers × 8 KV heads × 128 dim) | required 2.6e12 multi-level cells ≈ 26,000 mm² of array, even at a generous 0.01 µm² per 4-bit cell (that is 32 × 41 GB of keys) | available one reticle, about 858 mm², of array with no periphery. Devices are not at that scale: the best measured FeFET CAM is an 8-cell word (arXiv 2203.07948) and 2-bit cells on 28nm described as "preliminary" (DATE 2021). For scale, 6T SRAM co-integrated with FeFET on 28nm is 0.12 µm² per bit (GF/TU Dresden). | MARGIN 0.03
CHAIN | DeepSeek Sparse Attention (FP8 lightning indexer with top-2048 over MLA), 128K decode, batch 32. I counted the CAM's search energy as zero, which favours the idea. | now about 37 MB of HBM traffic per layer per user (indexer 16.8 MB + top-k 1.3 MB + weight share 19 MB) | with idea about 20 MB, so 1.8x less HBM traffic; with HBM at 50% of energy that is 1.29x for the system | RATIO 1.29
VERDICT | DEAD | Keys for one million-token user already fill a full reticle at a cell density no FeFET CAM has shown, and digital sparse attention (DSA) already captures most of the traffic saving.
NEW FACT | DeepSeek V3.2's DSA keeps decode cost roughly flat with context. Reported 128K decode cost fell from about $2.40 to about $0.80 per million tokens against V3.1-Terminus (H800 at $2/GPU-hr); one AMD article gives a conflicting $2.20 to $0.25 | https://blog.dailydoseofds.com/p/deepseek-cracked-the-ol-attention ; https://brewingintelligence.substack.com/p/deepseek-v32-a-technical-deep-dive

IDEA 2: Tokens Travel, Experts Stay
KILLER | Compute rate in the DRAM banks per package, needed to match the incumbent's decode throughput (DeepSeek R1, 37B active, 74 GFLOP per token) | required 306 TFLOP/s per package (4,130 tok/s per GPU × 74 GFLOP; the 4,130 is InferenceX, GB200 NVL72 at 125 tok/s/user) | available 9.6 TFLOP/s (8 stacks × 1.2 TFLOPS for Samsung HBM-PIM, ISSCC'21, where the PIM dies also hold half the capacity: 4 Gb vs 8 Gb). Even if I generously assume FP4 units give 4x more compute, it only reaches 0.13. | MARGIN 0.03
CHAIN | GB200 NVL72 with disaggregated serving and wide EP, DeepSeek R1 FP4 | now $0.125 per million tokens ($1.86 per chip-hr at 4,130 tok/s) | with idea about $0.54 per million tokens (130 tok/s per package at a generous all-in $0.25 per package-hr) | RATIO 0.23
VERDICT | DEAD | Logic built on a DRAM process delivers about 1/30 of the FLOP/s that batched MoE decode needs, so the energy saved per token is lost to a roughly 4x higher cost per token.
NEW FACT | On Samsung's Aquabolt-XL, the 300 MHz PIM dies hold half the capacity of a standard die (4 Gb vs 8 Gb), and the 6 GB stack used 4 PIM dies plus 4 standard dies. That works against "trillion-parameter models in a few packages" | https://blocksandfiles.com/2021/02/17/samung-high-bandwith-memory-ai-chip/
NEW FACT | InferenceX reports DeepSeek R1 FP4 on GB200 NVL72 (Dynamo TRT, MTP, disaggregated) at about 4,130 tok/s per GPU, against 941 on B200, both at 125 tok/s/user | https://inferencex.semianalysis.com/blog/gb200-nvl72-vs-b200-disagg-deepseek-r1-fp4-dynamo-trt

IDEA 3: Error-budgeted escalating numerics
KILLER | Share of tiles that must escalate when the cheap, provable per-tile bound is held to the same kind of bound computed for NVFP4 (measured: K=128 tiles, 3-bit absmax quantization, 20k samples, Gaussian and Student-t(3) activations) | required ≤ 0.125. That is the break-even against NVFP4, assuming a 3-bit tile costs 0.375 and an FP4 tile 0.5 of an FP8 tile. | available 1.00, measured: 100% of tiles break both the NVFP4-level and the FP8-level budget. The 3-bit bound is a median 3.1–4.3x the NVFP4 bound and 16–24x the FP8 bound. Even with a budget 4x looser than NVFP4, 1.5% (Gaussian) and 65% (heavy-tailed) of tiles still escalate (my measurement, idea3_escalation.py) | MARGIN 0.125
CHAIN | NVFP4 or FP8 matmul on Blackwell (2x FP4 throughput relative to FP8) | now 0.5 FP8-tile units with NVFP4, or 1.0 with FP8 | with idea 1.375 units (3-bit pass plus FP8 recompute on every tile). Even with zero escalation the gain over NVFP4 is capped at 1.33x on matmul alone. | RATIO 0.36 against NVFP4, 0.73 against FP8
VERDICT | DEAD | A provable worst-case bound on 3-bit tiles always exceeds an FP4- or FP8-grade budget, so every tile escalates and the chip runs slower than plain NVFP4.

IDEA 4: Optical Weight-Broadcast Fabric
KILLER | Optical ingress bandwidth per chip, which must exceed local HBM bandwidth to "break the per-chip decode bandwidth limit" | required more than 176 Tb/s (Rubin HBM4, about 22 TB/s) | available about 35 Tb/s (8 chiplets × 4.4 Tb/s, Celestial AI Photonic Fabric, HOTI'25). Ayar Labs claims more than 200 Tb/s per package for a future design, but that is an unshipped claim. | MARGIN 0.20
CHAIN | GB200 NVL72 wide-EP decode, which already keeps about one copy of the weights per EP group and amortizes each weight read over the batch | now the weight stream is about 1.4 TB/s per GPU (17% of HBM), roughly 43 W of a ~1,200 W GPU | with idea 15/16 of that 43 W is saved, before counting any optical receive energy, which is at most about 1% of power-linked TCO | RATIO 1.01
VERDICT | DEAD | Optical ingress per chip is 5x below the HBM it claims to beat, and batching plus expert parallelism already amortize weight reads, leaving almost nothing to save.
NEW FACT | Celestial AI's Photonic Fabric chiplet is reported at 4.4 Tb/s (HOTI'25; CB Insights' 14.4 Tb/s is unverified), and Marvell completed its roughly $3.25B acquisition of Celestial AI | https://convergedigest.com/hoti25-celestial-ais-photonic-fabric/ ; https://www.theregister.com/2026/03/03/ayar_labs_500m/
NEW FACT | Ayar Labs TeraPHY is 8 × 256G ports, 2.048 Tb/s full-duplex per chiplet; an Alchip reference design with 8 next-gen chiplets is claimed at more than 200 Tb/s per package | https://www.cbinsights.com/compare/ayar-labs-vs-inorganic-intelligence

A few inputs are my own estimates rather than sourced figures:
- **Idea 1:** the 0.01 µm² FeFET cell area. I found no published FeFET cell area, so I chose a value deliberately below every reported figure to favour the idea.
- **Idea 2:** the $0.25 per package-hour.
- **Idea 4:** the 8 GB of replicated dense/attention weights per GPU, about 70 decode steps/s, and 3.9 pJ/bit for HBM.

None of these changes a verdict at any plausible value.

Sources:
- [InferenceX: GB200 NVL72 vs B200, DeepSeek R1](https://inferencex.semianalysis.com/blog/gb200-nvl72-vs-b200-disagg-deepseek-r1-fp4-dynamo-trt)
- [Blocks and Files: Samsung HBM-PIM](https://blocksandfiles.com/2021/02/17/samung-high-bandwith-memory-ai-chip/)
- [Tom's Hardware mirror: HBM-PIM at 1.2 TFLOPS](https://www.3dtested.com/news/samsung-hbm2-hbm-pim-memory-tflops)
- [arXiv 2203.07948: single-FeFET CAM](https://arxiv.org/pdf/2203.07948)
- [DATE 2021: FeFET MCAM on 28nm](https://past.date-conference.com/proceedings-archive/2021/pdf/1285.pdf)
- [TU Dresden: 28nm HKMG FeFET eNVM](https://fis.tu-dresden.de/portal/en/publications/a-28nm-hkmg-super-low-power-embedded-nvm-technology-based-on-ferroelectric-fets(07d5b1f3-b4f1-4c3c-ba75-5d7aa0497146).html)
- [Daily Dose of DS: DSA](https://blog.dailydoseofds.com/p/deepseek-cracked-the-ol-attention)
- [Brewing Intelligence: DeepSeek V3.2](https://brewingintelligence.substack.com/p/deepseek-v32-a-technical-deep-dive)
- [AMD: MI355X and V3.2-Exp](https://www.amd.com/en/developer/resources/technical-articles/2025/amd-instinct-mi335x-gpu-supports-deepseek-v3-2-exp.html)
- [Converge Digest: HOTI25 Celestial AI](https://convergedigest.com/hoti25-celestial-ais-photonic-fabric/)
- [The Register: Ayar Labs](https://www.theregister.com/2026/03/03/ayar_labs_500m/)
- [CB Insights: Ayar vs Celestial](https://www.cbinsights.com/compare/ayar-labs-vs-inorganic-intelligence)