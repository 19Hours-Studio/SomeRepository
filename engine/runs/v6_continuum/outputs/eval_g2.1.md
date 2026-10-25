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