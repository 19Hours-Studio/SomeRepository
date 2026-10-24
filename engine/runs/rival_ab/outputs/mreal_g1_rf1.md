**Target:** data-center decode of long-context (128K) sparse-attention MoE models of the DeepSeek-V3.2 class, at a floor of 50 tok/s per user.
**Metrics:** J/token and $/token per rack, compared with GB300 NVL72 at the same tok/s/user. These define "best" because decode is the phase that memory traffic and HBM supply bound.
**Facts:** MLA KV is 656 B per token per layer at FP8, the DSA index key is about 132 B, and DSA uses top-2048 selection over 61 layers. An HBM3E stack costs about $550–600.
**My estimates:** everything else.
**What it loses:** prefill and training stay on GPUs and TPUs. Continuum does not win there.

=== IDEAS ===
IDEA 1
NAME: Two-tier exact sparse-KV decode
MECHANISM: HBM holds only each user's DSA index keys. At 128K context these come to 1.03 GB per step and 52 GB/s per user. On-die LPDDR controllers with gather engines hold the full MLA KV, which is 5.1 GB per user, and fetch the model-selected 2,048 rows (82 MB per step, about 4.1 GB/s per user) in the same step. Per chip, 8 TB/s HBM serves about 150 users and 768 GB LPDDR at about 1 TB/s holds their KV. A GB300 keeping everything in HBM is capacity-capped at about 47 users, so this is about 3x the users per HBM-GB (estimate). The closest earlier attempts are KV offload (OasisKV, Grace C2C), which reached 1.7–2.1x using approximate prefetch. Here selection is exact, because the model itself defines the top-k, so outputs do not change. The deciding quantity is LPDDR efficiency on random 656-B gathers. If it is below 40%, the gain collapses.
VALUE: About 3x the concurrent 128K-context users per scarce HBM stack, which cuts $/token by an estimated 1.5–2x on DSA-class models with identical outputs.

IDEA 2
NAME: Expert-stationary LPDDR MoE rack
MECHANISM: A 671B FP4 MoE (about 340 GB) is sharded at about 5.3 GB of experts per chip across 64 organic-substrate, CoWoS-free chips, each with 128 GB LPDDR. Only activations move between chips: about 7 MB per token per step, which is about 16 GB/s per chip at 3,000 tokens per 20 ms step. With about 94 tokens per expert per step, FP4 intensity is about 370 FLOP/B, so each chip needs only about 265 GB/s for weights. The closest earlier attempt is Groq, where 230 MB of SRAM per chip forced hundreds of chips. LPDDR at about $4/GB, against about $16/GB for HBM, supplies capacity without HBM supply limits. At roughly 350 W per chip, the rack stays within about 40 kW of air cooling. The deciding quantity is sustaining at least 64 tokens per expert per step under router skew without breaking the 20 ms step.
VALUE: MoE decode BOM falls by roughly the HBM-plus-packaging share (about 62%) and runs on air-cooled sites, an estimated 1.5–2x lower $/token than NVL72.

IDEA 3
NAME: Switchless scheduled MoE copper mesh
MECHANISM: Expert-parallel dispatch needs only about 16 GB/s per chip of bandwidth. Its real constraint is latency: 61 layers × 2 all-to-alls must fit inside a 20 ms step, which is about 160 µs per layer. Direct copper 800G links in a 2D mesh carry compile-time-scheduled dispatch slots, and a per-step router histogram reallocates those slots. This removes the NVSwitch trays. The closest earlier attempt is Groq's static scheduling, which was stopped by SRAM capacity, not by its network. Separately, TPU ICI still depends on HBM-class packaging. The deciding quantity is p99 all-to-all completion under skewed routing, which must stay below 30 µs.
VALUE: It removes most of the network share (11% of TCO) and switch power, an honest gain of about 1.1x in $/token, with deterministic per-user latency.