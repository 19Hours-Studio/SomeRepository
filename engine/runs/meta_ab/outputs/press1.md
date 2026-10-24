**Targets.** Continuum is for data-center frontier models: dense or MoE training, and serving with long context. It is scored on three metrics:
- tokens per joule at matched quality, the primary metric
- dollars per million tokens
- time-to-train per megawatt

Edge chips are out of scope. The CONTEXT figures you mentioned weren't included in the question, so I have used only physical limits, not vendor numbers.

**Why it beats the field.** Rubin and Ironwood still pay full voltage margin on every operation, memory bandwidth for every weight, and switch power for every collective. WSE-3 and Groq remove the off-chip memory traffic, but only by spending enormous SRAM area, capped at about 44 GB per wafer. Continuum attacks all three costs at the physics level instead of the integration level.

**Hard limits it respects:**
- Reticle size is about 858 mm².
- CoWoS and HBM supply limit how many packages can be built.
- Packages near 2 kW require liquid cooling.
- Dynamic energy scales with V², and leakage sets a floor below roughly 0.4 V.
- Analog optical signal-to-noise ratio caps precision at about 6–8 bits per hop.

**Rest of the stack:**
- **Numerics:** FP8/FP4 with stochastic rounding.
- **Programming model:** JAX/Triton-level graphs, plus compiler passes that assign an error budget to each tensor.
- **Packaging:** chiplets on silicon interposer, with co-packaged optics and direct-to-die liquid cooling.

**What must be true for it to work:**
1. Algorithm-based checksums can catch timing faults for less than 10% overhead.
2. Feed-forward (FFN) activations cluster tightly enough that retrieval error stays below FP4 quantization noise.
3. Error feedback absorbs the noise of analog gradient summation, as it already does for 1-bit SGD compression.

Each of these can be tested on existing FPGAs and photonic test chips before committing to silicon.

=== IDEAS ===
IDEA 1
NAME: Error-Budgeted Near-Threshold Silicon
MECHANISM: Tensor tiles run at about 0.45 V, where timing faults are frequent, instead of carrying the usual guard-band margins. Every matrix tile carries row and column checksums computed in a small, full-voltage sidecar. A mismatch triggers a local recompute, and per-tile voltage is retuned continuously from the observed fault rate. The compiler gives each tensor an error budget, so tolerant layers run lower than sensitive ones.
VALUE: Energy per operation falls about 3× through V² scaling while results stay exact, which raises tokens per joule beyond any guard-banded GPU or TPU.

IDEA 2
NAME: Retrieval-Replaced Feed-Forward Layers
MECHANISM: Each FFN layer's input space is clustered offline, and for each centroid the precomputed outputs are stored in dense 3D NAND stacked beside the compute die. At runtime, a locality-sensitive hash finds the nearest centroid, its stored output is prefetched, and only a low-rank correction is computed for the residual. Cache entries are added or refined online from serving traffic.
VALUE: Most FFN FLOPs and weight bandwidth become cheap flash reads, so cost per million tokens is set by bit density instead of HBM or SRAM supply.

IDEA 3
NAME: Physical Optical Gradient Summation
MECHANISM: Each chip intensity-modulates its gradient shard onto a shared wavelength, and photodetectors read the summed optical power, so the network performs the reduction in a single hop. Error-feedback buffers on each chip store the quantization and noise residual and re-inject it in the next step. Precision per pass adapts to the measured signal-to-noise ratio.
VALUE: All-reduce becomes a constant-latency, switchless physical operation, so data-parallel training scales across racks without collective bottlenecks.