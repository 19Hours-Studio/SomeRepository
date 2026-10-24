**Shared paradigm in the 8 obvious answers.** Stacked DRAM over logic, LPDDR prefill dies, SRAM-resident experts, attention in the HBM base die, GDDR racks, FP4 training, split attention/expert dies and HBM-lean trainers all do the same thing: they move bytes to a cheaper or closer memory tier. The three answers below instead cut the number of byte transfers per useful token or step.

**Targets and metrics.**
- Decode: tokens/s per user and joules per token (Archetype C, TIGHT).
- Training: cost per converged run, including networking (Archetype B, ROOM).
- Facts are cited in the brief. Everything marked "est." is my assumption.

**Decode energy check (est.).** Take C's shares of 50/15/18/7/5/5. Suppose a hardware verifier accepts 3.5 tokens per weight-and-KV pass and adds 30% compute.
- Energy per token ≈ 50/3.5 + 15×1.3 + 18/3.5 + 7/3.5 + 5 + 5 ≈ 51, which is about **2x** better.
- This is not a 10x gain, and it shrinks at large batch, where Rubin- or Ironwood-class decode is already compute-bound.
- Against WSE-3 or Groq it loses on per-user speed but needs no hundreds of chips.

**Training check (est.).** Removing the scale-up fabric and most cluster networking (13% plus the NVLink premium on the 44% hardware share) gives about 1.2–1.4x at best. Staff cost (33%) caps it.

**Falsifiers.**
- Measure acceptance rate at temperature 1 on production traces. Below 2.5, the decode idea fails.
- Run a 100B+ low-communication training run to equal FLOPs. A loss gap above 1%, or benchmark drops like those seen with NVFP4, kills the training idea.
- Sample the shared-prefix fraction across real agent and RAG logs. Below 50%, the prefix engine is not worth its area.

**Main risks.**
- Draft-model drift.
- Outer-optimizer instability at scale.
- Software: every idea must ship as PyTorch/vLLM backends, not a new language. That is the lesson of Graphcore and Gaudi.

=== IDEAS ===
IDEA 1
NAME: Continuum on-die speculative tree verifier
MECHANISM: A small resident draft head proposes a 32–64-node token tree. Fixed-function tree-attention and rejection-sampling units then verify all nodes in one pass over the weights and KV. Exact rejection sampling keeps outputs distribution-identical, and the tree shape adapts to measured acceptance. The closest earlier attempt is EAGLE/Medusa running on GPUs, where kernel and sampling overhead consumed the gain at batch scale. Here verification is hardwired and sized for low-batch, long-context serving. The deciding quantity is accepted tokens per pass at temperature 1, which must be at least 3.
VALUE: Gives about 2x joules per token and about 3x tokens/s per user on long-context decode without new memory technology.

IDEA 2
NAME: Continuum fabric-free low-communication trainer
MECHANISM: Islands of 8–16 air-cooled chips each train a replica. A hardware outer-optimizer engine streams compressed, quantized parameter deltas over commodity Ethernet every few hundred steps, with no scale-up fabric. The closest earlier attempt is DiLoCo/Streaming DiLoCo on GPUs, whose buyers still paid for NVLink and whose loss parity was shown only below frontier scale. This design removes that fabric from the bill of materials. The deciding quantity is the loss gap against synchronous training at equal FLOPs for models of 100B parameters and up.
VALUE: Cuts the networking and scale-up share of frontier run cost, which is about 1.3x per run.

IDEA 3
NAME: Continuum content-addressed shared-prefix attention
MECHANISM: KV pages are hashed and deduplicated in hardware. A cascade-attention unit reads each shared-prefix page once per batch as a dense GEMM over all requests that share it, and reads only per-user suffix KV individually. The closest earlier attempt is vLLM prefix caching and Hydragen, which save capacity, but GPU paged kernels often still re-stream shared KV per request. The deciding quantity is the shared-prefix fraction of context in production agent traffic.
VALUE: Divides KV bandwidth and capacity per user by the sharing factor, raising long-context batch size on any memory tier.