Fixing the weak links brings all three ideas below their original claims. Idea 1 gets cheaper per token than SRAM-chip list prices but loses the "GB300 cost at 20× the speed" claim. Idea 2 works only for high per-user speeds. Idea 3 cannot reach 1.5×, so it is reduced to its smallest honest version. All numbers are modelled; nothing is measured on silicon.

=== IDEAS ===
IDEA 1
NAME: N6 SRAM chiplets, package-wide tensor stages
MECHANISM: Weights and KV cache for Llama-3.3-70B are stored in NVFP4 (4.5 bits) and live entirely in SRAM on 100 mm² N6 chiplets, 32 per organic package. The fix has two parts. First, each die is sized to the measured 14.2 Mb/mm² of AMD's V-Cache die, not 17.5. A die has 70 mm² of SRAM (124 MB) and 30 mm² of logic, which gives 22.7 TF FP8 at A100's whole-die 0.755 TOPS/mm² on N7. Second, layers are no longer pipelined die by die, which had halved per-user speed in the last check. Each package is instead one tensor-parallel stage across its 32 dies. For 32 users at 8K context the model needs 67 GB, which is 544 dies in 17 stages running 16 micro-batches. Each stage takes 37.7 µs of compute plus 11.4 µs of collectives, assuming a 1 µs all-reduce across 32 dies, which still needs a simulator. That gives 1,198 tok/s/user, or 916 at 50% MAC efficiency. Full cost of ownership (2× vendor markup, host and network, facility, energy, 60% utilisation) comes to $0.23/Mtok with $7.5k package overhead, or $0.14 with $3k.
VALUE: At measured SRAM density it serves 70B at about 1,000–1,200 tok/s/user for about $0.14–0.23/Mtok. That is 2.6–5.6× below the Groq ($0.79) and Cerebras ($0.60–1.20) list prices, which include their margins, and capex per GB of SRAM is 13× below CS-3. The "GB300 cost at 20× speed" claim is dropped: this costs 2–4× more per token than GB300 at 50 tok/s, and it is slower per user than Cerebras (2,100–2,500 tok/s).

IDEA 2
NAME: Measured-density DRAM-on-logic for interactive decode
MECHANISM: Four 400 mm² N2 logic chiplets sit on top, each hybrid-bonded onto a 4-layer custom DRAM stack, with no HBM. The fix sizes the DRAM at 64 Mb/mm², the only measured density for hybrid-bonded logic-to-DRAM (ISSCC 2022), so no density is assumed above measurement. Power reaches the logic at 1.8 V through the DRAM stack and is stepped down by on-die regulators at 90% efficiency. That cuts the current from 433 A to 201 A per chiplet, so power TSVs take 4.5% of each DRAM layer instead of 9.7%. The package holds 48 GB at 44 TB/s, which needs 114 GB/s per Gb against 135 measured (margin 1.18). Access energy is the measured 0.88 pJ/bit, with 1.5 pJ/bit as a stress case. Capacity per package is small, so the part only pays off where bandwidth ÷ capacity is about 914 tok/s/user and is offered only for that tier. On a 1T-total/32B-active GQA MoE, against Rubin (288 GB, 22 TB/s, HBM at 3.44–5.74 pJ/bit), it gets 1.2–1.9× the tokens/s per kW at 400 tok/s/user and 1.8–4.3× at 1,000 tok/s/user (2.2–2.6× per package), at both 8K and 128K. At 100 tok/s/user it runs out of capacity and gets only 0.39–0.60× Rubin's tokens/s per kW.
VALUE: Modelled decode tokens per kW are about 2–4× Rubin at ≥1,000 tok/s/user and 1.2–1.9× at 400, with package draw of 0.6–1.7 kW. This is the smallest honest version: a part for fast per-user serving that loses about 2× to Rubin for bulk serving at ≤100 tok/s/user. A 4-layer stack at this density has not been demonstrated.

