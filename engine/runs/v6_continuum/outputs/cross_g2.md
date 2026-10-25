Each pair below is turned into one design, with the arithmetic that decides whether A's weak link is removed.

=== IDEAS ===
IDEA 1
NAME: DRAM-bonded N6 pipeline chiplets
MECHANISM: Each ~100 mm² N6 pipeline die keeps only activation and staging SRAM. Weights and KV cache sit in one hybrid-bonded stacked-DRAM layer at the measured 64 Mb/mm² (8 MB/mm²), which gives ~800 MB per die. A 70B pipeline at the same ~112 GB footprint then needs ~140 dies instead of 512 SRAM dies. Bandwidth is ~135 GB/s/Gb (≈0.86 TB/s per die, ≈121 TB/s per model) at 0.66 pJ/bit, still on organic packages. The compiler-managed layer pipelining is unchanged. The low per-die power of N6 SRAM-class logic is what keeps the stack below the thermal wall seen with DRAM on GPUs.
VALUE: Storage density is 3.7× the density the SRAM design needed (17.5 Mb/mm²) and is a measured figure, not one 25% above shipped parts. Even after a 3× vendor markup, delivered $/GB stays far under $1.5k/GB.

IDEA 2
NAME: Thin-stack DRAM-on-N6 decode pipeline
MECHANISM: Each 400 mm² N6 logic chiplet carries a 2-high hybrid-bonded DRAM stack at the measured 64 Mb/mm², not a 4-high stack at 200 Mb/mm². That gives 6.4 GB per chiplet and 25.6 GB and ~27.6 TB/s per package, with DRAM power of 27.6 TB/s × 8 × 0.66 pJ ≈ 146 W. A 1T/32B-active MoE with its KV cache (~800 GB) is layer-pipelined across ~32 such ~600 W packages, and only activations cross package links. Decode is memory-bound, so ~10 PF FP4 per package on mature N6 is enough. The power-saving logic stays the same: no slow tier, and every resident byte is read each step.
VALUE: The design depends only on measured density and energy. Current per package drops from ~2.7 kA to ~0.8 kA through half the stack. Modeled bandwidth per kW is ~46 TB/s/kW, against ~32 for the 4-high design and ~12 for Rubin. The cost is ~6× more logic area, but on a cheaper node.

IDEA 3
NAME: Cheap-node HBM decode tier
MECHANISM: Energy is ~9% of TCO, so this decode-only part competes on capex per TB/s rather than tokens per kW. Decode needs only ~3 PF FP8 to saturate 22 TB/s, so the compute dies move to N6. The design keeps 288 GB of HBM4 and is built at cost. Estimated package cost is ~$16k (HBM ~$12k, N6 logic ~$1.5k, packaging ~$2k), against a ~$45k street Rubin package (also an estimate). Prefill and training stay on HBM or GDDR parts, linked to this tier by KV-cache transfer.
VALUE: Cost per token improves by 1/(0.91/2.8 + 0.09/2) ≈ 2.7×. The 1.5× target holds while the package costs ≤ ~$31k, a ~1.9× margin, though most of that margin is vendor markup avoided rather than physics.