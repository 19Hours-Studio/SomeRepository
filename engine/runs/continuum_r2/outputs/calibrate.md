=== CALIBRATION ===

P | 2 | 22% | It is the most complete standalone architecture: no HBM or CoWoS, all weights resident, stage-local all-to-all. But its whole-chain gain is only about 1.05× once prefill GPUs are counted, and the LPDDR drain argument fails at its own 200–400 tok/s target.

P | 1 | 18% | Its arithmetic holds (790 GB, 117 GB, cost ratios). However, the gain shrinks to 1.06× against NVL72, falls below 1× against Cerebras above 1,000 tok/s, and it needs four SRAM layers under a ~900 W die that only Nvidia can build.

P | 4 | 8% | The ridge and tile-buffer analysis is sound. But the CPX comparison is a straw man, and with 2026 LPDDR prices the BOM is about 0.83×. Rubin CPX already ships this concept.

P | 3 | 7% | It concedes no bandwidth or energy gain. Rubin+Vera with HiSparse already provides the same tier, and memory cost alone exceeds the baseline's cost per slot. It also contradicts Idea 2's "no HBM" definition.

P | none | 45% | No candidate clears 1.5× against best practice (ratios 0.9–1.06), and each covers only part of the required scope. "Best in the world" is unsupported by any of them.

WEAKEST LINK: Idea 2's per-die KV bandwidth. At $0.095/M it needs about 330–360 GB/s of LPDDR per die, which is a 512-bit bus. That bus must fit in under 170 mm² left over after 691 mm² of SRAM, alongside the compute and SerDes. Even then, LPDDR is 2.2–4.5× short of the required drain time at 200–400 tok/s per user.

FLIP TEST: Floorplan the 858 mm² die and run a cycle-level simulation of 128K-context DSA decode at 200 and 400 tok/s per user on the 527-die system. Include the prefill GPUs, using the measured prefix-cache hit rate. | Idea 2 loses the lead if both of these hold: the 512-bit PHY plus compute cannot fit, or the simulated rate falls below about 1.1× Rubin NVL72 whole-chain cost per token at 200 tok/s. Then Idea 1 leads, or "none" exceeds 55%. If instead the simulation holds at least 1.3× whole-chain cost per token, Idea 2 rises to about 40%.

UNKNOWN: Even if Idea 2 is right, two things are unclear. First, whether sparse-attention MoE models of the DeepSeek-V3.2 class stay the dominant workload long enough to amortize a 527-die design tuned to one sparsity pattern. Second, what LPDDR and HBM prices will be in 2027, since every cost ratio here moves by roughly ±30% with them.