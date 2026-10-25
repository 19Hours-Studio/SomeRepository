=== GATE ===
IDEA 1: Measured-density DRAM-on-logic for interactive decode
KILLER | DRAM bandwidth per Gb at 64 Mb/mm², 4 layers (48.9 GB of capacity must deliver 44 TB/s) | required 112–114 GB/s/Gb | available 135 GB/s/Gb (UniIC, VLSI 2023, reported only in Chinese trade press, chinaflashmarket.com/a/179680). That chip's areal density is not published, and the 64 Mb/mm² comes from a different chip (Alibaba, ISSCC 2022), so the two numbers are combined across papers | MARGIN 1.2
CHAIN | Rubin NVL144-class serving of a 1T-total/32B-active MoE at 1,000 tok/s/user (1 ms step), with weights spread over 72 packages. With 24 packages Rubin cannot reach a 1 ms step at all | now 1.0 (Rubin TCO per token, ledger A shares, $45k package) | with idea 0.33–0.56 (roofline 1.7–2.9× tok/s per package; $16k package at 2× markup; facility and energy scaled by 1.2/2.3 kW) | RATIO 1.8–3.0. It is 3.6–6 if built at cost, but that gain is avoided markup, not physics
VERDICT | ALIVE | The numbers hold by my roofline, but the margin is only 1.2. It rests on one trade-press bandwidth figure paired with a density from a different chip, and the 4-layer stack at 64 Mb/mm² has not been built, so this is fragile.
NEW FACT | The first-generation SeDRAM platform offers 64 MB–8 GB at up to 34 GB/s/Gb and 0.88 pJ/bit | https://xmcwh.com/en/site/details/300?details=1
NEW FACT | The Alibaba ISSCC 2022 logic-to-DRAM system's bandwidth is reported secondhand as 1.38 TB/s; total capacity is not published | https://semiconductor-digest.com/?p=22931
IDEA 2: Cheap-node HBM decode tier
KILLER | The package cost needed for a 1.5× cut in cost per token over the whole TCO, using ledger A shares (package 45%, everything else unchanged) | required ≤ $11.7k per package | available ≈ $7.9k (8 × ~$550 per HBM4 12-high stack per TrendForce/Chosun, plus the idea's own $1.5k logic and $2k packaging) | MARGIN 1.48
CHAIN | GB300/Rubin bought from Nvidia (ledger A). The idea's 2.7× formula wrongly applies the package saving to 91% of TCO | now 1.0 | with idea 0.63–0.65 | RATIO 1.55–1.59 against Nvidia street price, but only ~1.15 against an at-cost hyperscaler ASIC such as Ironwood (assumed ~$12k package), which a competent practitioner would also count
VERDICT | WOUNDED | It works only by avoiding a vendor's margin. Against TPU-style in-house silicon the gain falls to about 1.15×, and the claimed 2.7× is an accounting error.
NEW FACT | HBM4 12-high is priced to Nvidia at about the mid-$500s per stack, 60–70% above HBM3E (~$300s) | https://www.tweaktown.com/news/106826/sk-hynix-drastically-raises-next-gen-hbm4-supply-price-in-a-war-of-nerves-with-nvidia/index.html ; https://www.trendforce.com/news/?p=49113
IDEA 3: N6 SRAM chiplets, package-wide tensor stages
KILLER | All-reduce latency across 32 dies on an organic package, with about 9.4 all-reduces per stage | required ≤ 1.2 µs each for 1,198 tok/s/user | available is not measured; ~0.4–1 µs is my estimate from UCIe-class hop latency on a 6×6 mesh and needs a simulator. Even at 5 µs (NVLink-class), my arithmetic gives 694 tok/s/user, which is still in Groq's 294–750 tier | MARGIN ~1 (estimated; above 0.5 even in the worst case I checked)
CHAIN | Groq/Cerebras API serving of Llama-3.3-70B at list price | now $0.60–0.79/Mtok (FACT 17) | with idea $0.16–0.21/Mtok (my recompute: a 100 mm² N6 die costs ~$17 at an assumed ~$10k per wafer; 2× markup, silicon at 60% of TCO, 60% utilisation, 4-year life) | RATIO 2.9–3.8 (wafer price is an assumption: I found no published N6 wafer price)
VERDICT | ALIVE | The cost win holds even if per-user speed falls to Groq levels. It is still 2–4× more expensive per token than GB300 at 50 tok/s and slower than Cerebras, as the idea itself says.
NEW FACT | TSMC N2 wafers are reported at ~$30k; I found no published N6/N7 wafer price | https://technode.com/2025/10/09/tsmc-sets-2nm-wafer-price-at-30000-far-below-earlier-50-increase-speculation/
IDEA 4: DRAM-bonded N6 pipeline chiplets
KILLER | Per-user decode rate when each layer is pipelined die by die: one token must read 39.7 GB of NVFP4 weights in sequence at 0.864 TB/s per die | required ≥ 300 tok/s/user (the SRAM tier it replaces; Groq does 294+) | available 22 tok/s/user (from the idea's own 135 GB/s/Gb × 6.4 Gb per die) | MARGIN 0.07
CHAIN | B200/GB200-class GPU serving 70B NVFP4 at batch ~96, 8K context, 50% bandwidth efficiency, $1.86 per GPU-hr | now ~$0.25/Mtok | with idea ~$1.09/Mtok (KV capacity limits it to ~96 users × 22 tok/s ≈ 2.1k tok/s on 140 dies) | RATIO 0.23
VERDICT | DEAD | Higher storage density does not fix sequential bandwidth. Die-by-die pipelining gives about 22 tok/s/user, slower than a single GPU, and costs about 4× more per token.
NEW FACT | none beyond the above | —

I wrote the arithmetic to `gate.py`, its output to `gate_out.txt` and a summary to `gate.md` in the working directory. I committed nothing.

Sources:
- [chinaflashmarket: UniIC VLSI 2023](https://chinaflashmarket.com/a/179680)
- [XMC SeDRAM platform](https://xmcwh.com/en/site/details/300?details=1)
- [Semiconductor Digest: Alibaba ISSCC 2022](https://semiconductor-digest.com/?p=22931)
- [TweakTown: HBM4 price](https://www.tweaktown.com/news/106826/sk-hynix-drastically-raises-next-gen-hbm4-supply-price-in-a-war-of-nerves-with-nvidia/index.html)
- [TrendForce: HBM4 pricing](https://www.trendforce.com/news/?p=49113)
- [TechNode: TSMC 2nm wafer price](https://technode.com/2025/10/09/tsmc-sets-2nm-wafer-price-at-30000-far-below-earlier-50-increase-speculation/)
IDEA 5: Bandwidth-sized HBM4 decode part (smallest honest)
KILLER | Cut in package price that a 192 GB, 5 PF, 1.2 TB/s part gets against a $55k Rubin. The 22 TB/s stays, so decode tok/s per package is unchanged and every gain must come from cost. | required 24% package-price cut to reach the claimed 1.2× (ledger A shares: package 45%; the rack, facility and energy savings from 1.64→1.34 kW cover only the rest of the 16.7% TCO cut) | available 6% if the vendor price falls only by the BOM saved (96 GB × ~$16/GB HBM4 ≈ $1.5k, plus about $2k of compute and CoWoS silicon). It is 35% only if the price scales with the BOM at constant margin (HBM4 ~$2/Gb ≈ $16/GB, DigiTimes via siliconanalysts.com/market-data/hbm-pricing; the BOM split is my estimate). The capacity check passes: 22 TB/s ÷ 300 tok/s = 73 GB + 7.6 GB = 81 GB against 192 GB, a 2.4× margin, using exact arithmetic. | MARGIN 0.25–1.45 (≈0.6 central; it depends on vendor margin, not physics)
CHAIN | Rubin NVL72 disaggregated decode at ≥300 tok/s/user, full TCO (ledger A) | now 1.00 (normalised $/Mtok) | with idea 0.91–0.78 | RATIO 1.10–1.28 (the idea itself claims 1.19–1.24; ≈1.00 at 100 tok/s/user because of capacity)
VERDICT | WOUNDED | The physics holds (2.4× capacity headroom, and the bandwidth is unchanged), but the gain is capped below 1.5× by its own numbers. Whether it even reaches 1.2× depends on Nvidia or an ASIC vendor passing the BOM savings into the price, which no engineering choice controls.
NEW FACT | HBM4 is ~$2.00/Gb (≈$16/GB) for H2 2026 per DigiTimes. Per-stack estimates are ~$10/GB, and revenue-implied figures are ~$14–15.5/GB. Sources differ by about 1.7×. | https://siliconanalysts.com/market-data/hbm-pricing ; https://siliconanalysts.com/data/hbm-pricing/methodology
IDEA 6: Thin-stack DRAM-on-N6 decode pipeline
KILLER | Hybrid-bonded logic-to-DRAM bandwidth per mm² | required 17.2 GB/s/mm² (27.6 TB/s ÷ 4 chiplets ÷ 400 mm²) | available 2.29 GB/s/mm² measured (Alibaba ISSCC 2022 64 Mb/mm² hybrid-bond chip: 1.38 TB/s system bandwidth on 602.22 mm², from secondary reports at monolithic3d.com/blog/archives/03-2022 and theregister.com/2021/12/08/alibaba_teases_a_breakthrough_chip). I checked that 64 Mb/mm² × 400 mm² × 2 layers = 6.4 GB, which matches the idea. | MARGIN 0.13
CHAIN | Rubin NVL72 decode of a 1T/32B MoE (384 experts, top-8, 61 layers) at 8K context, measured in tok/s per kW | now ≈28,400 tok/s/kW (72 × 22 TB/s, 288 GB, 2.3 kW each; batch limited by capacity → 0.34 GB read per token) | with idea ≈5,300 tok/s/kW (800 GB in total leaves 300 GB of KV ≈ 915 users. In 32 microbatches of ~29 users, each microbatch touches 45% of the experts, so each token reads ~8.7 GB. That is 26× more bytes per token, against only ~3.8× better bandwidth per kW. KV is 656 B/token/layer, from the FP8 MLA layout in ledger fact 6.) | RATIO 0.19
VERDICT | DEAD | Its own claim to depend "only on measured" data fails. The one measured hybrid-bond chip delivers about 7.5× less bandwidth per mm² than the design assumes. Even at the assumed bandwidth, 25.6 GB per package is too small to batch enough users to spread the cost of reading the weights, so it loses about 5× on tokens per kW to Rubin.
NEW FACT | The Alibaba ISSCC 2022 hybrid-bonded logic-to-DRAM chip is 602.22 mm² with 1.38 TB/s system bandwidth. Both figures come from secondary sources, and I did not find the paper's pJ/bit, so the 0.66 pJ/bit the idea uses is unverified. | https://www.monolithic3d.com/blog/archives/03-2022

I put the arithmetic in `gate.py` in the working directory and did not commit it. The cost and BOM splits in Idea 1 and the model shape in Idea 2 (FP4 weights of ~500 GB, 95% of them in experts) are my own assumptions, not sourced figures.

Sources:
- [siliconanalysts – HBM pricing](https://siliconanalysts.com/market-data/hbm-pricing)
- [siliconanalysts – method notes](https://siliconanalysts.com/data/hbm-pricing/methodology)
- [MonolithIC 3D blog, Mar 2022](https://www.monolithic3d.com/blog/archives/03-2022)
- [The Register – Alibaba hybrid-bond chip](https://www.theregister.com/2021/12/08/alibaba_teases_a_breakthrough_chip/)
