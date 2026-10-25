=== LEDGER ===
KIND: cost
(The cost unit is $ per million output tokens for inference and $ per chip-hour for training, on owner-operated hyperscaler TCO. The shares are my estimates anchored to the sources below, not published splits.)

ARCHETYPE A: GB200/GB300 NVL72 rack, disaggregated prefill/decode serving of an MoE model at about 50 tok/s/user | cost $0.06 per Mtok (MiniMax M2.5/M2.7; H100 is $0.19, so 3.2x higher) at $1.86 per chip-hr (H100 $1.17) | Nvidia claims up to 35x lower cost per Mtok for GB300 versus Hopper. That is a vendor figure.
SHARES: accelerator package (die + HBM) 45% | rack, NVLink, CPU, NICs 20% | facility (shell, power, cooling) 12% | energy 9% | ops labour 3% | other (financing, tax, vendor margin) 11%
LARGEST: accelerator package - a 10x cut of it removes 40.5% of the cost

ARCHETYPE B: Google Ironwood (TPU7x) pod serving, 256-chip inference slice or 9,216-chip pod | cost: no sourced $/Mtok. The only independent anchor is 1 GW capex of about $27B for TPUv7 versus $33B for GB300 and $41B for Vera Rubin. That is about 18% lower than GB300 per GW, but it is a secondhand Morgan Stanley figure. | Google lists no price.
Per-chip specs from the Google Cloud docs: 192 GiB HBM, 7.38 TB/s, 4.6 PFLOPS FP8, 1.2 TB/s ICI.
SHARES: accelerator package 38% | ICI/optical interconnect and rack 18% | facility 15% | energy 11% | ops labour 3% | other 15%
LARGEST: accelerator package - a 10x cut of it removes 34.2% of the cost

ARCHETYPE C: SRAM-resident dataflow serving (Cerebras WSE-3, Groq LPU) of a 70B-class dense model at 300 to 2,500 tok/s/user | cost: no sourced $/Mtok. Sources disagree on which vendor is cheaper, and Cerebras claims up to 6x price-performance. | Priced as an API.
- Cerebras WSE-3 has 44 GB SRAM and 21 PB/s.
- The first-generation Groq LPU has 230 MB SRAM per chip. The Groq 3 LPU is reported at 500 MB and 150 TB/s.
- Groq earlier said it needed 576 LPUs to exceed 300 tok/s on 70B.
- Throughput on Llama 3.3 70B is reported at about 294 to 750 tok/s for Groq and 2,100 to 2,500 tok/s for Cerebras.
- Nvidia–Groq deal: one source says Nvidia acquired Groq technology for $20B in December 2025, while others call it a licence. I did not resolve this.
SHARES: silicon (wafer or many LPUs, because capacity is bought in SRAM bytes) 60% | host, network, rack 15% | facility 8% | energy 8% | ops labour 3% | other 6%
LARGEST: silicon - a 10x cut of it removes 54% of the cost

ARCHETYPE D: frontier training on a GB200 NVL72 cluster, with 1 GW treated as the unit | cost $8.5M per MW-year (Epoch, GB200 NVL72; the earlier DGX H100 model gave $10.8M/MW-yr). That is about $1.0k per MW-hr, or about $1.8 per chip-hr at about 1.8 kW IT per GPU, which matches SemiAnalysis' $1.86. | Reference cloud rental is about $2 to 8 per GPU-hr.
SHARES: accelerator package 42% | scale-up and scale-out network 23% | facility 12% | energy 9% | ops labour 3% | other 11%
LARGEST: accelerator package - a 10x cut of it removes 37.8% of the cost

Cross-archetype findings (the energy share is my arithmetic):
- Energy is only about 9 to 11% of TCO. A pure tokens-per-joule gain therefore moves cost per token less than a gain in capex per token. With about 1.8 kW IT per chip, PUE 1.3 and $0.07/kWh, I get about $0.16/hr against $1.86/hr.
- Capex dominates (about 85%). The 1 GW build is about $23B for H100, $24B for B200, $33B for GB300 and $41B for Vera Rubin, so cost per GW rises each generation. Cost per token falls only because throughput per GW rises faster.
- Racks and servers are about 58 to 63% of 1 GW capex, so the facility plus power is about 40%.
- The Rubin figures are secondary sources: 288 GB HBM4, 50 PFLOPS FP4, two reticle dies, 8 HBM stacks, NVLink 6 at 260 TB/s per rack, NVL144 at 3.6 EFLOPS FP4. I found no reliable per-GPU HBM4 TB/s figure, so it is open.
- Nvidia's "$5M yields $75M token revenue" claim is revenue framing, not cost.
- Pricing vintages differ between SemiAnalysis surveys: $2.21 per GB200 GPU-hr in August 2025 against $1.86 in July 2026.
- I did not find Ironwood power or TDP in any source.

SOURCES:
https://inferencex.semianalysis.com/compare-per-dollar/minimax-m27-gb200-vs-h100/8k-1k
https://inferencex.semianalysis.com/compare-per-dollar/minimax-m27-gb200-vs-gb300/8k-1k
https://blogs.nvidia.com/blog/blackwell-inferencemax-benchmark-results
https://epoch.ai/data-insights/ai-datacenter-cost-breakdown
https://substack.com/@hypertechinvest/note/c-261423177 (Morgan Stanley capex per GW, secondhand)
https://docs.cloud.google.com/tpu/docs/tpu7x
https://www.theregister.com/2025/04/10/googles_7thgen_ironwood_tpus_debut/
https://www.networkworld.com/article/3848394/nvidia-details-its-gpu-cpu-and-system-roadmap-for-the-next-three-years.html
https://newsletter.semianalysis.com/p/cerebras-faster-tokens-please
https://www.spheron.network/blog/groq-lpu-vs-cerebras-wse-cheapest-inference-2026/
https://www.spheron.network/blog/nvidia-groq-3-lpu-explained/
https://www.theregister.com/2024/08/27/cerebras_ai_inference/