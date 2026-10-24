**Continuum: three candidate architectures, each built around the scarce inputs**

**Targets and metrics.** The question I answer is how much delivered throughput each scarce input yields: per HBM stack, per CoWoS wafer, and per facility kW. Those inputs gate 2027–28 volume. User-facing metrics are tokens/s per user (at least 50) and tokens/J. For training, the metric is useful FLOP per stack. Inference total cost has no room for a 3x gain because vendor margin dominates it. Chip bill of materials (BOM) and training do have room. I therefore claim gains of 1.3–2x, not "best overall".

**Reference points (vendor figures, not verified).**

| Design | Memory | Bandwidth | Compute |
|---|---|---|---|
| Rubin | ~288 GB HBM4 | ~22 TB/s | ~50 PF FP4 |
| Ironwood | 192 GB | 7.4 TB/s | 4.6 PF FP8 |
| WSE-3 | 44 GB SRAM | n/a | n/a |
| Groq | 230 MB per chip | n/a | n/a |

**Established facts:**
- Decode is memory-bound.
- HBM is roughly 45% of the B200 BOM, at about $550–600 per stack.
- Absorbed-MLA decode is compute-bound.

**Software, all three ideas.**
- PyTorch runs through a torch.compile backend, and serving uses vLLM/SGLang kernels.
- Checkpoints run unmodified, with no lossless-breaking tricks.

**Test plan.** Replay real serving and training traces in a cycle-level simulator, calibrated first on H100, where the known result is about 27% achieved HBM bandwidth. Each idea dies if its deciding quantity misses its threshold.

=== IDEAS ===
IDEA 1
NAME: Half-HBM training die
MECHANISM: Pair about 4.5 PF FP8 with only 4 HBM stacks instead of 8. This raises the compute-to-bandwidth ridge from about 560 to 1,100 FLOP/B (est.). About 400 MB of on-die SRAM tiles the GEMMs, and ZeRO sharding covers the lost capacity. Ironwood and B200 stop short because they spend 8 stacks per die on flexibility that training GEMMs rarely use. The deciding quantity is the share of step time spent in ops below 1,100 FLOP/B (norms, attention backward, MoE dispatch, optimizer); above about 15%, the gain disappears.
VALUE: Roughly 2x training FLOP per HBM stack and per CoWoS wafer, and about 1.3x lower chip BOM (est.).

IDEA 2
NAME: Stacked-SRAM weights, HBM KV
MECHANISM: Hybrid-bond three SRAM layers over the logic die. This gives about 4 GB per package (est., from V-Cache density of about 1.6 MB/mm² per layer) at a cost of about $650, close to one HBM stack. A 96-package pod holds a 671B FP4 MoE stationary in SRAM, and the remaining HBM serves only the KV cache. Groq and Cerebras stopped short at 230 MB and 44 GB because the KV cache also had to fit in SRAM; here KV stays in HBM, so context length is not capped. The deciding quantity is the weight share of HBM bytes per decode step at deployed batch and context. That share is about 50% at 32K, so the gain is about 2x, falling to about 1.1x at 128K.
VALUE: About 2x decode tokens per HBM stack and per joule for medium-context MoE serving (est.), using hybrid bonding rather than extra stacks.

IDEA 3
NAME: Attention in HBM4 base die
MECHANISM: Use the logic-process base die of a custom HBM4 stack to run one fixed kernel: GQA paged-attention partial softmax, at about 16 FLOP/B. Only partial results then cross the interposer. Samsung's HBM-PIM died on programmability and on DRAM-process logic. This design avoids both by exposing a single vLLM operator and building it on an N3-class base die. The deciding quantity is internal TSV bandwidth over external PHY bandwidth, assumed 2–3x but unverified. At 1x, only the energy saving remains.
VALUE: About 1.5–2x long-context GQA decode tokens per stack and lower mJ per token, though none on compute-bound MLA models.