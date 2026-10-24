=== REVIEW ===
IDEA 1: Continuum-D: SRAM experts, LPDDR sparse-KV
DEFECT | MAJOR | The "decode-only" $/token leaves out the prefill GPUs. By the design's own figure of 1.5 GB/s of KV writes per die, those GPUs cost far more than the Continuum-D system they feed, so the 1.34–1.44× decode saving shrinks to almost nothing on the whole chain. | 527 dies × 1.5 GB/s = 790 GB/s of KV ÷ 48 KB/token ((132+656) B × 61 layers) = 16.4M prefill tok/s. At 76.5k tok/s per Rubin (Idea 4) that is about 215 Rubins × ~$108k ($7.8M per rack ÷ 72) ≈ $23M, against $1.44M of decode hardware. Whole-chain ratio is (23.2+2.0)/(23.2+1.44) = 1.02, or 1.15 with a 90% prefix-cache hit rate.
DEFECT | MAJOR | The drain-time argument for choosing LPDDR over HBM only holds at 100 tok/s per user. At the 200–400 tok/s where the value is claimed, the required drain time drops to the point where HBM4 is the matched memory and LPDDR is 2.2–4.5× short on bandwidth. | Required drain = 6.30 GB per user ÷ 1.137 GB per step ÷ tok/s. That gives 55.4 ms at 100, 27.7 ms at 200, 13.8 ms at 400 (HBM4 is 13.1 ms) and 5.5 ms at 1,000, against LPDDR's 62 ms (python check).
DEFECT | MAJOR | Every die needs a wide LPDDR bus, on a die that is already about 80% SRAM. This is not costed or floor-planned. If KV sits only on the "+1" die of each stage, the bandwidth cannot be built at all. | $0.095/M tokens with a 4-year life, 100–160 kW and $0.10/kWh implies about 150–170k tok/s × 1.137 GB = 170–190 TB/s. That is about 330–360 GB/s per die over 527 dies (a 512-bit LPDDR5X-class bus, like M4 Max), or about 3 TB/s per die if only 61 dies hold KV. The SRAM alone takes 691 mm² per die (36 × 44.0 MB × 436 mm²/GB), leaving under 170 mm² of an 858 mm² reticle for compute, PHYs and SerDes.
DEFECT | MINOR | "55% of N3E bitcell density" does not give 436 mm²/GB. The number is really about 39–41% of bitcell density. It is a conservative figure but mislabeled. | Bitcell 0.021 µm² → 168 mm² per GB (180 per GiB) → 305–328 mm² at 55%. 258/436 = 0.59.
DEFECT | MINOR | All-in cost per die is an assumption, not sourced, and the memory market is tightening. | $1.44M ÷ 527 = $2,732 per die for an N3E reticle die plus package, LPDDR, board, network and power. LPDDR5X contract prices roughly doubled in H1 2026.
SURVIVES | Die count of 527 (58 × 9 + 5) and 36 experts × 44.0 MB = 1.59 GB per die reproduce. KV of 6.30 GB per user and 1.137 GB per step at 128K reproduce. Rubin drain of 13.1 ms reproduces.
RATIO | 1.05 | Whole-chain cost (prefill GPUs plus decode) with the decode gain kept at 1.39×; range 1.02–1.15 depending on prefix-cache hit rate.
KNOWN | partly | Nvidia Groq 3 LPX (256 SRAM LPUs, 128 GB per rack, decode-only next to Vera Rubin, which does prefill), in full production in 2026 (theregister.com/2026/03/16/nvidia_lpx_groq_3/); Cerebras WSE-3.
NEW FACT | Groq 3 LPU: 500 MB SRAM and 1.2 PF FP8 per chip; 256 per rack. A 671B FP8 model needs about 1,342 LPUs (about 5.2 racks). | https://www.theregister.com/2026/03/16/nvidia_lpx_groq_3/
NEW FACT | Vera Rubin rack estimated at $7.8M, about $2M of it memory; HBM4 about $17–18.4/GB (UBS/BofA estimates) | https://wccftech.com/nvidia-vera-rubin-rack-hit-with-memory-price-surge-pushing-hbm4-lpddr5x-bill-to-2m-of-7-8m-total/

