=== RECHECK ===
IDEA 1: DRAM bandwidth per Gb at 64 Mb/mm², 4 layers | required 107 GB/s per Gb (44 TB/s over 51.2 GB = 410 Gb; the idea's 48.9 GB gives 114) (exact arithmetic) | available 35.8 GB/s per Gb (Alibaba ISSCC 2022: 1.38 TB/s over 602 mm² × 64 Mb/mm² = 38.5 Gb; [Semiconductor Digest](https://semiconductor-digest.com/?p=22931) for the bandwidth). The paper's capacity and die areas were not found, so the idea's 135 is unverified. | MARGIN 0.33

IDEA 2: package cost for a 1.5× cut in cost per token | required ≤ $11.7k per package (0.259 × $45k, package share 45%, the rest unchanged) | available ~$8.1k if HBM4 is 288 GB × $16/GB (DigiTimes, FACT 25) = $4.6k, plus the idea's own $1.5k logic and $2k packaging. The idea's $16k assumes ~$42/GB for HBM, well above every ledger price ($10–16/GB). | MARGIN 1.44 (0.73 at the idea's own $16k)

IDEA 3: all-reduce latency across 32 dies, ~9.4 per stage | required ≤ 2.25 µs each (1,000 tok/s/user over 17 stages leaves 58.8 µs per stage, minus 37.7 µs compute, over 9.4 all-reduces; the idea assumes 1 µs) (exact arithmetic) | available ~32 µs for a small all-reduce on 8× B300 over NVLink 5 ([NCCLbpf, arXiv 2603.11438](https://arxiv.org/pdf/2603.11438)). That is a GPU-to-GPU number on another system; I found no measurement for 32 dies on an organic package. | MARGIN 0.07 against the GPU measurement; no direct measurement exists, and the 1 µs assumption is unmeasured

IDEA 4: per-user decode rate with die-by-die layer pipelining | required ≥ 100 tok/s/user (the interactive floor; the sibling SRAM design targets ~1,000) | available 21.8 tok/s/user (39.7 GB ÷ 0.864 TB/s = 46 ms per token, exact arithmetic) | MARGIN 0.22 (0.02 against 1,000 tok/s)

IDEA 5: package price cut against a $55k Rubin | required ≤ $14.3k per package for 1.5× (74% cut; same 45% package share) | available ~$53k. The only quantified saving is 96 GB less HBM at $18.4/GB = $1.8k; the compute and scale-up savings are unquantified. | MARGIN 0.27 (~0.27 if the compute savings are small; the 1.19–1.24× claim needs only a ~37% cut)

IDEA 6: hybrid-bonded logic-to-DRAM bandwidth per mm² | required 17.25 GB/s per mm² (27.6 TB/s over 4 × 400 mm²) (exact arithmetic) | available 2.29 GB/s per mm² (Alibaba ISSCC 2022: 1.38 TB/s over 602 mm², both from secondary sources; the bonded area may be smaller than the die) | MARGIN 0.13

Notes are in `/home/user/SomeRepository/engine/runs/v6_continuum/eval_g2_re/r1/notes.md`.