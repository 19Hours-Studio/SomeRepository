=== TRIAGE ===
IDEA 1 | I 4 | P 3 | DECIDES: accepted tokens/pass at T>0 and production batch (≥3) | Speculation works on HBM parts too, so the "vs. no speculation" baseline is unfair. 256 GB can't hold a 671B MoE, and KV reads aren't amortized.

IDEA 2 | I 3 | P 5 | DECIDES: ≥64 tokens/expert/step under router skew within a 20 ms step | Arithmetic holds and beats Groq's capacity limit. Archetype A has no room: a 10x silicon/HBM cut gives only 1.08x, and margin gives 1.34x, so the 1.5–2x claim exceeds the ledger. Attention/KV is unaddressed.

IDEA 3 | I 2 | P 2 | DECIDES: sustained $/TB/s < ~$167 | Fails its own test: 200 GB LPDDR at ~$4/GB for 1.2 TB/s is ~$670/TB/s, against HBM3E at ~$500/TB/s. LPDDR is cheap per GB, not per GB/s.

IDEA 4 | I 2 | P 5 | DECIDES: p99 all-to-all < 30 µs under skew | Network ceiling is 1.11x, and the idea honestly claims ~1.1x. TPU tori show it's buildable.

IDEA 5 | I 3 | P 4 | DECIDES: CPO laser/module FIT vs. copper NVL72 availability | 72 W at 5 pJ/bit checks out. Value is site access, not much $/token (facility ceiling 1.22x).

IDEA 6 | I 3 | P 5 | DECIDES: all-to-all p99 < ~50 µs/layer | Near-duplicate of Idea 2. Numbers check (10.6 GB/1.1 TB/s ≈ 10 ms), but it runs into the same Archetype A ceiling.

IDEA 7 | I 4 | P 3 | DECIDES: loss gap vs. synchronous at equal FLOPs, ≥100B | Networking ceiling is 1.13x. Frontier DiLoCo parity is unproven, and 8–16-chip islands must still hold the model.

IDEA 8 | I 6 | P 4 | DECIDES: accuracy loss of FP4 KV at 128K | Targets the 1.82x HBM-streaming term. Part of the 4x gain comes from the FP4 format, which GPUs can adopt too. Base-die thermals are a risk.

IDEA 9 | I 2 | P 5 | DECIDES: per-chip HBM actually freed vs. ZeRO-sharded optimizer state | ZeRO already shards Adam state to small per-chip shares, so the halved HBM yields ≈1.1x at most.

IDEA 10 | I 7 | P 3 | DECIDES: whole-step achieved FLOP/B ≥ 2,500 | Hits the room-bearing terms: B accelerator 1.66x, D HBM 1.68x. 13x Cerebras's off-wafer bandwidth answers that design's failure. Risks are 512 MB of stacked SRAM and the beachfront for 2 TB/s of LPDDR. Scale-out is unspecified.

IDEA 11 | I 3 | P 6 | DECIDES: shared-prefix fraction of production context | Works, but FlashInfer cascade/Hydragen already do it in software, so a chip is unnecessary.

IDEA 12 | I 4 | P 5 | DECIDES: expert-weight bytes per prefill batch vs. LPDDR bandwidth | 8K-token MoE prefill touches all ~340 GB of experts (0.34 s at 1 TB/s), which doesn't fit 256 GB. Rubin CPX is prior art.

IDEA 13 | I 3 | P 2 | DECIDES: $ per sustained TB/s of DDR5 nodes vs. HBM | Node bandwidth is shared: 4 nodes serve one 128K user at 110 tok/s, roughly ten times HBM's cost per TB/s.

IDEA 14 | I 6 | P 5 | DECIDES: LPDDR efficiency on random 656-B gathers | Arithmetic is correct (47 vs. 150 users, exact DSA top-k). But 150 users × 4.1 GB/s = 615 GB/s needs ~60% efficiency, not 40%. Limited to DSA-class models, and it needs both HBM and LPDDR PHYs.

IDEA 15 | I 5 | P 5 | DECIDES: accepted tokens/pass at T=1 (≥3) | Attacks the bandwidth term on long-context decode. Gains collapse at batch because compute saturates, not because of kernel overhead, so hardwiring adds little over GPU EAGLE.