IDEA 2: Touch-rate-split DSA KV tier
DEFECT | MAJOR | The baseline already has the same tier. Vera gives each Rubin about 750 GB of LPDDR5X at about 0.6 TB/s, over a 0.9 TB/s C2C share, and HiSparse already keeps indexer and hot data on the GPU with latents in host memory. So the claimed "1.9× users per HBM stack when hit ≤0.4" has no mechanism behind it. | At hit 0.4, miss traffic for 74 users is 364 GB/s, which is below Vera's per-GPU share of about 0.6 TB/s. Users per stack limited by the indexer scan are the same for both: 2.75 TB/s ÷ 105.5 GB/s ≈ 26.
DEFECT | MAJOR | The cost per slot cannot cover the die's own memory at 2026 prices. | 74 × $86–100 = $6.4–7.4k per die. Memory alone is 512 GB LPDDR × ~$12/GB = $6.1k plus 144 GB HBM4 × ~$17/GB = $2.5k, so at least $116 per slot before any silicon (against $102 for the baseline).
DEFECT | MAJOR | It uses the name "Continuum-D" for a die with 4 HBM4 stacks, while Idea 1's Continuum-D is defined as having no HBM. The two tiers cannot both be the architecture. | Idea 1 says "no HBM and no CoWoS"; Idea 2 says "4 HBM4 stacks".
DEFECT | MINOR | The headline ratios do not reproduce from the stated numbers. | 18.4/5.0 = 3.68×, not 3.9×. $102 ÷ $86–100 = 1.02–1.19×, not "1.0× to 1.0×".
DEFECT | MINOR | The "touch rate matches HBM" argument assumes one token per step. With MTP speculative decoding the indexer touch rate falls below HBM's ratio, so indexer keys become capacity-bound, not bandwidth-bound. | At 100 tok/s and about 1.8 accepted tokens per step, the touch rate is 55.6/s against HBM's 76.4/s.
DEFECT | MINOR | The 79 GB/s miss traffic is the figure at hit ≈ 0.87, not at 0.4. LPDDR bandwidth actually has headroom down to hit = 0, so the 0.4 limit must come from latency alone, and that is unshown. | 606 GB/s × (1 − hit): 79 GB/s at 0.87, 364 at 0.4, 606 at 0 (all below 700).
SURVIVES | 1.055 and 1.137 GB per step, 82 MB of latent per step, 164 µs × 61 = 10.0 ms, and 74 users × 105.5 GB/s = 1.95 TB/s per stack all reproduce. The "no bandwidth or energy gain" concession is correct.
RATIO | 1.0 | Same mechanism and roughly the same LPDDR bandwidth and capacity as Rubin+Vera with HiSparse; at 2026 memory prices it is ≤1.0.
KNOWN | yes | SGLang HiSparse, April 2026 (lmsys.org/blog/2026-04-10-sglang-hisparse); ESS latent-cache offload for V3.2-Exp (arxiv.org/abs/2512.10576).
NEW FACT | HiSparse: over 3× throughput at 256 concurrent requests for GLM-5.1-FP8 on 8×H200; only runs in prefill/decode-disaggregated mode | https://www.lmsys.org/blog/2026-04-10-sglang-hisparse
NEW FACT | Vera: up to 1.5 TB LPDDR5X, about 1.2 TB/s, 1.8 TB/s NVLink-C2C shared by 2 Rubins (secondary sources) | https://www.naddod.com/ar/ai-insights/nvidia-rubin-platform-ai-supercomputer-with-six-new-chips

IDEA 3: Node-scale expert-stationary SRAM stacks
DEFECT | MAJOR | The gain only exists against a deliberately weak baseline (an isolated 8-GPU node). A competent operator chasing 500–800+ tok/s per user would use NVL72 (their own figure: 1.06×) or an SRAM system that already exceeds 1,000 tok/s on this exact model. | Weight read per step on NVL72 is 63 GB ÷ 72 ÷ 22 TB/s = 0.04 ms. Cerebras serves gpt-oss-120b at about 1,700 (AA) to 2,700 (vendor) tok/s; the best 8×GB200 result is 650 tok/s.
DEFECT | MAJOR | The 1.39× and 1.86× gains need an effective weight-read time of about 0.57 ms per step. At Rubin's 22 TB/s with all experts touched it is 0.36 ms, and at small batch fewer experts are touched. | T/(T−W): with W = 0.36 the gain is 1.21× at 500 and 1.39× at 800; W = 0.57 is needed to get 1.40/1.84. Top-4 of 128 experts at batch 16 touches only 40% of experts.
DEFECT | MAJOR | Neither the risk nor the NRE of this design is counted. It puts four hybrid-bonded SRAM layers under a roughly 900 W Rubin-class compute die, so all power and HBM I/O must pass through four TSV layers. It also needs a custom Rubin-class die that only Nvidia can build. | Closest precedent is AMD's single 64 MB layer under a 120 W CCD (9800X3D). The $24k adder covers only about 51,000 mm² of N5 (about 1 wafer at 100% yield, before stack yield and bonding).
DEFECT | MINOR | The margins are slightly off for real checkpoint sizes. | 117/65.3 GB (gpt-oss-120b actual) = 1.79. 790/594 GB (K2 native INT4) = 1.33.
SURVIVES | 790 GB per rack and 117 GB per node reproduce at about 800 mm² × 2.29 MB/mm². 790/377 = 2.10 (claimed 2.15). Cost ratios of 1.41–1.88 follow from the stated $/M figures.
RATIO | 1.06 | Against NVL72, the best GPU practice for a 120B MoE at high tok/s per user; below 1 against Cerebras above 1,000 tok/s per user.
KNOWN | partly | AMD 3D V-Cache (SRAM hybrid-bonded under logic); Cerebras/Groq LPX for SRAM-resident weights; HGX Rubin NVL8 exists as the node baseline.
NEW FACT | Fastest GPU result on gpt-oss-120b: 650 tok/s on 8×GB200 (Baseten, as cited by Cerebras); most providers run at 100–300 tok/s | https://www.cerebras.ai/blog/blackwell-vs-cerebras

