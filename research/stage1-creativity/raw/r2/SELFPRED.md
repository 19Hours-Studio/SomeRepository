**Run 1, predicted core mechanisms:**
1. Continuous latent recurrence: a shared block iterates over a hidden state with learned adaptive halting, reasoning without emitting tokens.
2. Test-time weight updates: a small fast-weight module takes gradient steps on the context during inference, storing it in weights rather than the KV cache.
3. Multi-timescale byte-level hierarchy: learned boundary detection pools bytes into chunks that a slower outer model processes.

**Run 2, predicted core mechanisms:**
1. Parallel diffusion decoding: the whole output is produced by iterative denoising over the full sequence rather than left to right.
2. Differentiable external memory: a key-value store with learned write gates and sparse retrieval across sessions.
3. Routed specialist composition: a learned router assembles small expert modules into a per-input computation graph.

**Estimated overlap:** about 1 of 3 ideas shared in substance. The memory ideas (fast weights in Run 1 versus an external store in Run 2) are the most likely point of convergence, and a grader that treats them as one mechanism would count 2. My best single estimate is 1.