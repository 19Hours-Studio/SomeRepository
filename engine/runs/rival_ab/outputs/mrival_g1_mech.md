**Continuum: what "best" means here.** The target is data-center serving of large MoE models (1T total and about 32B active parameters, FP4 weights) at 32K–128K context. A second target is training on the same silicon. The metrics are mJ/token and $/Mtoken at ≥100 tok/s/user, plus BF16/FP8 training $/token. These terms carry the most cost: HBM is about 45% of BOM, and memory traffic is about 50% of decode energy (that share is an estimate).

**Deciding arithmetic.** At 32K context with MLA (about 70 KB/token), KV traffic is about 2.2 GB per request-step.
- In HBM at about 3 pJ/bit (assumed), that is about 53 mJ/token. This is consistent with the measured 107–242 mJ.
- At 0.5 pJ/bit it is about 9 mJ.

**Where Continuum should win and lose (estimates):**

| Versus | Continuum | Margin |
|---|---|---|
| Rubin and Ironwood | Wins on tok/J | 2–4x |
| Groq and Cerebras | Wins on chips per model | about 10x fewer |
| Rubin | Loses on peak dense FLOPs per package | about 1.5x |
| Rubin | Loses on software maturity | not quantified |

**Risks:**
- Hybrid-bond yield.
- DRAM-on-logic thermals above about 1 W/mm².
- FP4 training beyond 12B parameters, which is unproven.

**Software.** It must provide a PyTorch/vLLM backend from day one.

**Falsification tests:**
- A cycle simulation of DeepSeek-class decode against measured B200 mJ/token.
- A thermal test chip with 4-high DRAM.

Continuum is a credible candidate for best on these metrics, not a proven one.

=== IDEAS ===
IDEA 1
NAME: Bonded-DRAM Decode Tiles
MECHANISM: Four DRAM dies are hybrid-bonded directly onto each compute die, giving about 16 GB at about 0.5 pJ/bit and about 8 TB/s per die (assumed figures). This replaces HBM's long PHY path at about 3 pJ/bit. Expert weights stay resident and are sharded across about 64 dies, and the KV pages of each request live in the bonded DRAM on the die that owns its attention heads. The closest earlier attempts are Groq and Cerebras SRAM designs, which lacked capacity (230 MB per chip; 44 GB per wafer). Bonded DRAM gives about 70x Groq's capacity per die. The deciding quantity is delivered pJ/bit at 1 W/mm² without thermal throttling.
VALUE: Long-context decode energy could fall from about 53 mJ to about 9 mJ of KV traffic per token.

IDEA 2
NAME: Exact Attention Memory Appliance
MECHANISM: Decode is split by operation. Feed-forward and expert matrix work runs on compute-dense dies. Exact softmax attention over paged KV runs on commodity LPDDR modules that carry simple dot-product logic. The appliance exposes only the paged-attention kernel interface that vLLM already calls, so the computation stays lossless and needs no general programming. The closest earlier attempt is PIM (HBM-PIM, UPMEM), which stalled on programmability. That is avoided by offering one fixed operation. The deciding quantity is $/(TB/s) of LPDDR against HBM at about $20/GB.
VALUE: KV capacity would scale with cheap DRAM, so batch size is no longer limited by scarce HBM.

IDEA 3
NAME: Spill-Tolerant LPDDR Training Dies
MECHANISM: Each 2 PFLOP die has 256 MB of SRAM for activations and LPDDR5X at about 0.5 TB/s for weights, optimizer state and checkpointed activations. It sits on standard organic packaging, with no CoWoS and no HBM. A transformer layer offers about d/1.4 FLOP per byte, about 6,000 at d=8192, so each die needs only about 0.35 TB/s off-chip. The closest earlier attempt is Cerebras weight streaming, which was limited by 150 GB/s of off-wafer I/O on a single wafer. Here each die has its own memory channels. The deciding quantity is achieved FLOP per off-chip byte at production microbatch sizes.
VALUE: Training hardware would no longer need HBM and CoWoS, which together are about two-thirds of BOM.