# Continuum: decode-first rack architecture (proposal; all Continuum numbers are design estimates)

**Target and metrics.** Continuum targets long-context (32K) MoE decode for DeepSeek/Kimi-class models (671B total, 37B active parameters). It is ranked on three metrics:
- joules per token,
- cost per token,
- tokens/s per rack.

All three are measured at a floor of **≥100 tok/s/user**, the same band as GB200 InferenceX (85–195). Decode is where tokens are sold, and memory movement dominates its energy.

**Explicit losses.**
- **Training:** Continuum loses. The SRAM holds weights, not optimizer state.
- **Single-stream latency:** it loses to Cerebras and Groq, which exceed 1,000 tok/s/user.
- **Margin and staff cost:** no chip can touch either.

**Deciding arithmetic (est.).**
- **FP4 weights:** 335 GB. At batch 64 with top-8 of 256 experts, about 87% of experts are touched per step. That is about 4.5 GB of weight reads per token.
  - From HBM (~30 pJ/B) this costs about 135 mJ/token.
  - From stacked SRAM (~1.5 pJ/B) it costs about 7 mJ/token.
- **MLA KV:** about 35 KB per token, so a 32K context is 1.1 GB/user. At 100 tok/s that needs 110 GB/s per user.

**Reference figures (vendor-reported).**

| Design | Memory per chip | Memory bandwidth | Power / scale |
|---|---|---|---|
| GB200 NVL72 | 72 × ~186 GB HBM | 576 TB/s per rack | ~120–130 kW per rack |
| Ironwood | 192 GB | 7.4 TB/s | — |
| WSE-3 | 44 GB SRAM | — | — |
| Groq LPU | 230 MB | — | — |

**Falsification test.** Replay production decode traces through a cycle model plus a measured hybrid-bond SRAM test chip. Continuum is wrong if any of these holds:
- **Energy:** J/token is less than 1.5× better than measured GB300.
- **SRAM cost:** stacked-SRAM good-die cost exceeds $250/GB.
- **Expert balance:** the hottest expert's chip exceeds 2× the mean expert load at batch 64.

=== IDEAS ===
IDEA 1
NAME: Expert-stationary stacked-SRAM rack
MECHANISM: Each of 96 packages hybrid-bonds two N3 SRAM dies (~3.5 GB) onto a logic die, so the rack holds all 335 GB of FP4 weights on-chip. Only activations cross the scale-up fabric, and hot experts are replicated from routing statistics. The closest attempt is Groq, which stalled on capacity at 230 MB per chip; 3D stacking plus FP4 gives about 15× more capacity per chip. The deciding quantity is good-die stacked-SRAM cost per GB, which must stay under about $250/GB against HBM's ~$24/GB.
VALUE: It cuts the weight-read term of MoE decode energy about 19× (135 to 7 mJ/token, est.) at ≥100 tok/s/user.

IDEA 2
NAME: Attention in HBM4 base die
MECHANISM: A custom HBM4 logic base die runs one fixed kernel: exact flash-decode partial attention over the KV resident in that stack. Only per-head partial sums and softmax maxima leave the stack, so output is unchanged. The closest attempt is HBM-PIM, which died on general programmability; this exposes a single vLLM attention op and nothing else. The deciding quantity is the base die's internal TSV bandwidth and pJ/B relative to the PHY-plus-interposer path.
VALUE: It roughly doubles KV bytes/s and halves KV energy per token at 32K+ context without changing model outputs.

IDEA 3
NAME: Two-stack-per-package decode rack
MECHANISM: Weights live in on-package SRAM, so each package needs only two HBM4 stacks, which hold KV alone. A 96-package rack then has about 6.9 TB of KV and about 384 TB/s of bandwidth. That serves about 3,500 users at 32K and 100 tok/s, roughly 350k tok/s per rack, at about 70 kW, using 192 stacks against NVL72's 576. The closest attempt is the HBM-everything GPU, stopped by sold-out HBM and CoWoS supply. The deciding quantity is KV bandwidth per user (110 GB/s) against per-stack bandwidth.
VALUE: It targets roughly 2× fewer joules and about 3× fewer HBM stacks per token than GB300 for long-context MoE serving.