**Targets and metrics.** The targets are data-center MoE inference and frontier training. The metrics are $ per sustained TB/s, tokens/J and cost per training step. The cost ledger only leaves room for a 3x gain in chip BOM (D) and training hardware (B). Inference TCO (A) is capped by vendor margin, so the ideas below do not claim 3x there. All figures are my estimates and are not yet verified.

=== IDEAS ===
IDEA 1
NAME: Continuum-B mature-node bandwidth die
MECHANISM: Decode spends most of its energy and BOM moving bytes rather than computing, so the logic sits on an older ~400 mm² die. The die has a wide LPDDR6 interface: about 48 devices on an organic substrate, an est. ~1.2 TB/s and ~200 GB, with no CoWoS and no HBM. Experts stay fixed per die, and tokens are routed to the experts instead of moving weights. The closest earlier attempts were Groq and Cerebras, which ran out of capacity, and GDDR boards, which ran out of capacity per chip. This design keeps the capacity, but it can only pay off if it wins on cost per byte/s. The deciding quantity is sustained $ per TB/s. It must come in under about one third of an HBM3E package's roughly $4k/(8 TB/s), measured at the real 27–60% bandwidth utilization, not at peak.
VALUE: It removes the HBM and CoWoS terms, which are about two thirds of BOM, from the decode tier.

IDEA 2
NAME: Continuum-T memory-side optimizer pool
MECHANISM: Training chips keep only FP8 weights and activations in 4 HBM stacks instead of 8. The FP32 master weights and the two Adam moments (12 B/param) live in rack-level LPDDR pools. Small update engines next to that memory apply the update there. The closest earlier attempt was ZeRO-Offload, which stalled on PCIe bandwidth and slow CPU updates. Here, each parameter crosses the link only once per optimizer step: 2 B of gradient in and 1 B of weight out. The deciding quantity is update bytes per step against step time. For 1T params that is ~3 TB per step; over a ~10 s step it needs ~300 GB/s per rack, which is easily within link budgets. The design fails if the update falls into the critical path at small global batch.
VALUE: It halves HBM per training chip, cutting an est. ~20% of accelerator BOM in the term that dominates training cost.

IDEA 3
NAME: Continuum-K query-shipping attention nodes
MECHANISM: Each request's KV cache is sharded across cheap DDR5 nodes, each with 12 channels, ~600 GB/s and ~768 GB. Each node runs one fixed exact-attention kernel at FP8. Only the queries and the attention outputs cross the fabric, ~32 KB per token-layer. That is against ~268 MB of KV per layer at 128K context for GQA with 8 KV heads, roughly an 8,000x cut in traffic. The closest earlier attempts were CXL and host offload, which lacked bandwidth, and HBM-PIM, which lacked programmability. Here the bytes never leave the node, and the kernel is fixed, so it needs no general-purpose programming. The deciding quantity is tok/s per user. A 21 GB per-token KV sweep runs at ~28 tok/s on one node, so a user's KV must be split across ≥4 nodes to reach about 110 tok/s.
VALUE: It enables exact long-context decode with KV capacity priced at commodity DRAM instead of HBM.