IDEA 4: SRAM-tiled LPDDR prefill die
DEFECT | MAJOR | The CPX comparison is a straw man. Prefill across Rubin CPX can use pipeline parallelism instead of expert parallelism, and then the NIC is nowhere near the limit, so CPX is compute-bound rather than "network-bound at 30k tok/s". | PP activation traffic at 30k tok/s is 7,168 × 2 B × 30k = 0.43 GB/s, against a 200 GB/s NIC. At 457 GF/token, CPX (30 PF) is compute-bound at 65.6k tok/s, which is 0.86× this package with one die and no HBM.
DEFECT | MAJOR | The BOM leaves out the 2026 LPDDR price rise. The 512 GB of LPDDR alone costs more than Rubin's HBM, and the 2027 "1.6×" assumes HBM rises 121% while LPDDR stays flat. | 512 GB × ~$12/GB = $6.1k, which is 70% of the claimed $8.8k package BOM, against $4.9k of HBM4 in Rubin (UBS). That makes the BOM about $10.5k, or $137 per ktok/s (0.83× in 2026). In 2027 it is 1.39× with LPDDR flat and 1.07× with LPDDR +50%.
DEFECT | MAJOR | The memory bandwidth contradicts Idea 2. A die needs 1.4 TB/s from LPDDR6 (about a 1,050-bit bus per die, about 2,100 bits per package), while Idea 2 says the same 512 GB in 4 modules gives 0.7 TB/s, which is 4× less per package. | 1.4e12 × 8 ÷ 10.667 Gb/s ≈ 1,050 bits. At 0.7 TB/s per package the ridge is 50,000 FLOP/B, and a 128K DSA pass needs about 108K tokens.
DEFECT | MINOR | The 76.5k tok/s figure implies dense attention at 128K, not the DSA models the other ideas target. With DSA the FLOPs per token fall 2.6×, so tiles must grow by the same factor. | 35 PF ÷ 76.5k = 457 GF/token. V3.2 DSA prefill is about 174 GF/token (74 GF from MoE plus 100 GF from indexer and sparse attention).
DEFECT | MINOR | The minimum of 64K tokens per pass adds 0.84 s or more of time-to-first-token for short prompts. That is a real penalty under interactive SLOs. | 64K ÷ 76.5k tok/s = 0.84 s.
SURVIVES | Ridge of 12,500, the 34% figure (4,096/12,500), NVFP4 size of 377 GB, KV rate of 1.84 GB/s per die, 1.82 kW power (23.8 mJ × 76.5k), and the $187/$115 = 1.63 arithmetic all reproduce.
RATIO | 0.9 | Corrected 2026 BOM (0.83) up to a 2027 asymmetric-HBM case (1.07–1.39), against CPX with pipeline parallelism or Rubin.
KNOWN | yes | Nvidia Rubin CPX: a prefill part with no HBM, 128 GB GDDR7 and 30 PF NVFP4 in the NVL144 CPX rack, shipping late 2026 (guru3d.com/story/nvidia-rubin-cpx-gpu-announced-at-ai-infra-summit-2025/).
NEW FACT | LPDDR5X contract price for a 12 GB part went from $77 to about $146 in Q2 2026 (+89% quarter on quarter), about $12/GB | https://www.softwareseni.com/dram-prices-in-2026-have-doubled-and-the-numbers-are-getting-worse/
NEW FACT | TrendForce: HBM prices projected to rise 121% in 2027 | https://www.inside.com.tw/article/42684-nvidia-rubin-12-layer-hbm4-trendforce-2027-hbm-price

Ranking, weakest to strongest: Idea 2 (already ships as software, ≤1.0×), then Idea 4 (≤1.0× in 2026; CPX already exists), then Idea 3 (1.06× against the real baseline), then Idea 1 (1.05× whole-chain, but it is the only one with a structural decode-side advantage).

Sources:
- https://www.theregister.com/2026/03/16/nvidia_lpx_groq_3/
- https://wccftech.com/nvidia-vera-rubin-rack-hit-with-memory-price-surge-pushing-hbm4-lpddr5x-bill-to-2m-of-7-8m-total/
- https://letsdatascience.com/news/nvidia-vera-rubin-memory-costs-dominate-superchip-bom-1c630dcd
- https://www.lmsys.org/blog/2026-04-10-sglang-hisparse
- https://arxiv.org/html/2512.10576v1
- https://www.naddod.com/ar/ai-insights/nvidia-rubin-platform-ai-supercomputer-with-six-new-chips
- https://www.cerebras.ai/blog/blackwell-vs-cerebras
- https://www.spheron.network/blog/groq-lpu-vs-cerebras-wse-cheapest-inference-2026/
- https://www.guru3d.com/story/nvidia-rubin-cpx-gpu-announced-at-ai-infra-summit-2025/
- https://www.softwareseni.com/dram-prices-in-2026-have-doubled-and-the-numbers-are-getting-worse/
- https://www.inside.com.tw/article/42684-nvidia-rubin-12-layer-hbm4-trendforce-2027-hbm-price