IDEA 3
NAME: Bandwidth-sized HBM4 decode part (smallest honest)
MECHANISM: Prefill and training stay on Rubin or Rubin CPX. Decode moves to a part priced for memory bandwidth rather than FLOPS, keeping Rubin's 8 HBM4 stacks and 22 TB/s, which use proven supply. Three things are cut. The stacks are 8-high (192 GB, not 288 GB), because the capacity decode needs is about bandwidth ÷ per-user rate plus the weight share: 81 GB at 128K and 300 tok/s/user. Compute drops to 5 PF FP8, against the 3–4 PF needed. Scale-up drops to 1.2 TB/s, since the MoE all-to-all needs about 0.6 TB/s. The weak link is handled by moving the claim from tokens per kW to cost per token, because energy is only 6% of cost of ownership. The cost inputs are HBM4 at $18.4/GB, a $55k Rubin and a $7.8M rack. On a full cost-of-ownership model the part is 1.19–1.24× cheaper per token than Rubin NVL72 at ≥300 tok/s/user, at 8K and 128K. Decode draw falls from 1.64 kW to 1.34 kW. At 100 tok/s/user the gain is only 1.00–1.04×, because 192 GB runs out of capacity.
VALUE: About 1.2× lower cost per decode token than Rubin NVL72 at ≥300 tok/s/user, and 1.5× more decode packages per HBM wafer while HBM is sold out. The weak link cannot be fixed to 1.5×: the rest of the cost is vendor price and rack, not physics. This is the smallest honest version, and it gives up training and the lowest-latency tier.

=== NOTES ===
IDEA 1: What changed: measured SRAM density (124 MB per die); each package is one tensor-parallel stage instead of die-level pipelining; the deciding metric is now full $/Mtok. New deciding number: $0.14–0.23/Mtok at 1,198 tok/s/user. Sources: FACT 1 (V-Cache density), A100 datasheet (624 TOPS on 826 mm²), FACT 17 (list prices), FACT 2/11 (CS-3 price). Assumptions:
- the 1 µs all-reduce;
- $12k per N6 wafer (4nm is about $18–20k, per Morgan Stanley via guru3d);
- package overhead;
- 25 W per die.

IDEA 2: What changed: DRAM at the measured 64 Mb/mm² (48 GB per package); 1.8 V supply with on-die regulators; served only at ≥400 tok/s/user. New deciding number: 1.8–4.3× Rubin's tokens/s per kW at 1,000 tok/s/user and 1.2–1.9× at 400, with a bandwidth-per-Gb margin of 1.18. Sources: FACT 14, FACT 8, FACT 12, FACT 13, FACT 10 (KV shape). I searched for the layer count of UniIC's VLSI 2023 stack and found none published. TSV current limit, compute energy (0.15 pJ/FLOP) and idle power are assumptions.

IDEA 3: What changed: HBM4 instead of stacked DRAM, 8-high stacks, less compute and scale-up, and the claim moved from tokens per kW to cost per token. New deciding number: 1.19–1.24× lower cost per token at ≥300 tok/s/user. Sources: Morgan Stanley estimates (Rubin $55k, rack $7.8M, HBM4 $382k per rack) via [digitalcitizen.life](https://www.digitalcitizen.life/nvidias-vera-rubin-ai-rack-may-cost-7-8-million-as-memory-prices-surge/) and [wccftech](https://wccftech.com/nvidia-vera-rubin-rack-hit-with-memory-price-surge-pushing-hbm4-lpddr5x-bill-to-2m-of-7-8m-total/amp/); FACT 12, FACT 13. The 40% share of rack cost that scales with scale-up bandwidth and the $700 logic cost saving are assumptions.

Files are in `/home/user/SomeRepository/engine/runs/v6_continuum/improve_g2/`:
- answer.md
- improve_calc.py
- improve_calc.out

Nothing was committed.

Sources: [UniIC VLSI 2023 (chinaflashmarket)](https://chinaflashmarket.com/a/179680) · [TSMC wafer pricing (guru3d)](https://www.guru3d.com/story/wafer-pricing-adjustments-by-tsmc-in-2025-rise/) · [Rubin rack/HBM4 cost (digitalcitizen.life)](https://www.digitalcitizen.life/nvidia-vera-rubin-rack-pricing-could-climb-as-hbm4-memory-costs-surge/)